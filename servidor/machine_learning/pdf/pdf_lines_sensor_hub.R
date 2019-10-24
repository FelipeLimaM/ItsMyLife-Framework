#!/usr/bin/env Rscript

getdata <- function(args) {
  if (grepl(".zip", args[1])){
      data <- read.csv(unz(args[1], args[2]), header=TRUE, sep=",")
  } else {
      data <- read.csv(file=args[1], header=TRUE, sep=",")
  }
  return(data)
}

getoutput <- function(args) {
  if (grepl(".zip", args[1])){
      output = args[3]
  } else {
      output = args[2]
  }
  return(output)
}

convert <- function(data){
  if(data == 32){ #Vehicle
    return(4)
  }
  if(data == 16){#Running
    return(3)
  }
  if(data == 8){#Walking
    return(2)
  }
  if(data == 1){#Stopped
    return(1)
  }
}


args = commandArgs(trailingOnly=TRUE)

data = 0

if (length(args)<2){
  exit
}
# Getting file
output <- getoutput(args)
data <- getdata(args)

# line size
cex <- 0.5

# converting timestamp unix in date
data$timestamp <- as.POSIXct(trunc(data[,1]),origin="1970-01-01",tz="America/Sao_Paulo")

pdf(output,width=30, height=10)
mar.default <- c(5,5,5,1) + 0.1
par(mar = mar.default + c(0,4,0,0))

#creating color range (it's Sensor hub problem)
mycolors <- c("grey","green","gold","blue")

#
init = as.POSIXct(trunc(data[1,1], "days"),origin="1970-01-01")


# building initial Plot
plot(data[1,1],1,xlab='Time',xlim=c(0,24),ylim=c(trunc(as.numeric(difftime(data[1,1], init,units="days"))),trunc(as.numeric(difftime(data[nrow(data),1], init,units="days")))+2),ylab='',
  col=mycolors[convert(data[1,2])],pch=19,cex=cex,xaxt="n",yaxt="n")

previous_time = 0
previous_day = 0
flag = 0
#days_vector = c(format(init, format="%B %d %Y"))


count_days = trunc(as.numeric(difftime(data[nrow(data),1], init,units="days")))+1

current_day <- c(1)
current_color <- c(mycolors[convert(data[2,2])])
X <- c(current_day)
Y <- c(as.numeric(difftime(data[2,1], init,units="hours"))%%24) # TIME
C <- c(current_color)

# Vector that keep the date label list
days_vector = c(format(data[2,1], format="%A"))

# Loop for each line in csv
for (i in 2:nrow(data)){

  # get id date
  day <- trunc(as.numeric(difftime(data[i,1], init,units="days")))+1
  # get time of day
  time <- c(as.numeric(difftime(data[i,1], init,units="hours"))%%24)

  # get color
  # modification in code because it's battery problem
  color <- mycolors[convert(data[i,2])]

  # break line of day
  if (day != current_day){
    days_vector <- c(days_vector, format(data[i,1], format="%A") )

    #End a line
    X <- c(X, current_day)
    Y <- c(Y, 24) # TIME
    C <- c(C, current_color)
    current_day = day

    # plot line
    lines(Y,X,col=C,pch=19,lwd=10)

    #Start a new line
    X <- c(current_day)
    Y <- c(0) # TIME
    C <- c(current_color)
  }
    if(color != current_color){
      #End a line
      X <- c(X, current_day)
      Y <- c(Y, time-0.00000000001) # TIME
      current_color <- color

      # plot line
      lines(Y,X,col=C,pch=19,lwd=10)

      #Start a new line
      X <- c(current_day)
      Y <- c(time) # TIME
      C <- c(current_color)
    }


}
#End a line
X <- c(X, trunc(as.numeric(difftime(data[nrow(data),1], init,units="days")))+1)
Y <- c(Y, c(as.numeric(difftime(data[nrow(data),1], init,units="hours"))%%24))
lines(Y,X,col=C,pch=19,lwd=10)


x_labels <- c()
for (i in 0:24){
  x_labels <- c(x_labels, paste(formatC(i,width=2,flag="0"),":00H",sep=""))
}

axis(1, at=0:24, label=x_labels)
#text(x = seq(0,24, by=1 ), par("usr")[1]-0.1, labels = x_labels, srt = 0, pos = 1, xpd = TRUE)
text(y = seq(trunc(as.numeric(difftime(data[1,1], init,units="days")))+1, trunc(as.numeric(difftime(data[nrow(data),1], init,units="days")))+1, by=1 ), par("usr")[1]-0.1, labels = days_vector, srt = 0, pos = 2, xpd = TRUE)
axis(2, labels=FALSE)
dev.off()
