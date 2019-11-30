.libPaths(c('/Users/vlisovyk/Desktop/Data_Science/ShinyLibs', .libPaths()))
# install.packages('rvest')
library(rvest)
all_articles <- list()
article_count = 1
for (page in 1:80) {
    
    url_raw <- paste0('https://www.omicsonline.org/archive-political-sciences-public-affairs-open-access.php?page=', page)
    webpage_raw <- read_html(url_raw)
    outer_div <- html_nodes(webpage_raw, 'a[title="Peer-reviewed Full Article"][href]')

        # for each article:
    for (link_num in 1:length(outer_div)) {
        start_of_link <- 10
        end_of_link <- regexpr('title=', as.character(outer_div)[link_num])-3
        url_article <- substr(as.character(outer_div)[link_num], start_of_link, end_of_link) 
        
        webpage_article <- read_html(url_article)
        full_text <- html_nodes(webpage_article, 'article')
        if (length(full_text) == 0) {
            full_text <- html_nodes(webpage_article, '.full-text')
        } 
        if (length(full_text) == 0) {
            print(paste0('Text returned empty for url: ', url_article, ' Link_num ', link_num, ' page ', page))
            next
        }
        headlines <- full_text %>% html_nodes('h4')
        clean_headlines <- as.list(gsub("<[^>]+>|/[[^/]]+/]", "", headlines))
        if (length(clean_headlines) > 3) clean_headlines <- clean_headlines[2:length(headlines)-1]
                                   
        
        paragraphs <- full_text %>% html_nodes('p') #starts at 5
        if (length(paragraphs) > 8) paragraphs <- paragraphs[5:(length(paragraphs)-3)]
        
        clean_paragraphs <- as.list(gsub("<[^>]+>|\n", "",paragraphs))
        clean_paragraphs <- gsub("\\[.*?\\]", "", clean_paragraphs)
        clean_paragraphs <- gsub(' \\.','.', clean_paragraphs)
        clean_paragraphs <- gsub('\\r ', '', clean_paragraphs)
        
        all_articles[[paste0('article_', article_count)]] <- list()
        all_articles[[paste0('article_', article_count)]]$headlines <- clean_headlines
        all_articles[[paste0('article_', article_count)]]$paragraphs <- clean_paragraphs
        article_count <- article_count + 1
        
    }
    print(paste0('Page ', page, ' ouf of 80'))
    
}


######################################################################
######################## Export data to txt's ########################
######################################################################

library(stringi)
clean_sentences <- function (sentences, start_tag = "^", end_tag = "$") {
    # sanity checks
    stopifnot (is.character (sentences))
    stopifnot (length (sentences) > 0)
    # lower case
    # remove anything that is not alpha, numeric, whitespace or ' (for contractions)
    stri_replace_all_regex(sentences, "[’]", "'")
    sentences <- stri_replace_all_regex (sentences, "[^A-Za-z0-9 ']+", " ")
    # replace all digits with a simple indicator flag
    sentences <- stri_replace_all_regex (sentences, "[[:digit:]]+", "###")
    sentences <- gsub("\\s+", " ", sentences)
    # # add starting/ending tag to each sentence
    # sentences <- stri_paste (start_tag, sentences, end_tag, sep = " ")
    # trim whitespace
    sentences <- stri_trim_both(sentences)
    return (sentences)
}

load('article_data.RData')

results_vector <- c()
for (i in all_articles) {
    if (length(i$headlines) > 0) {
        headlines <- unlist(str_split(i[[1]], '\\.'))
        headlines <- clean_sentences(headlines)
        full_headlines <- headlines[nchar(headlines) > 0]
    } else {
        full_headlines <- NULL
    }
    if (length(i$paragraphs) > 0) {
        # split by sentence
        sentences_list <- lapply(i[[2]], function(y) { return(str_split(y, '\\.')[[1]])} )
        # clear unnecessary symbols
        sentences_list <- lapply(sentences_list, clean_sentences)
        # remove empty sentences
        full_sentences <- unlist(sentences_list)[nchar(unlist(sentences_list)) > 0]
    } else {
        full_sentences <- NULL
    }
    if (!is.null(full_headlines) & !is.null(full_headlines)) {
    result <- c(full_headlines, full_sentences)
    results_vector <- c(results_vector, result)
    } else if (!is.null(full_headlines)) {
        results_vector <- c(results_vector, full_headlines)
    } else {
        results_vector <- c(results_vector, full_sentences)
    }
}

writeLines(results_vector, "../data/article_results.txt")


############### END ################