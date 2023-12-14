
## 清空环境
rm(list=ls())  

## 加载必要包
library(stats4)
library(splines)
library(VGAM)   

## 加载程序
source("./czip_statistics_functions.R")
source("./czip_parplot_functions.R")
source("./czip_data_functions.R")

## 配置模拟设置
set.seed(2021)
cut=30;
nsim=100;
ns=c(50,100,200,500,1000);
lp=0.01*(seq(5,30,5));
mu=c(-0.5,0.5,1,1.5)

aa=c(-0.5,0.5,1,1.5)
bb=c(-0.5,0.5,1,1.5)



## CASE 1：无协变量
################################################################################
# 生成数据并保存
filename = "czip_power_case1"
datacase1 <- power_data_func(mu = mu,aa = NULL,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = NULL)
save(datacase1,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case1"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase1$wald_conv), 2:4, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase1$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:4, sum);

datacase1$lr[datacase1$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase1$wald[datacase1$wald_conv>0]=NA;
datacase1$score[which(datacase1$wald_conv>0)]=NA;
datacase1$snew[which(datacase1$wald_conv>0)]=NA;

wald_statistic <- datacase1$wald                                          # 获取统计量
lr_statistic <- datacase1$lr
score_statistic <- datacase1$score
snew_statistic <- datacase1$snew

pw1<-1-pnorm(wald_statistic);     pl1<-(1-pchisq(lr_statistic, df=1))/1;
ps1<-1-pnorm(score_statistic);    pn1<-1-pnorm(snew_statistic);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply((pl1<0.05)*(datacase1$wald_wrhop>0), 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图1:QQ图
filename = "czip_power_case1"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/power_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase1$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,mu = mu,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off()  
# # 布图2:统计量直方图
# filename = "czip_power_case1"
# thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
# pdf(paste("../A4_report/power_hist/hist_",filename,"_","Wald_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = wald_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Wald")
# dev.off()  
# pdf(paste("../A4_report/power_hist/hist_",filename,"_","LR_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = lr_statistic,mu = mu,alpha = NULL,ns = ns,statname = "LR")
# dev.off()  
# pdf(paste("../A4_report/power_hist/hist_",filename,"_","Score_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = score_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Score")
# dev.off()  
# pdf(paste("../A4_report/power_hist/hist_",filename,"_","He_",thistime,'.pdf',sep=""))
# type1error_hist_par_func(statistic = snew_statistic,mu = mu,alpha = NULL,ns = ns,statname = "Snew")
# dev.off()  


## CASE 2：一个服从正态分布N(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_power_case2"
datacase2 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'norm')
save(datacase2,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case2"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase2$wald_conv), 2:4, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase2$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:4, sum);

datacase2$lr[datacase2$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase2$wald[datacase2$wald_conv>0]=NA;
datacase2$score[which(datacase2$wald_conv>0)]=NA;
datacase2$snew[which(datacase2$wald_conv>0)]=NA;

wald_statistic <- datacase2$wald                                          # 获取统计量
lr_statistic <- datacase2$lr
score_statistic <- datacase2$score
snew_statistic <- datacase2$snew


pw1<-1-pnorm(datacase2$wald);     pl1<-(1-pchisq(datacase2$lr, df=1))/1;
ps1<-1-pnorm(datacase2$score);    pn1<-1-pnorm(datacase2$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图1：QQ图
filename = "czip_power_case2"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/power_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase2$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off() 



## CASE 3：一个服从均匀分布U(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_power_case3"
datacase3 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'unif')
save(datacase3,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case3"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase3$wald_conv), 2:4, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase3$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:4, sum);

datacase3$lr[datacase3$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase3$wald[datacase3$wald_conv>0]=NA;
datacase3$score[which(datacase3$wald_conv>0)]=NA;
datacase3$snew[which(datacase3$wald_conv>0)]=NA;

wald_statistic <- datacase3$wald                                          # 获取统计量
lr_statistic <- datacase3$lr
score_statistic <- datacase3$score
snew_statistic <- datacase3$snew


pw1<-1-pnorm(datacase3$wald);     pl1<-(1-pchisq(datacase3$lr, df=1))/1;
ps1<-1-pnorm(datacase3$score);    pn1<-1-pnorm(datacase3$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图
filename = "czip_power_case3"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/power_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase3$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off() 

## CASE 7：一个服从正态分布N(0,1)的协变量 + logit变换的omega
################################################################################
# 生成数据并保存
filename = "czip_power_case7"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
datacase7 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'norm_logit')
save(datacase7,file=paste("../A2_data/data_",filename,"_",thistime,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case7"
load(paste("../A2_data/data_",filename,"_",thistime,".RData",sep = ""))
apply(is.na(datacase7$wald_conv), 2:4, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase7$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:4, sum);

datacase7$lr[datacase7$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase7$wald[datacase7$wald_conv>0]=NA;
datacase7$score[which(datacase7$wald_conv>0)]=NA;
datacase7$snew[which(datacase7$wald_conv>0)]=NA;

wald_statistic <- datacase7$wald                                          # 获取统计量
lr_statistic <- datacase7$lr
score_statistic <- datacase7$score
snew_statistic <- datacase7$snew



pw1<-1-pnorm(datacase7$wald);     pl1<-(1-pchisq(datacase7$lr, df=1))/1;
ps1<-1-pnorm(datacase7$score);    pn1<-1-pnorm(datacase7$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);

# 布图
pdf(paste("../A4_report/plot_",filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase7$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off()


## CASE 4：两个服从正态分布N(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_power_case4"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
datacase4 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'two_norm')
save(datacase4,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case4"
load(paste("../A2_data/data_",filename,".RData",sep = ""))
pw1<-1-pnorm(datacase4$wald);     pl1<-(1-pchisq(datacase4$lr, df=1))/1;
ps1<-1-pnorm(datacase4$score);    pn1<-1-pnorm(datacase4$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图
filename = "czip_power_case4"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/plot_",filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase4$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off() 



## CASE 5：两个服从均匀分布U(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_power_case5"
datacase5 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'two_unif')
save(datacase5,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case5"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))
pw1<-1-pnorm(datacase5$wald);     pl1<-(1-pchisq(datacase5$lr, df=1))/1;
ps1<-1-pnorm(datacase5$score);    pn1<-1-pnorm(datacase5$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图
filename = "czip_power_case5"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase5$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off() 



## CASE 6：一个服从正态分布N(0,1)的协变量 + 一个服从均匀分布U(0,1)的协变量
################################################################################
# 生成数据并保存
filename = "czip_power_case6"
datacase6 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'two_unif')
save(datacase6,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case6"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))
pw1<-1-pnorm(datacase6$wald);     pl1<-(1-pchisq(datacase6$lr, df=1))/1;
ps1<-1-pnorm(datacase6$score);    pn1<-1-pnorm(datacase6$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图
filename = "czip_power_case6"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase6$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off() 






## CASE 8：一个服从均匀分布U(0,1)的协变量 + logit变换的omega
################################################################################
# 生成数据并保存
filename = "czip_power_case8"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
datacase8 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'unif_logit')
save(datacase8,file=paste("../A2_data/data_cut",as.character(cut),filename,"_",thistime,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case8"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))
pw1<-1-pnorm(datacase8$wald);     pl1<-(1-pchisq(datacase8$lr, df=1))/1;
ps1<-1-pnorm(datacase8$score);    pn1<-1-pnorm(datacase8$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);

# 布图
filename = "czip_power_case8"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase8$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off()



## CASE 9：一个服从正态分布N(0,1)的协变量 + sin非线性变换的omega
################################################################################
# 生成数据并保存
filename = "czip_power_case9"
datacase9 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'norm_sin')
save(datacase9,file=paste("../A2_data/data_",filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case9"
load(paste("../A2_data/data_",filename,".RData",sep = ""))
pw1<-1-pnorm(datacase9$wald);     pl1<-(1-pchisq(datacase9$lr, df=1))/1;
ps1<-1-pnorm(datacase9$score);    pn1<-1-pnorm(datacase9$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图
filename = "czip_power_case9"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/plot_",filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase9$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off() 



## CASE 10：一个服从均匀分布U(0,1)的协变量 + sin非线性变换的omega
################################################################################
# 生成数据并保存
filename = "czip_power_case10"
datacase10 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'unif_sin')
save(datacase10,file=paste("../A2_data/data_",filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case10"
load(paste("../A2_data/data_",filename,".RData",sep = ""))
pw1<-1-pnorm(datacase10$wald);     pl1<-(1-pchisq(datacase10$lr, df=1))/1;
ps1<-1-pnorm(datacase10$score);    pn1<-1-pnorm(datacase10$ss);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图
filename = "czip_power_case10"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/plot_",filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase10$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off() 



## CASE 11：两个服从均匀分布U(0,1)的协变量 + sin非线性变换的omega
################################################################################
## CASE 12：两个服从正态分布N(0,1)的协变量 + sin非线性变换的omega
################################################################################
## CASE 13：两个服从均匀分布U(0,1)的协变量 + logit变换的omega
################################################################################
## CASE 14：两个服从正态分布N(0,1)的协变量 + logit变换的omega
################################################################################



## CASE 11：一个服logit的协变量
################################################################################
# 生成数据并保存
filename = "czip_power_case3"
datacase3 <- power_data_func(mu = NULL,aa = aa,bb = 1.45,lp = lp,ns = ns,nsim = nsim,cut = cut,method = 'unif')
save(datacase3,file=paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

# 加载数据并计算
filename = "czip_power_case3"
load(paste("../A2_data/data_cut",as.character(cut),filename,".RData",sep = ""))

apply(is.na(datacase3$wald_conv), 2:4, sum);                              # 统计未收敛的数据（wald/lr）

ss=is.na(datacase3$wald);                                                 # 统计wald中为na的数据
apply(ss, 2:4, sum);

datacase3$lr[datacase3$wald_conv>0]=NA;                                   # 未收敛数据处理
datacase3$wald[datacase3$wald_conv>0]=NA;
datacase3$score[which(datacase3$wald_conv>0)]=NA;
datacase3$snew[which(datacase3$wald_conv>0)]=NA;

wald_statistic <- datacase3$wald                                          # 获取统计量
lr_statistic <- datacase3$lr
score_statistic <- datacase3$score
snew_statistic <- datacase3$snew


pw1<-1-pnorm(datacase3$wald);     pl1<-(1-pchisq(datacase3$lr, df=1))/1;
ps1<-1-pnorm(datacase3$score);    pn1<-1-pnorm(datacase3$snew);
pw2=apply(pw1<0.05, 2:4,mean,na.rm=T);  pl2=apply(pl1<0.05, 2:4,mean,na.rm=T);  
ps2=apply(ps1<0.05, 2:4,mean,na.rm=T);  pn2=apply(pn1<0.05, 2:4,mean,na.rm=T);  

# 布图
filename = "czip_power_case3"
thistime = gsub(":","-",gsub("\\s", "_", as.character(Sys.time())))
pdf(paste("../A4_report/power_plot/plot_cut",as.character(cut),filename,"_",thistime,'.pdf',sep=""))
power_plot_par_func(lp = datacase3$lp,ps = ps2,pw = pw2,pl = pl2,pn = pn2,alpha = aa,ns = ns,legend_x = -0.6,legend_y = -0.7) # x绝对值越大 越左；y绝对值越大 越下；
dev.off() 



