
## 清空环境
rm(list=ls())  

## 加载必要包
# install.packages("VGAM")
library(stats4)
library(splines)
library(VGAM)   

## 加载程序
source("./czip_statistics_functions.R")
source("./czip_parplot_functions.R")
source("./czip_data_functions.R")

## 配置模拟设置
set.seed(2021)
# cut=7;
cut=4
# cut=30;
# cut=10
nsim=100;
ns=c(50,100,200,500,1000);
lp=0.01*(seq(5,30,5));
mu=c(-0.5,0.5,1,1.5)
aa=c(-0.5,0.5,1,1.5)
bb=c(-0.5,0.5,1,1.5)

## CASE1：无协变量
################################################################################
# 生成数据并保存
filename = "czip_type1error_case1"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
datacase1 <- type1error_data_func(mu=mu,aa=NULL,bb=1.45,beta2=1,ns,nsim,cut=cut,method=NULL)
save(datacase1,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_type1error_case1"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))
apply(is.na(datacase1$wald_conv), 2:3, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase1$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:3, sum);

datacase1$lr[datacase1$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase1$wald[datacase1$wald_conv>0]=NA;
datacase1$score[which(datacase1$wald_conv>0)]=NA;
datacase1$snew[which(datacase1$wald_conv>0)]=NA;

# 计算cut掉的样本量
apply(datacase1$data1,2:3,mean)

wald_statistic <- datacase1$wald                                          # 获取统计量
lr_statistic <- datacase1$lr
score_statistic <- datacase1$score
snew_statistic <- datacase1$snew

pw1<-1-pnorm(wald_statistic);     pl1<-(1-pchisq(lr_statistic, df=1))/1;  # 计算pvalue
ps1<-1-pnorm(score_statistic);    pn1<-1-pnorm(snew_statistic);

# 布图1:QQ图
filename = "czip_type1error_case1"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
type1error_plot_par_func(ps=ps1,pw=pw1,pl=pl1,pn=pn1,mu=mu,alpha = NULL,ns = ns,legend_x = -2.65,legend_y = -.65)# x绝对值越大 越左；y绝对值越大 越下；
dev.off()  

# 布图2:统计量直方图
filename = "czip_type1error_case1"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Wald_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = wald_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Wald")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","LR_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = lr_statistic,mu = mu,alpha = NULL,ns = ns,statname = "LR")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Score_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = score_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Score")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","He_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = snew_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Snew")
dev.off()






## CASE 2：一个服从正态分布N(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_type1error_case2"
datacase2 <- type1error_data_func(mu=NULL,aa=aa,bb=1.45,beta2=1,ns,nsim,cut=cut,method="norm")
save(datacase2,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_type1error_case2"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase2$wald_conv), 2:3, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase2$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:3, sum);

datacase2$lr[datacase2$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase2$wald[datacase2$wald_conv>0]=NA;
datacase2$score[which(datacase2$wald_conv>0)]=NA;
datacase2$snew[which(datacase2$wald_conv>0)]=NA;

# 计算cut掉的样本量
apply(datacase2$data1,2:3,mean)

wald_statistic <- datacase2$wald                                          # 获取统计量
lr_statistic <- datacase2$lr
score_statistic <- datacase2$score
snew_statistic <- datacase2$snew

pw1<-1-pnorm(wald_statistic);     pl1<-(1-pchisq(lr_statistic, df=1))/1;  # 计算pvalue
ps1<-1-pnorm(score_statistic);    pn1<-1-pnorm(snew_statistic);

# 布图1:QQ图
filename = "czip_type1error_case2"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
type1error_plot_par_func(ps=ps1,pw=pw1,pl=pl1,pn=pn1,mu=NULL,alpha = aa,ns = ns,legend_x = -2.65,legend_y = -.65)# x绝对值越大 越左；y绝对值越大 越下；
dev.off()  
# # 布图2:统计量直方图
filename = "czip_type1error_case2"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Wald_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = wald_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Wald")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","LR_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = lr_statistic,mu = mu,alpha = NULL,ns = ns,statname = "LR")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Score_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = score_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Score")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","He_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = snew_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Snew")
dev.off()
# 



## CASE 3：一个服从均匀分布U(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_type1error_case3"
datacase3 <- type1error_data_func(mu=NULL,aa=aa,bb=1.45,beta2=1,ns,nsim,cut=cut,method="unif")
save(datacase3,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_type1error_case3"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase3$wald_conv), 2:3, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase3$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:3, sum);

datacase3$lr[datacase3$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase3$wald[datacase3$wald_conv>0]=NA;
datacase3$score[which(datacase3$wald_conv>0)]=NA;
datacase3$snew[which(datacase3$wald_conv>0)]=NA;

# 计算cut掉的样本量
apply(datacase3$data1,2:3,mean)

wald_statistic <- datacase3$wald                                          # 获取统计量
lr_statistic <- datacase3$lr
score_statistic <- datacase3$score
snew_statistic <- datacase3$snew

pw1<-1-pnorm(wald_statistic);     pl1<-(1-pchisq(lr_statistic, df=1))/1;  # 计算pvalue
ps1<-1-pnorm(score_statistic);    pn1<-1-pnorm(snew_statistic);


# 布图1:QQ图
filename = "czip_type1error_case3"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
type1error_plot_par_func(ps=ps1,pw=pw1,pl=pl1,pn=pn1,mu=NULL,alpha = aa,ns = ns,legend_x = -2.65,legend_y = -.65)# x绝对值越大 越左；y绝对值越大 越下；
dev.off()  

# # 布图2:统计量直方图
filename = "czip_type1error_case3"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Wald_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = wald_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Wald")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","LR_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = lr_statistic,mu = mu,alpha = NULL,ns = ns,statname = "LR")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Score_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = score_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Score")
dev.off()
pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","He_",thistime,'.pdf',sep=""))
type1error_hist_par_func(statistic = snew_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Snew")
dev.off()



## CASE 4：两个服从正态分布N(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_type1error_case4"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
datacase4 <- type1error_data_func(mu=NULL,aa=aa,bb=1.45,beta2=1,ns,nsim,cut=cut,method="two_norm")
save(datacase4,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_type1error_case4"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase4$wald_conv), 2:3, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase4$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:3, sum);

datacase4$lr[datacase4$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase4$wald[datacase4$wald_conv>0]=NA;
datacase4$score[which(datacase4$wald_conv>0)]=NA;
datacase4$snew[which(datacase4$wald_conv>0)]=NA;

wald_statistic <- datacase4$wald                                          # 获取统计量
lr_statistic <- datacase4$lr
score_statistic <- datacase4$score
snew_statistic <- datacase4$snew

pw1<-1-pnorm(wald_statistic);     pl1<-(1-pchisq(lr_statistic, df=1))/1;  # 计算pvalue
ps1<-1-pnorm(score_statistic);    pn1<-1-pnorm(snew_statistic);

# 布图1:QQ图
filename = "czip_type1error_case4"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
type1error_plot_par_func(ps=ps1,pw=pw1,pl=pl1,pn=pn1,mu=NULL,alpha = aa,ns = ns,legend_x = -0.3,legend_y = -1.3)# x绝对值越大 越左；y绝对值越大 越下；
dev.off()  
# # 布图2:统计量直方图
# filename = "czip_type1error_case4"
# thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Wald_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = wald_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Wald")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","LR_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = lr_statistic,mu = mu,alpha = NULL,ns = ns,statname = "LR")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Score_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = score_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Score")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","He_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = snew_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Snew")
# dev.off()  
# 
# 

## CASE 5：两个服从均匀分布U(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_type1error_case5"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
datacase5 <- type1error_data_func(mu=NULL,aa=aa,bb=1.45,beta2=1,ns,nsim,cut=cut,method="two_unif")
save(datacase5,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_type1error_case5"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase5$wald_conv), 2:3, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase5$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:3, sum);

datacase5$lr[datacase5$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase5$wald[datacase5$wald_conv>0]=NA;
datacase5$score[which(datacase5$wald_conv>0)]=NA;
datacase5$snew[which(datacase5$wald_conv>0)]=NA;

wald_statistic <- datacase5$wald                                          # 获取统计量
lr_statistic <- datacase5$lr
score_statistic <- datacase5$score
snew_statistic <- datacase5$snew

pw1<-1-pnorm(wald_statistic);     pl1<-(1-pchisq(lr_statistic, df=1))/1;  # 计算pvalue
ps1<-1-pnorm(score_statistic);    pn1<-1-pnorm(snew_statistic);

# 布图1:QQ图
filename = "czip_type1error_case5"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
type1error_plot_par_func(ps=ps1,pw=pw1,pl=pl1,pn=pn1,mu=NULL,alpha = aa,ns = ns,legend_x = -0.3,legend_y = -1.3)# x绝对值越大 越左；y绝对值越大 越下；
dev.off()  
# # 布图2:统计量直方图
# filename = "czip_type1error_case5"
# thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Wald_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = wald_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Wald")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","LR_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = lr_statistic,mu = mu,alpha = NULL,ns = ns,statname = "LR")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Score_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = score_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Score")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","He_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = snew_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Snew")
# dev.off()  


## CASE 6：一个服从正态分布N(0,1)的协变量 + 一个服从均匀分布U(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_type1error_case6"
datacase6 <- type1error_data_func(mu=NULL,aa=aa,bb=1.45,beta2=1,ns,nsim,cut=cut,method="two_unifnorm")
save(datacase6,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_type1error_case6"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase6$wald_conv), 2:3, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase6$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:3, sum);

datacase6$lr[datacase6$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase6$wald[datacase6$wald_conv>0]=NA;
datacase6$score[which(datacase6$wald_conv>0)]=NA;
datacase6$snew[which(datacase6$wald_conv>0)]=NA;

wald_statistic <- datacase6$wald                                          # 获取统计量
lr_statistic <- datacase6$lr
score_statistic <- datacase6$score
snew_statistic <- datacase6$snew

pw1<-1-pnorm(wald_statistic);     pl1<-(1-pchisq(lr_statistic, df=1))/1;  # 计算pvalue
ps1<-1-pnorm(score_statistic);    pn1<-1-pnorm(snew_statistic);

# 布图1:QQ图
filename = "czip_type1error_case6"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/type1error_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
type1error_plot_par_func(ps=ps1,pw=pw1,pl=pl1,pn=pn1,mu=NULL,alpha = aa,ns = ns,legend_x = -0.3,legend_y = -1.3)# x绝对值越大 越左；y绝对值越大 越下；
dev.off()  
# # 布图2:统计量直方图
# filename = "czip_type1error_case6"
# thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Wald_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = wald_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Wald")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","LR_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = lr_statistic,mu = mu,alpha = NULL,ns = ns,statname = "LR")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","Score_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = score_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Score")
# dev.off()  
# pdf(paste("../A4_report/type1error_hist/hist_",filename,"_","He_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = snew_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Snew")
# dev.off()  
# 

