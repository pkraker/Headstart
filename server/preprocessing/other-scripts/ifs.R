library('httr')
library('async')


set_config(timeout(90))

get_nouns <- function(id, index) {
  url <- paste("http://localhost:5001/noun_chunks", index, id, sep="/")
  res <- GET(url)
  nc <- unlist(httr::content(res)$noun_chunks)
  return(nc)
}

create_nouns <- function(text, index, lang) {
  url <- "http://localhost:5002/tag"
  body <- list(lang=, doc=toJSON(text))
  res <- POST(url, body=body, encode='json')
  nc <- unlist(httr::content(res)$noun_chunks)
  return(nc)
}

create_nouns_batch <- function(docs, lang) {
  url <- "http://localhost:5002/batch_pos"
  body <- list(lang=lang, docs=toJSON(docs))
  res <- POST(url, body=body, encode='json')
  nc <- httr::content(res)$noun_chunks
  nc <- lapply(nc, unlist)
  return(nc)
}

post_nouns <- function(id, nc, index) {
  url <- paste("http://localhost:5001/noun_chunks", index, id, sep="/")
  body <- list(noun_chunks = toJSON(nc))
  res <- POST(url, body=body, encode='json')
}

get_or_create_nouns_async <- function(docs, index, lang) {
  nc <- synchronise(async_map(docs$id, get_nouns, index=index))
  nc_null <- which(unlist(lapply(nc, is.null)))
  if (length(nc_null) > 0) {
    nc_fill <- create_nouns_batch(docs$paper_abstract, lang=lang)
    mapply(post_nouns, docs[nc_null, 'id'], nc_fill, MoreArgs=list(index=index))
    nc[nc_null] <- nc_fill
  }
  return(nc)
}

get_ne <- function(id, index) {
  url <- paste("http://localhost:5001/entities", index, id, sep="/")
  res <- GET(url)
  nc <- unlist(httr::content(res)$ne)
  return(nc)
}

create_ne_batch <- function(docs, lang) {
  url <- "http://localhost:5002/batch_ner"
  body <- list(lang=lang, docs=toJSON(docs))
  res <- POST(url, body=body, encode='json')
  ne <- httr::content(res)$entities
  ne <- lapply(ne, unlist)
  return(ne)
}

post_ne <- function(id, ne, index) {
  url <- paste("http://localhost:5001/entities", index, id, sep="/")
  body <- list(entities = toJSON(ne))
  res <- POST(url, body=body, encode='json')
}

get_or_create_ne_async <- function(docs, index, lang) {
  ne <- synchronise(async_map(docs$id, get_ne, index=index))
  ne_null <- which(unlist(lapply(ne, is.null)))
  if (length(ne_null) > 0) {
    ne_fill <- create_ne_batch(docs$paper_abstract, lang=lang)
    mapply(post_ne, docs[ne_null, 'id'], ne_fill, MoreArgs=list(index=index))
    ne[ne_null] <- ne_fill
  }
  return(ne)
}

#noun_chunks <- get_or_create_nouns_async(metadata, index)
