#install.packages("arules")
#install.packages("arulesSequences")
#install.packages("stringr")
#install.packages("repurrrsive")

library(Matrix)
library(arules)
library(arulesSequences)
library(readr)
library(stringr)
library(purrr)
library(repurrrsive)
library(tidyverse)

absolute_min_support = 1


run <- function(){
  data_file <- '../data.txt'
  
  source("data_processing.R")
  seqs <- read_file_and_get_sequences(data_file)
  print(seqs)
  number_of_sequences <- length(unique(seqs$sequenceID))
  data <- preprocess_data(seqs)
  print(data)
  
  min_sup= absolute_min_support/number_of_sequences - 0.0000001 # xd
  result <- cspade(
    data, 
    parameter = list(support = min_sup), 
    control = list(verbose = FALSE)
  )
  print(result)
  inspect((result))
}

run()



