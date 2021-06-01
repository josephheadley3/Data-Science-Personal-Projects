library(shiny)
library(DT)
library(data.table)

library(tidyverse)
library(jsonlite)
library(tidytext)
library(reshape2)
library(recommenderlab)

busn_recs <- readRDS("busn_recs.Rdata")
busn_sent <- readRDS("busn_sent.Rdata")
businesses <- readRDS("businesses.Rdata")


MakeSentiment <- function(comment, business_name, stars){
  
  # remove any new lines
  review <- gsub("\n","",comment)
  
  # tokenize
  tokens <- tibble(text = review) %>% unnest_tokens(word, text)
  
  # get the sentiment from each review: 
  sentiment_df <- tokens %>%
    inner_join(get_sentiments("bing")) %>% # pull out only sentiment words
    count(sentiment) %>% # count the # of positive & negative words
    spread(sentiment, n, fill = 0) %>% # made data wide rather than narrow
    mutate(user_id = "New User") %>% # add the user id
    mutate(business_id = businesses$business_id[businesses$name == business_name][1]) %>% # add the business id
    mutate(rating = stars) %>% # add the user ratings
    mutate(gval = ifelse("positive" %in% names(.), gval <- positive, gval <- 0)) %>%
    mutate(bval = ifelse("negative" %in% names(.), bval <- negative, bval <- 0)) %>%
    mutate(review_score = gval/(gval + bval)) %>% # add user review sentiment analysis score
    mutate(sentiment_score = (rating + review_score)/2)
  
  sentiment_df <- sentiment_df[, !(names(sentiment_df) %in% c("positive", "negative", "gval", "bval", "review_score", "rating"))]
  
  # return our sentiment dataframe
  return(sentiment_df)
}


Recommendation <- function(comment1, comment2, comment3, business_name1, business_name2, business_name3, stars1, stars2, stars3){
  busn_sent <- rbind(busn_sent, MakeSentiment(comment1, business_name1, stars1))
  busn_sent <- rbind(busn_sent, MakeSentiment(comment2, business_name2, stars2))
  busn_sent <- rbind(busn_sent, MakeSentiment(comment3, business_name3, stars3))
  
  sentiment_mat <- reshape2::dcast(data = busn_sent, user_id ~ business_id, mean, value.var = "sentiment_score", na.rm = T)
  rownames(sentiment_mat) <- sentiment_mat[,1]
  sentiment_mat <- as.matrix(sentiment_mat[,-1])
  sentiment_mat = as(sentiment_mat, "realRatingMatrix")
  
  rec_mod <- Recommender(sentiment_mat[1:(length(table(busn_sent$user_id))-1)], method = "UBCF", param=list(method="Cosine",nn=10))
  
  Top_5_df=tibble()
  Top_5_pred <- predict(rec_mod, sentiment_mat[which(rownames(sentiment_mat) == "New User")], n=5)
  Top_5_List <- as(Top_5_pred, "list")
  cur_Top_5_df <- tibble(business_id = Top_5_List[[1]])
  cur_Top_5_df <- left_join(cur_Top_5_df, businesses, by="business_id")
  if(length(cur_Top_5_df$name) == 0) {
    Top_5_df <- rbind(Top_5_df, rep(NA,5))
  }
  if(length(cur_Top_5_df$name) > 0 & length(cur_Top_5_df$name) < 5) {
    filler <- c(cur_Top_5_df$name, rep(NA, 5-length(cur_Top_5_df$name)))
    Top_5_df <- rbind(Top_5_df, filler)
  }
  else {
    Top_5_df <- rbind(Top_5_df, t(cur_Top_5_df$name))
  }
  rownames(Top_5_df) <- rownames(sentiment_mat)[which(rownames(sentiment_mat) == "New User")]
  return(Top_5_df)
}


ui <- fluidPage(titlePanel("Yelp Dataset Recommender System"),
                fluidRow(
                  column(4, h3("Business #1"),
                         selectInput(inputId = "business1",
                                     label = "Choose a business to rate and review",
                                     choices = busn_recs,
                                     selected = "Legal Sea Foods"),
                         numericInput(inputId = "rating1",
                                      label = "Give a rating to selected business",
                                      value = 2,
                                      min = 1,
                                      max = 5,
                                      step = 0.25),
                         textInput(inputId = "review1",
                                   label = "Give a review to selected business",
                                   value = "Good")),
                  column(4, h3("Business #2"),
                         selectInput(inputId = "business2",
                                     label = "Choose a business to rate and review",
                                     choices = busn_recs,
                                     selected = "Loca Luna"),
                         numericInput(inputId = "rating2",
                                      label = "Give a rating to selected business",
                                      value = 3,
                                      min = 1,
                                      max = 5,
                                      step = 0.25),
                         textInput(inputId = "review2",
                                   label = "Give a review to selected business",
                                   value = "Great")),
                  column(4, h3("Business #3"),
                         selectInput(inputId = "business3",
                                     label = "Choose a business to rate and review",
                                     choices = busn_recs,
                                     selected = "IKEA"),
                         numericInput(inputId = "rating3",
                                      label = "Give a rating to selected business",
                                      value = 4,
                                      min = 1,
                                      max = 5,
                                      step = 0.25),
                         textInput(inputId = "review3",
                                   label = "Give a review to selected business",
                                   value = "Amazing"))
                ),
                submitButton(text = "Submit"),
                verbatimTextOutput("printout"),
                dataTableOutput("df") )
server <- function(input, output) {
  #output$printout <- renderPrint({c(input$business, input$rating, input$review)})
  output$df <- DT::renderDataTable({datatable(Recommendation(input$review1, input$review2, input$review3, 
                                                             input$business1, input$business2, input$business3, 
                                                             input$rating1, input$rating2, input$rating3), rownames = T)})
}
shinyApp(server = server, ui = ui)