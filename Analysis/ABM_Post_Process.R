################################################################################
# ABM data processing script.                                                  #
# Author: Jonathan S. Reeves                                                   #
# Last Updated: 3/23/2022                                                      #
#                                                                              #  
# This script will iterate through all the ABM output files and bundle them    #
# into two RDS files that are used to carry out the diagnotistcs and analysis  #
# published in the [INSERT TITLE, JOURNAL AND DOI here].                       #
#                                                                              #      
################################################################################

# Read in helper_functions

source("Analysis/helper_functions.R")

# Compile the run summary data

## Set a path to where the ABM output is held
PATH <- "Data/ABM/"

## Run the compile_csv_data helper function
run_data <- compile_csv_data(xdir = PATH, str_pattern = "_run_data.csv")

## save the file as an RDS file 

saveRDS(run_data, "Data/ABM_run_summaries.RDS")



# Do social network analysis and compile results. 

run_data <- subset(run_data, stop_reason == "Tool Pop Achieved")

run_data$mean_user_EV <- NA
run_data$mean_non_user_EV <- NA
nodes_compile <- data.frame()

plots <- list()

a <- 0

for(run in 1:nrow(run_data)){
  
  a <- a+1
  id <- run_data$run_id[run]  
  nodes <- read.csv(paste0(PATH,id,"_nodes.csv"))
  edges <- read.csv(paste0(PATH,id,"_social_edges.csv"))
  
  xdata <- mm_graph_prep(V=nodes, E=edges)
  
  xdata[[1]]$EV_C_STD <- as.numeric(scale(xdata[[1]]$EV_C))
  nodes_compile <- rbind(xdata[[1]],nodes_compile)
  
  mean_ec_c <- xdata[[1]][xdata[[1]]$age >=25,] %>% 
    group_by(tool_user) %>%
    summarize(mean_EC_C = mean(EV_C))
  
  run_data[run_data$run_id == id,]$mean_user_EV <- as.numeric(mean_ec_c[2,2])
  run_data[run_data$run_id == id,]$mean_non_user_EV <- as.numeric(mean_ec_c[1,2])
  
  plots[[a]] <- xdata[[4]] + ggtitle(run_data$transmission_mech[run])
  
}

run_data$ev_diff <- run_data$mean_user_EV-run_data$mean_non_user_EV

nodes_compile$U <- ifelse(nodes_compile$tool_user == "False",0,1)
nodes_compile$A <- ifelse(nodes_compile$age >= 25, 2,1)

nodes_compile$H <- ifelse(nodes_compile$A == 1, 
                          nodes$hair, 
                          nodes_compile$hair + 2)



saveRDS(nodes_compile, "Data//ABM_Compiled.RDS")
readRDS(file = "Data/ABM_run_summaries.RDS")
