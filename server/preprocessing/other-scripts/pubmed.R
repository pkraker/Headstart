library("rentrez")
library("data.table")
library("xml2")
library("tidyverse")

# get_papers for Pubmed via Entrez API
#
# Params:
#
# * query: search query
# * params: parameters for the search in JSON format
#    * from: publication date lower bound in the form YYYY-MM-DD
#    * to: publication date upper bound in the form YYYY-MM-DD
#    * article_types: in the form of an array of identifiers of article types
#    * sorting: can be one of "most-relevant" and "most-recent"
# * limit: number of search results to return
#
# It is expected that get_papers returns a list containing two data frames named "text" and "metadata"
#
# "text" contains the text for similarity analysis; it is expected to have two columns "id" and "content"
#
# "metadata" contains all metadata; has the following columns:
# * "id": the DOI
# * "pmid": the PMID
# * "title": the title
# * "authors": authors, in the format "LASTNAME1, FIRSTNAME1;LASTNAME2, FIRSTNAME2", split by ;
# * "paper_abstract": the abstract
# * "published_in": name of the journal or venue
# * "year": publication year
# * "date": publication date
# * "url": URL to the landing page
# * "subject": keywords, split by ;
#
# Examples:
# get_papers(query = "ecology")
# get_papers(query = "ecology", params = list(from = "2016/04/01", to = "2016/06/05"))


plog <- getLogger('api.pubmed')


get_papers <- function(query, params = NULL, limit = 100) {
  plog$info(paste("Search:", query))
  start.time <- Sys.time()

  fields <- c('.//ArticleTitle', './/MedlineCitation/PMID', './/Title', './/Abstract')
  year = './/Article/Journal/JournalIssue/PubDate'
  book_fields <- c('.//BookDocument/Book/BookTitle', './/BookDocument/PMID',
                   './/BookDocument/Book/Publisher/PublisherName', './/Abstract')
  book_year = './/BookDocument/Book/PubDate'
  fnames <- c('title', 'pmid', 'published_in', 'paper_abstract')
  date <- './/MedlineCitation/DateCreated'
  authors <- './/AuthorList'
  keywords <- './/Keyword'
  doi <- ".//PubmedData/ArticleIdList/ArticleId[@IdType=\"doi\"]"
  sortby = ifelse(params$sorting == "most-recent", "", "relevance")
  from = gsub("-", "/", params$from)
  to = gsub("-", "/", params$to)
  article_types_string = paste0(" ((", '"', paste(params$article_types, sep='"', collapse='"[Publication Type] OR "'), '"[Publication Type]))')
  exclude_articles_with_abstract = " AND hasabstract"
  #HOTFIX - article_types cause a 414 with PubMed
  #query <- paste0(query, article_types_string, exclude_articles_with_abstract)
  query <- paste0(query, exclude_articles_with_abstract)
  plog$info(paste("Query:", query))

  n_batches = ceiling(limit/25)
  limits <- table(cut(1:limit, n_batches, labels=FALSE))
  retstarts <- cumsum(limits) - limits
  search <- rentrez::entrez_search(db = "pubmed", term = query, retmax = limit,
                                   mindate = from, maxdate = to, sort=sortby, use_history=TRUE)
  searches <- lapply(1:n_batches, function(i) {
    rentrez::entrez_search(db = "pubmed", term = query, retmax = limits[i], retstart = retstarts[i],
                           mindate = from, maxdate = to, sort=sortby, use_history=TRUE)
  })
  res <- lapply(1:n_batches, function(i){
    rentrez::entrez_fetch(db = "pubmed", web_history = searches[[i]]$web_history,
                          retstart = retstarts[i], retmax = limits[i], rettype = "xml")
  })
  
  xml <-sapply(res, function(x) xml2::xml_children(xml2::read_xml(x)))


  out <- lapply(xml, function(z) {
    flds <- switch(
      xml2::xml_name(z),
      PubmedArticle = fields,
      PubmedBookArticle = book_fields
    )
    tmp <- stats::setNames(
      lapply(
        flds,
        function(w) xml2::xml_text(xml2::xml_find_all(z, w))
      ),
      fnames
    )
    xdate <- paste0(vapply(xml2::xml_children(xml2::xml_find_all(z, date)), function(a) {
      xtext(a)
    }, ""), collapse = "-")

    year_fld <- switch(
      xml2::xml_name(z),
      PubmedArticle = year,
      PubmedBookArticle = book_year
    )

    xyear <- vapply(xml2::xml_find_all(z, year_fld), function(a) {
      if(!is.na(xml2::xml_find_first(a, ".//Year"))) {
        xtext(xml2::xml_find_first(a, ".//Year"))
      } else {
        substr(xtext(xml2::xml_find_first(a, ".//MedlineDate")),0,4)
      }
    }, "")

    xauthors <- paste0(vapply(xml2::xml_children(xml2::xml_find_all(z, authors)), function(a) {
      if(!is.na(xml2::xml_find_first(a, ".//CollectiveName"))) {
        xtext(xml2::xml_find_first(a, ".//CollectiveName"))
      } else {
        paste(
          xtext(xml2::xml_find_first(a, ".//LastName")),
          xtext(xml2::xml_find_first(a, ".//ForeName")),
          sep = ", "
        )
      }
    }, ""), collapse = ";")
    xkeywords <- paste0(xtext(xml2::xml_find_all(z, keywords)), collapse = ";")
    xdoi <- xtext(xml2::xml_find_all(z, doi))
    lst <- c(tmp, date = xdate, year = xyear, id = xdoi, authors = list(xauthors), subject = list(xkeywords))
    lst[vapply(lst, length, 1) != 1] <- NA
    return(lst)
  })

  df <- data.table::setDF(data.table::rbindlist(out, fill = TRUE, use.names = TRUE))
  df <- setNames(df, tolower(names(df)))
  df$url <- paste0("http://www.ncbi.nlm.nih.gov/pubmed/", df$pmid)
  df$paper_abstract <- gsub("^\\s+|\\s+$", "", gsub("[\r\n]", "", df$paper_abstract))
  df$content <- paste(df$title, df$paper_abstract, df$authors, df$subject, df$published_in, sep= " ")
  df$doi = df$id
  df$id = df$pmid
  df$subject_orig = df$subject

  summary <- rentrez::entrez_summary(db="pubmed", web_history = search$web_history, retmax = limit)
  readers <- data.frame(list(readers=extract_from_esummary(summary, "pmcrefcount")))
  readers$pmid <- rownames(readers)
  df <- merge(df, readers, by="pmid", all.x=TRUE)

  idlist = extract_from_esummary(summary, "articleids", simplify = FALSE)
  pmc_ids <- data.frame(list(pmcid=cbind(lapply(idlist, function(x) x$articleids %>% subset(idtype=="pmc") %>% select(value) %>% pull()))))
  pmc_ids$pmid <- rownames(pmc_ids)
  pmc_ids <- unnest(pmc_ids)
  df <- merge(df, pmc_ids, by="pmid", all.x=TRUE)

  end.time <- Sys.time()
  time.taken <- end.time - start.time
  plog$info(paste("Time taken:", time.taken, sep=" "))

  return(list(metadata = df, text = df[,c('id', 'content')]))
}

xtext <- function(x) xml2::xml_text(x)


valid_langs <- list(
    'eng'='english'
)
