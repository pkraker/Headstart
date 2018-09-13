rm(list = ls())

library(rstudioapi)

options(warn=1)

wd <- dirname(rstudioapi::getActiveDocumentContext()$path)

setwd(wd) #Don't forget to set your working directory

#query <- "russian" #args[2]
#service <- "pubmed"
#params <- NULL
#params_file <- "params_pubmed.json"

source("../vis_layout.R")
#source('../pubmed.R')
source('../utils.R')

debug = FALSE

MAX_CLUSTERS = 15
ADDITIONAL_STOP_WORDS = "english"

#if(!is.null(params_file)) {
#  params <- fromJSON(params_file)
#}

library(SPARQL)

endpoint = 'https://query.wikidata.org/sparql'

query = '#    ?main_subject rdfs:label ?main_subjectLabel.
SELECT DISTINCT ?item ?_PubMed_ID ?PMCID ?publication_date ?DOI ?itemLabel
(GROUP_CONCAT(DISTINCT ?published_in; SEPARATOR = "; ") AS ?publicationQId)  
(GROUP_CONCAT(DISTINCT ?published_inLabel; SEPARATOR = "; ") AS ?publication)  
(GROUP_CONCAT(DISTINCT ?author_name_string; SEPARATOR = "; ") AS ?authors) 
(GROUP_CONCAT(DISTINCT ?main_subjectLabel; SEPARATOR = "; ") AS ?subject) WHERE {
{
  SELECT * WHERE {
  ?item wdt:P31 wd:Q13442814.
  ?item rdfs:label ?itemLabel.
  FILTER(CONTAINS(LCASE(?itemLabel), "zika"))
  FILTER((LANG(?itemLabel)) = "en")
  }
  LIMIT 1000
}
OPTIONAL { ?item wdt:P698 ?_PubMed_ID. }
OPTIONAL { ?item wdt:P1433 ?published_in.
?published_in rdfs:label ?published_inLabel.
FILTER((LANG(?published_inLabel)) = "en")
}
OPTIONAL { ?item wdt:P921 ?main_subject. ?main_subject rdfs:label ?main_subjectLabel. FILTER((LANG(?main_subjectLabel)) = "en")}
OPTIONAL { ?item wdt:P932 ?PMCID. }
OPTIONAL { ?item wdt:P577 ?publication_date. }
OPTIONAL { ?item wdt:P921 ?published_in. }
OPTIONAL { ?item wdt:P2093 ?author_name_string. }
OPTIONAL { ?item wdt:P356 ?DOI }
}
GROUP BY ?item ?itemLabel ?_PubMed_ID ?PMCID ?publication_date ?DOI
LIMIT 100'

qd <- SPARQL(endpoint,query)

metadata = qd$results
names(metadata)[names(metadata)=="item"] <- "id"
names(metadata)[names(metadata)=="DOI"] <- "doi"
names(metadata)[names(metadata)=="itemLabel"] <- "title"
names(metadata)[names(metadata)=="PMCID"] <- "pmcid"
names(metadata)[names(metadata)=="publication_date"] <- "year"
names(metadata)[names(metadata)=="published_in"] <- "journal_id"
names(metadata)[names(metadata)=="published_inLabel"] <- "published_in"
metadata$relevance = seq.int(nrow(metadata))
metadata$id = chartr('<:/>', '____', metadata$id)
metadata$subject_orig = metadata$subject

metadata$year = as.POSIXct(as.numeric(metadata$year), origin="1970-01-01", tz="GMT", format="%Y-%m-%d")

text = data.frame(matrix(nrow=length(metadata$id)))
text$id = metadata$id
# Add all keywords, including classification to text
text$content = paste(metadata$title, 
                     #metadata$paper_abstract,
                     metadata$subject, 
                     metadata$published_in, metadata$authors,
                     sep=" ")

output_json = vis_layout(text, metadata, max_clusters=MAX_CLUSTERS, add_stop_words=ADDITIONAL_STOP_WORDS, testing=TRUE)

write(output_json, "../../../../examples/zika/data/output_zika.json")