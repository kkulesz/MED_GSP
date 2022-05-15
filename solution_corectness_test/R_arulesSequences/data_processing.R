# UGLY AS HELL, FML

read_file_and_get_sequences <- function(filename){
  whole_string <- read_file(filename)
  without_new_lines <- gsub("\r\n", " ", whole_string)
  without_new_lines <- gsub("\n", " ", without_new_lines)
  ints <- strsplit(without_new_lines, split = " ")
  ints <- ints[[1]]
  
  sequences = list()
  transactions = list()
  transaction = c()
  for (i in ints){
    if( i == '-2' ){
      sequences[[length(sequences) + 1]] <- transactions
      transaction <- c()
      transactions <- c()
      next
    }
    
    if( i == '-1' ){
      transaction <- unique(transaction) 
      transactions[[length(transactions) + 1]] <- transaction
      transaction <- c()
      next
    }
    
    transaction <- append(transaction, i)
  }
  
  
  columns <- c("items", "sequenceID", "eventID", "SIZE")
  result <- data.frame(matrix(nrow = 0, ncol = length(columns)))
  colnames(result) <- columns
  
  seq_id = 1
  for (s in sequences){
    tran_time = 0
    for(t in s){
      for (i in t){
        # print(i)
        new_row <- data.frame(items=i, sequenceID=seq_id, eventID=tran_time, SIZE=length(t))
        result <- rbind(result, new_row)
      }
      tran_time <- tran_time + 5
    }
    
    seq_id = seq_id + 1
  }
  
  return(result)
}


preprocess_data <- function(df1){
  # TAKEN FROM(but modified a little): https://github.com/xiaoqingwan/sequential_pattern_mining/blob/main/sequence_mining.R
  
  df1 <- df1 %>% group_by(sequenceID) %>% 
    arrange(eventID) %>% 
    distinct(sequenceID, items, .keep_all = TRUE) %>%
    mutate(item_id = row_number()) %>% 
    select(sequenceID, eventID, item_id, items) %>% 
    ungroup() %>% 
    mutate(across(.cols = c("sequenceID", "items"), .f = as.factor))
  df1 <- df1[order(df1$sequenceID),] # descending order
  df2 <- df1
  df2$unique<-paste0(as.character(df2$sequenceID)," ", as.character(df2$eventID)) 
  df2 <- df2 %>% 
    dplyr::group_by(unique) %>%
    dplyr::summarise(items = paste(items, collapse = ","))
  
  df2$sequenceID <- word(df2$unique, 1)
  df2$eventID <- word(df2$unique, 2)
  
  df2 <- df2 %>% 
    group_by(sequenceID) %>% 
    arrange(eventID) %>% 
    mutate(item_id = row_number()) %>%
    select(sequenceID, eventID, item_id, items) %>% 
    ungroup()
  
  df2 <- df2 %>% arrange(sequenceID)
  
  sessions <-  as(df2 %>% transmute(items = items), "transactions")
  transactionInfo(sessions)$sequenceID <- df2$sequenceID
  transactionInfo(sessions)$eventID <- df2$item_id
  itemLabels(sessions) <- str_replace_all(itemLabels(sessions), "items=", "")

  return(sessions)
}