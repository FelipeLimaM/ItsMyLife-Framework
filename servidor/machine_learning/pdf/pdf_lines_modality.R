#!/usr/bin/env Rscript


args = commandArgs(trailingOnly=TRUE)

data = 0
modality = 0

if (length(args)<2) {
  exit
}

if (grepl(".zip", args[1])){
    data <- read.csv(unz(args[1], args[2]), header=TRUE, sep=",")
    modality <- read.csv(unz(args[1], "modality.csv"), header=F, sep=",")
    output = args[3]
} else {
    data <- read.csv(file=args[1], header=TRUE, sep=",")
    output = args[2]
}


hash <- function(i){
  return (i*265441)%%657
}

cex <- 0.5

data$seconds <- as.POSIXct(trunc(data[,1]),origin="1970-01-01",tz="America/Sao_Paulo")
pdf(output,width=30, height=10)
mar.default <- c(5,5,5,1) + 0.1
par(mar = mar.default + c(0,4,0,0))



init = as.POSIXct(trunc(data[1,1], "days"),origin="1970-01-01")



#colors <- c("blue", "brown", "chartreuse", "cornflowerblue", "darkorange", "coral", "cyan2", "blueviolet", "black", "bisque4", "azure4", "darkred", "darkgreen")
print (max(data[,2])+1)

plot(data[1,1],1,xlab='Time',xlim=c(0,24),ylim=c(trunc(as.numeric(difftime(data[1,1], init,units="days")))+1,trunc(as.numeric(difftime(data[nrow(data),1], init,units="days")))+1),ylab='',
  col=data[1,2]+3,pch=19,cex=cex,xaxt="n",yaxt="n")




previous_time = 0
previous_day = 0
flag = 0
#days_vector = c(format(init, format="%B %d %Y"))
days_vector = c()
for (i in 2:nrow(data)-1){
    day = trunc(as.numeric(difftime(data[i,1], init,units="days")))+1
    next_day = trunc(as.numeric(difftime(data[i+1,1], init,units="days")))+1

    time = as.numeric(difftime(data[i,1], init,units="hours"))%%24


    if(flag == 0){
      previous_time  = as.numeric(difftime(data[i,1], init,units="hours"))%%24
      flag = 1
    }
    if (data[i,2] != data[i+1,2] || day != next_day){

      lines(c(previous_time,time),c(day,day),col=data[i,2]+3,pch=19,lwd=10)
      flag = 0
    }
    if (day != next_day){
      days_vector <- c(days_vector, format(data[i,1], format="(%a) %b %d %Y") )
    }

}
days_vector <- c(days_vector, format(data[nrow(data),1], format="(%a) %b %d %Y") )

x_labels <- c()
for (i in 0:24){
  x_labels <- c(x_labels, paste(formatC(i,width=2,flag="0"),":00H",sep=""))
}

axis(1, at=0:24, label=x_labels)
#text(x = seq(0,24, by=1 ), par("usr")[1]-0.1, labels = x_labels, srt = 0, pos = 1, xpd = TRUE)
text(y = seq(trunc(as.numeric(difftime(data[1,1], init,units="days")))+1, trunc(as.numeric(difftime(data[nrow(data),1], init,units="days")))+1, by=1 ), par("usr")[1]-0.1, labels = days_vector, srt = 0, pos = 2, xpd = TRUE)
axis(2, labels=FALSE)

#Modality

colors <- c("blue", "black", "green", "yellow")
modality[,1] <- as.POSIXct(trunc(modality[,1]),origin="1970-01-01",tz="America/Sao_Paulo")
data = modality
previous_time = 0
previous_day = 0
flag = 0
for (i in 2:nrow(data)-1){
    day = trunc(as.numeric(difftime(data[i,1], init,units="days")))+1
    next_day = trunc(as.numeric(difftime(data[i+1,1], init,units="days")))+1

    time = as.numeric(difftime(data[i,1], init,units="hours"))%%24


    if(flag == 0){
      previous_time  = as.numeric(difftime(data[i,1], init,units="hours"))%%24
      flag = 1
    }
    if (data[i,2] != data[i+1,2] || day != next_day){

      lines(c(previous_time,time),c(day+.1,day+.1),col=colors[data[i,2]],pch=19,lwd=10)
      # lines(c(previous_time,time),c(day+.1,day+.1),col=data[i,2]+1,pch=19,lwd=10)
      flag = 0
    }

}




dev.off()
