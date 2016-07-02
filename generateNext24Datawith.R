library(forecast)
library(Metrics)
library(plyr)

data = read.csv('data/Training_Data_Refined_192_hours.csv')

minpress = data$min_pressure[1:168]
mintemp = data$min_temp[1:168]
maxpress = data$max_pressure[1:168]
maxtemp = data$max_temp[1:168]
sradiation = data$solar_radiation[1:168]
wspeed = data$wind_speed[1:168]
pressure = data$pressure[1:168]

topredict = list(minpress,mintemp,maxpress,maxtemp,sradiation,wspeed,pressure)
xorder = list(c(1,3,1),c(1,3,2),c(1,2,2),c(3,2,3),c(0,0,0),c(3,0,3),c(1,2,1))
yorder = list(c(3,2,3),c(3,3,3),c(3,3,1),c(1,1,1),c(3,1,2),c(3,1,1),c(3,2,2))

predicted = list()

for (i in 1:length(topredict)){
	arma <- arima0(as.numeric(unlist(topredict[i])),as.numeric(unlist(xorder[i])),list(order=as.numeric(unlist(yorder[i])),period=24))
	predicted[[i]] <- predict(arma,24)$pred
}

#values that we don't have to predict
rowid = data$row_id[169:192]
weekday = data$weekday[169:192]
hour = data$hour[169:192]
pollutants = data$pollutants[169:192]
# Now write these predicted values to a new file
featureVector = vector('character')

allPollutants = vector('double')
allPollutants = c(allPollutants,data$pollutants[168:168][[1]])
for (i in 1:23){
	allPollutants = c(allPollutants,-1)
}

for (i in 1:24){
	featureVector = c(featureVector,c(toString(rowid[i]),toString(weekday[i]),toString(hour[i]),toString(predicted[[5]][[i]])
		,toString(predicted[[6]][[i]]),toString(predicted[[4]][[i]]),toString(predicted[[2]][[i]]),toString(predicted[[7]][[i]]),
		toString(predicted[[1]][[i]]),toString(predicted[[3]][[i]]),toString(allPollutants[[i]]),toString(pollutants[[i]])))
}
writeMatrix = matrix(featureVector,ncol=24,nrow=12)
write.table(t(writeMatrix),file="data/generatedwith.csv",sep=",",row.names=FALSE)
