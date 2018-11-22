library('httr')
library('async')


set_config(timeout(90))

get_nouns_batch <- function(docs, lang) {
  url <- "http://localhost:5002/batch_tag"
  body <- list(lang=lang, docs=toJSON(docs))
  res <- POST(url, body=body, encode='json')
  nc <- httr::content(res)$noun_chunks
  nc <- lapply(nc, unlist)
  return(nc)
}

get_nouns <- function(id, index) {
  url <- paste("http://localhost:5001/noun_chunks", index, id, sep="/")
  res <- GET(url)
  nc <- unlist(httr::content(res)$noun_chunks)
  return(nc)
}

create_nouns <- function(text, index) {
  url <- "http://localhost:5002/tag"
  body <- list(lang='en', doc=toJSON(text))
  res <- POST(url, body=body, encode='json')
  nc <- unlist(httr::content(res)$noun_chunks)
  return(nc)
}

post_nouns <- function(id, nc, index) {
  url <- paste("http://localhost:5001/noun_chunks", index, id, sep="/")
  body <- list(noun_chunks = toJSON(nc))
  res <- POST(url, body=body, encode='json')
}

get_or_create_nouns_async <- function(docs, index) {
  nc <- synchronise(async_map(docs$id, get_nouns, index=index))
  nc_null <- which(unlist(lapply(nc, is.null)))
  if (length(nc_null) > 0) {
    nc_fill <- get_nouns_batch(docs$paper_abstract, lang='en')
    mapply(post_nouns, docs[nc_null, 'id'], nc_fill, MoreArgs=list(index=index))
  }
  return(nc)
}

#noun_chunks <- get_or_create_nouns_async(metadata, index)
