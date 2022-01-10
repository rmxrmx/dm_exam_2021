# seed RNG and load libraries
set.seed(1982)
library(R2jags)
library(polspline)

# data from here:
# https://zenodo.org/record/3764693

# set working directory and load data
setwd("./dm_exam/")
a <- read.csv("data_with_percentiles.csv")

# extract info about experiment from data
ntrials <- length(unique(a$Period)) # number of rounds played (aka trials)
nagents <- length(unique(a$Subject))*2 # number of participants
vals <- seq(1,100,1) #possible values to contribute - from 0 to 20 tokens

# extract the relevant contribution values from the overall dataframe
# let's focus on the non-punishment trials only (first 10 trials)
b <- a[a$treat==2,]
b <- b[order(b$Subject), ]
c <- matrix(b$ownCon, nrow = ntrials, ncol = nagents) # converting the contributions to a matrix to feed to JAGS
c <- t(c) # transposing the matrix so the dimensions fit what we've told JAGS
Ga <- matrix(b$sumFSG/10, nrow = ntrials, ncol = nagents) # specifying a "group average" for each participant
Ga <- t(Ga)
#Ga <- colMeans(c) # common group average for *all* participants

# empty data frame to fill with parameter estimates from jags model
MAP <- c()
MAP$omega1 <- array(0,nagents)
MAP$lambda <- array(0,nagents)
MAP$gamma <- array(0,nagents)
MAP$pbeta <- array(0,nagents)
#-----------------------------------------------------------
  
#-----------------------------------------------------------
#prepare jags model for inference
data <- list("ntrials", "nagents", "vals", "c","Ga") #data inputted into jags
params <- c("omega1","lambda","gamma","p0","pbeta","c","omega") #parameters we'll track in jags
# load and run jags model
samples <- jags(data, inits=NULL, params,
     model.file ="CC_Jags",
     n.chains=3, n.iter=2000, n.burnin=1000, n.thin=1)

# save maximum a posteriori (MAP) values for parameters from fitted model (see CC_jags.txt for more details)
for (n in 1:nagents) {
  
  X <- samples$BUGSoutput$sims.list$omega1[,n]
  MAP$omega1[n] <-density(X)$x[which(density(X)$y==max(density(X)$y))]

  X <- samples$BUGSoutput$sims.list$lambda[,n]
  MAP$lambda[n] <-density(X)$x[which(density(X)$y==max(density(X)$y))]
  
  X <- samples$BUGSoutput$sims.list$gamma[,n]
  MAP$gamma[n] <-density(X)$x[which(density(X)$y==max(density(X)$y))]
  
  X <- samples$BUGSoutput$sims.list$pbeta[,n]
  MAP$pbeta[n] <-density(X)$x[which(density(X)$y==max(density(X)$y))] # this is the slope
  
}

# investigating timing effects
idx <- seq(20,length(b$timing),20) # index looking at one trial per participant (and thereby also allows us to elicit a vector of timing)
times <- b$timing[idx]
t.test(MAP$pbeta[times=="1"],MAP$pbeta[times=="2"])
boxplot(MAP$pbeta[times=="0"],MAP$pbeta[times=="1"], MAP$pbeta[times=="2"], names = c("bottom 25%", "middle 50%", "top 25%"), main="Willingness to conditionally cooperate", ylab="Willingness")
MAP$pbeta
