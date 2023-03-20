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

## debugging


mm_graph_prep <- function(V = nodes, E = edges, ABM = TRUE, living = FALSE) {
  
  require(dplyr)
  require(igraph)
  require(ggplot2)
  
  if(ABM == TRUE){
    V <- V[,-1]
    E <- E[,-1]
    if(living == TRUE){
      V <- subset(V, living == "True")
    }else{
      
    }
    
  }
  
  tu_ids <- V$id[V$tool_user == 'True']
  
  edges_wt <- E %>% 
    group_by(source,target) %>%
    summarise(weight = n())
  
  tu_edges <- subset(edges_wt, source %in% tu_ids)
  
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
  xdata[[1]]$tu_strength <- NA
  
  for(id in xdata[[1]]$id){
    xdata[[1]][xdata[[1]]$id == id,]$tu_strength <- sum(tu_edges$weight[tu_edges$target == id])
  }
  
  xdata[[1]]$tu_strength_std <- 
    (xdata[[1]]$tu_strength - min(xdata[[1]]$tu_strength))/
    (max(xdata[[1]]$tu_strength) - min(xdata[[1]]$tu_strength))
    
  xdata[[2]] <- edges_wt
  
  xdata[[3]] <- g
  
  xdata[[4]] <- ggplot(xdata[[1]], aes(x = tool_user, y=EV_C)) +
    geom_boxplot() + geom_jitter()
  
  return(xdata)
  
}


plot_post_pred <- function(xmodel, sim,line_var, 
                           compat = "PI", prob = .89,alpha = .75,
                           cols = c("#151F30", "#103778", "#0593A2","#FF7A48","#E3371E", 
                                    "#146152", "#44803F", "#B4CF66", "#FFEC5C", "#FF5A33"),
                           xlim = c(0,1), ylim = c(0,1),
                           cex.ax = .5, 
                           titl = "",
                           leg = FALSE){
  
  plot.new()
  plot.window(xlim = xlim, 
              ylim = ylim)
  
  box(which = "plot")
  axis(side=1,cex.axis= cex.ax, cex.lab = .25)
  axis(side=2, cex.axis=cex.ax,cex.lab=.25)  
  
  if(class(xmodel) %in% c("ulam")){
    
    p <- link(xmodel,data = sim)
    p_mean <- apply(p, 2, mean)
    p_ci <- apply(p,2, PI, prob = prob)
    lines(line_var, p_mean, lwd=2)
    shade(p_ci, line_var, col =  col.alpha(cols[1], alpha = .75))
    title(main = titl)
    
  }
  
  if(class(xmodel) == "list"){
    
    for(i in 1:length(xmodel)){
      
      p <- link(xmodel[[i]],data = sim)
      p_mean <- apply(p, 2, mean)
      p_ci <- apply(p,2, PI, prob = prob)
      shade(p_ci, line_var, col =  col.alpha(cols[i], .75))
      lines(line_var, p_mean, lwd=2, lty = i)
      title(main = titl)
      
    }
    
    if(leg == TRUE){
    legend(0, .975, legend=names(xmodel),
           col= cols, lty=1:2, cex=.8,
           box.lty=1, box.lwd=1)
    }else{
      
    }
  }
  
}


process_edges <- function(run_data = run_data, PATH = PATH){
  
  a <- 0
  
  nodes_compile <- data.frame()
  
  run_data$mean_user_EV <- NA
  
  run_data$mean_non_user_EV <- NA
    
  for(run in 1:nrow(run_data)){
    a <- a+1
    id <- run_data$run_id[run]  
    nodes <- read.csv(paste0(PATH,id,"_nodes.csv"))
    edges <- read.csv(paste0(PATH,id,"_social_edges.csv"))
  
    xdata <- mm_graph_prep(V=nodes, E=edges)
  
    nodes_compile <- rbind(xdata[[1]],nodes_compile)
  
    mean_ec_c <- xdata[[1]][xdata[[1]]$age >=25,] %>% 
      group_by(tool_user) %>%
      summarize(mean_EC_C = mean(EV_C))
  
    run_data[run_data$run_id == id,]$mean_user_EV <- as.numeric(mean_ec_c[2,2])
    run_data[run_data$run_id == id,]$mean_non_user_EV <- as.numeric(mean_ec_c[1,2])
  
  
}

  run_data$ev_diff <- run_data$mean_user_EV-run_data$mean_non_user_EV

  nodes_compile$U <- ifelse(nodes_compile$tool_user == "False",0,1)
  nodes_compile$A <- ifelse(nodes_compile$age >= 25, 2,1)

  nodes_compile$H <- ifelse(nodes_compile$A == 1, 
                          nodes$hair, 
                          nodes_compile$hair + 2)
  
  output <- list(run_data, nodes_compile)
  return(output)
}

build.edges <- function(x, ID, Associates){
  xdata <- x
  edges <- data.frame(source = NA, target = NA)
  for(i in 1:nrow(xdata)){
    indiv <- xdata[i,ID]
    Partners <- unlist(strsplit(xdata[i, Associates], c(", "))) 
    for(j in Partners){
      connection <- c(indiv, j)
      edges <- rbind(edges, connection)
      
    }
    
  }
  return(edges[-1,])
  
}



sim_plots <- function(model){
  
  par(mfrow=c(4,2))
  n <- 100
  
  sim <- data.frame(C = seq(from= 0, to= 1, length.out=n),
                    S = rep(c(0),n),
                    H = rep(c(1),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$C,
                 titl = "Centrality"
  )
  sim <- data.frame(C = rep(c(0),n),
                    S = seq(from= 0, to= 1, length.out=n),
                    H = rep(c(1),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$S,
                 titl = "Strength"
  )
  
  sim <- data.frame(C = seq(from= 0, to= 1, length.out=n),
                    S = rep(c(0),n),
                    H = rep(c(2),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$C,
                 titl = "Centrality"
  )
  sim <- data.frame(C = rep(c(0),n),
                    S = seq(from= 0, to= 1, length.out=n),
                    H = rep(c(2),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$S,
                 titl = "Strength"
  )
  
  sim <- data.frame(C = seq(from= 0, to= 1, length.out=n),
                    S = rep(c(0),n),
                    H = rep(c(3),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$C,
                 titl = "Centrality"
  )
  
  sim <- data.frame(#C = seq(from= 0, to= 1, length.out=n),
    C = rep(c(0),n),
    S = seq(from= 0, to= 1, length.out=n),
    H = rep(c(3),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$S,
                 titl = "Strength"
  )
  
  sim <- data.frame(C = seq(from= 0, to= 1, length.out=n),
                    S = rep(c(0),n),
                    H = rep(c(4),n))
  
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$C,
                 titl = "Centrality"
  )
  
  sim <- data.frame(C = rep(c(0),n),
                    S = seq(from= 0, to= 1, length.out=n),
                    H = rep(c(4),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$S,
                 titl = "Strength"
  )
  
}


figure_1 <- function(model, cols = c("#103778",
                                     "#FFB30D",
                                     "#E3371E")){
  
  par(mfrow=c(2,2),
      mar = c(2,2,2,2))
  n <- 100
  
  
  sim <- data.frame(C = seq(from= 0, to= 1, length.out=n),
                    S = rep(c(0),n),
                    H = rep(c(3),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$C,
                 titl = "Centrality: Common",cols = cols,
                 leg = TRUE
  )
  
  sim <- data.frame(C = seq(from= 0, to= 1, length.out=n),
                    S = rep(c(0),n),
                    H = rep(c(4),n))
  
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$C,
                 titl = "Centrality: Hybrid",cols = cols
  )
  
  
  sim <- data.frame(#C = seq(from= 0, to= 1, length.out=n),
    C = rep(c(0),n),
    S = seq(from= 0, to= 1, length.out=n),
    H = rep(c(3),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$S,
                 titl = "Strength: Common",cols = cols
  )
  
  sim <- data.frame(C = rep(c(0),n),
                    S = seq(from= 0, to= 1, length.out=n),
                    H = rep(c(4),n))
  
  plot_post_pred(xmodel = model, 
                 sim = sim, line_var = sim$S,
                 titl = "Strength: Hybrid",cols = cols
  )
  
}
