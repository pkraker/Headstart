library('httr')
library('async')



get_nouns_batch <- function(docs) {
  url <- "http://localhost:5000/batch_tag"
  body <- list(lang="de", docs=toJSON(docs))
  res <- POST(url, body=body, encode='json')
  nc <- httr::content(res)$noun_chunks
  nc <- lapply(nc, unlist)
}

get_nouns <- function(doc_id, index) {
  url <- "http://localhost:5001/noun_chunks"
  body <- list(index=index, doc_id=doc_id)
  res <- POST(url, body=body, encode='json')
  nc <- unlist(httr::content(res)$noun_chunks)
}


get_nouns_async <- function(docs_ids, index) {
  async_map(docs_ids, get_nouns, index=index)
}

#noun_chunks <- synchronise(get_nouns_async(input_data$metadata$id, index))
