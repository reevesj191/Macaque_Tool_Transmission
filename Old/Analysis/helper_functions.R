################################################################################
# Helper_Functions                                                             #
# Author: Jonathan S. Reeves                                                   #
# Last Updated: 3/23/2022                                                      #
#                                                                              #  
# This script contains the functions used in the analysis and diagnostics      #
# scripts. This script is read in by using the source function and does not    #
# need to be called directly.                                                  #
# published in the [INSERT TITLE, JOURNAL AND DOI here].                       #
#                                                                              #      
################################################################################

compile_csv_data <- function(xdir, str_pattern = "run_data.csv"){
  
  # Combines together CSV files within a single folder
  # with the same file structure and naming pattern.  
  
  xfiles <- list.files(xdir,pattern = str_pattern)
  print(paste(length(xfiles), "Found"))
  
  for(i in xfiles){
    
    csv <- read.csv(paste0(xdir, i))
    
    if(exists("compiled")){
      compiled <- rbind(compiled, csv)
    }else{
      compiled <- csv
    }
  }
  
  return(compiled[,-1]) 
  
}

mm_graph_prep <- function(V = nodes, E = edges, ABM = TRUE) {
  
  require(dplyr)
  require(igraph)
  require(ggplot2)
  
  
  if(ABM == TRUE){
    V <- V[,-1]
    E <- E[,-1]  
    V <- subset(V, living == "True")
  }
  
  edges_wt <- E %>% 
    group_by(source,target) %>%
    suppressMessages(summarise(weight = n()))
  
  
  nodes <- subset(V, id %in% edges_wt$source | id %in% edges_wt$target)
  
  edges_wt <- subset(edges_wt, source %in% nodes$id)
  edges_wt <- subset(edges_wt, target %in% nodes$id)
  
  
  
  g <- graph_from_data_frame(d = edges_wt,
                             vertices = nodes)
  
  V(g)$color <- ifelse(V(g)$tool_user == "True", "orange","blue")
  
  dist<- distances(graph = g,v = V(g),to = V(g)[V(g)$tool_user == "True"])
  
  
  xdata <- list()
  xdata[[1]] <- nodes
  xdata[[1]]$EV_C <- eigen_centrality(g)$vector
  xdata[[1]]$dist_2_tu <- apply(dist, 1, mean, na.rm = TRUE)
  
  
  xdata[[2]] <- edges_wt
  
  xdata[[3]] <- g
  
  xdata[[4]] <- ggplot(xdata[[1]], aes(x = tool_user, y=EV_C)) +
    geom_boxplot() + geom_jitter()
  
  return(xdata)
  
}

