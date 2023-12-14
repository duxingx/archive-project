
# 清除工作环境
rm(list = ls())
# 加载必要包
library(igraph)  
library(dplyr)
library(plyr)
library(ggplot2)
getwd()

data = read.table("../A2_data/final/CollegeMsg.txt",col.names = c("SRC","DST","UNIXTS") ) 
# head(data)
g <- graph_from_data_frame(data,directed = F)
print(paste("网络的节点数为：",length(V(g))))
print(paste("网络的边数为：",length(E(g))))
print(paste("网络的密度为：",graph.density(g)))



g <- graph_from_data_frame(data,directed = F)
print(paste("网络的节点数为：",length(V(g))))
while (any(degree(g) <10)) {
        g = delete.vertices(g,V(g)[degree(g)<10])
}
print(paste("删除之后网络的节点数为：",length(V(g))))
print(paste("删除之后网络的所有节点数都大于10吗：",all(degree(g)>=10)))

