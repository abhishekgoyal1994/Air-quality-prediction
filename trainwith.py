from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import sklearn.feature_selection as fs
#from sklearn.neural_network import MLPClassifier
#from sklearn.neural_network import MLPRegressor
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import csv
plt.figure

listOfFeatureVector = []
listOfFeatureVectorFloat = []
listOfY = []
listOfYFloat = []

featureFields = ['row_id','weekday','hour','solar_radiation','wind_speed','max_temp','min_temp','pressure','min_pressure','max_pressure','pollutants']
featureFieldsNew = ['row_id','weekday','hour','solar_radiation','wind_speed','max_temp','min_temp','pressure','min_pressure','max_pressure','prevPollutants','pollutants']

'''
    This function reads the training file and makes the feature vectors which will be used in fitting.
'''
def getListOfFeatureVectors():
    featureFile = open("data/Training_Data_Refined_192_hours.csv","rb")
    reader = csv.DictReader(featureFile,fieldnames=featureFields)
    featureList = []
    count = 0
    for row in reader:
        count += 1
        if count==1:
            continue
        if count==170:
            break
        featureList = []
        for field in featureFields:
                if field!="pollutants" and field!="row_id" and field!="weekday" and field!="solar_radiation" and field!="max_pressure":
                    featureList.append(float(row[field]))
                elif field=="pollutants":
                    listOfY.append(float(row['pollutants']))
        if count==2:
            featureList.append(float(row['pollutants']))
        else:
            featureList.append(listOfY[len(listOfY)-2])
        listOfFeatureVector.append(featureList)
    featureFile.close()

'''
    Draws the graph of acutal and predicted values and saves it in the current directory
    param: actualY
        - The actual values of pollutants.
    param: predictedY
        - The predicted values of pollutants.
    param name
        - The graph will be stored as name in current directory
'''
def drawGraph(actualY,predictedY,name):
    #create data
    xSeries = []
    for i in range(1,25):
        xSeries.append(i)
     
    #plot data
    plt.plot(xSeries,actualY,label="Actual pollutants value")
    plt.plot(xSeries,predictedY,label="Predicted pollutants value")
     
    #add in labels and title
    plt.xlabel("Hour")
    plt.ylabel("Pollutant Levels")
    plt.title("Comparison between actual and predicted values") 
    
    plt.legend(loc="upper left")
     
    plt.savefig(name)

def draw(listData):
    xSeries = []
    for i in range(0,48):
        xSeries.append(i)
     
    #plot data
    plt.plot(xSeries,listData)
     
    #add in labels and title
    plt.xlabel("Hour")
    plt.ylabel("Solar radiation")
    plt.title("Seasonal Trend of solar radiation for 2 days") 
     
    plt.savefig("sr.png")    

'''
    Calculates the mean absolute error between acutal and predicted values of pollutants.
    param: actualY
        - The actual values of pollutants.
    param: predictedY
        - The predicted values of pollutants.
'''
def calculateMAE(actualY,predictedY,nameOfGraphFile):
    drawGraph(actualY,predictedY,nameOfGraphFile)
    numFloat = 0.0
    yp = 0
    ya = 0
    for i in range(len(predictedY)):
        #get the nearest integer
        yp = float(predictedY[i])
        ya = float(actualY[i])
        #print yp,ya
        numFloat += abs(yp - ya)

    ans = numFloat/len(predictedY)
    print "value of MAE is " + str(ans)

'''
    ANN Model
'''
def applyANN():
    actualY = []
    min_val = 100.00
    rs_val = 0
    l = (0,0,0) 
    listOfFeatureVectorFloat = deepcopy(listOfFeatureVector)
    listOfYFloat = deepcopy(listOfY)
    clf = MLPRegressor(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(13,13,13,), random_state=99)
    #temp1 = np.array(listOfFeatureVectorFloat)
    #temp2 = np.array(listOfYFloat)
    temp2 = deepcopy(listOfYFloat)
    temp1 = deepcopy(listOfFeatureVectorFloat)
    for i in range(len(temp2)):
        temp2[i] = float(temp2[i])
    for i in range(len(temp1)):
        for j in range(len(temp1[i])):
            temp1[i][j] = float(temp1[i][j])
    clf.fit(temp1, temp2)
    testFile = open("data/generatedwith.csv","rb")
    reader = csv.DictReader(testFile,fieldnames=featureFieldsNew)
    featureList = []
    testFeatureVector = []
    predictedYs=[]
    count=0
    for row in reader:
        count+=1
        if count==1:
            continue
        featureList = []
        if count==2:
            for field in featureFieldsNew:
                if field!="pollutants" and field!="row_id" and field!="weekday":
                    featureList.append(float(row[field]))
                elif field=="pollutants":
                    actualY.append(row[field])
        else:
            predictedY = clf.predict(testFeatureVector)
            predictedYs.append(predictedY[0])
            for field in featureFieldsNew:
                if field!="pollutants" and field!="prevPollutants" and field!="row_id" and field!="weekday":
                    featureList.append(float(row[field]))
                elif field=="prevPollutants":
                    featureList.append(float(predictedY[0]))
                elif field=="pollutants":
                    actualY.append(row[field])
            testFeatureVector = []
        testFeatureVector.append(featureList)
    predictedY = clf.predict(testFeatureVector)
    predictedYs.append(predictedY[0])
    testFile.close()
    #store all the predicted y in txt file
    f = open("data/predictedwith.txt","w")
    f.write(str(predictedYs))
    f.close()
    # now calculate R2 value
    #calculateR2(actualY,predictedY)
    calculateMAE(actualY,predictedYs,"ann.png")

'''
    Random Forest
'''
def applyRandomForest():
    actualY = []
    clf = RandomForestClassifier(n_estimators=6,random_state=269)
    testFeatureVector = []
    predictedYs=[]
    clf.fit(listOfFeatureVector,listOfY)
    testFile = open("data/generatedwith.csv","rb")
    reader = csv.DictReader(testFile,fieldnames=featureFieldsNew)
    featureList = []
    count=0
    for row in reader:
        count+=1
        if count==1:
            continue
        featureList = []
        if count==2:
            for field in featureFieldsNew:
                if field!="pollutants" and field!="row_id" and field!="weekday":
                    featureList.append(float(row[field]))
                elif field=="pollutants":
                    actualY.append(float(row[field]))
        else:
            predictedY = clf.predict(testFeatureVector)
            predictedYs.append(predictedY[0])
            for field in featureFieldsNew:
                if field!="pollutants" and field!="prevPollutants" and field!="row_id" and field!="weekday":
                    featureList.append(float(row[field]))
                elif field=="prevPollutants":
                    featureList.append(float(predictedY[0]))
                elif field=="pollutants":
                    actualY.append(float(row[field]))
            testFeatureVector = []
        testFeatureVector.append(featureList)
    predictedY = clf.predict(testFeatureVector)
    predictedYs.append(float(predictedY[0]))
    testFile.close()
    #store all the predicted y in txt file
    f = open("data/predictedwith.txt","w")
    f.write(str(predictedYs))
    f.close()
    # now calculate R2 value
    #calculateR2(actualY,predictedY)
    calculateMAE(actualY,predictedYs,"randomforest.png")    

'''
    Regression Trees
'''
def applyRegressionTrees():
    actualY = []
    clf = tree.DecisionTreeRegressor(random_state=9166)
    testFeatureVector = []
    predictedYs=[]
    clf.fit(listOfFeatureVector,listOfY)
    testFile = open("data/generatedwith.csv","rb")
    reader = csv.DictReader(testFile,fieldnames=featureFieldsNew)
    featureList = []
    count=0
    for row in reader:
        count+=1
        if count==1:
            continue
        featureList = []
        if count==2:
            for field in featureFieldsNew:
                if field!="pollutants" and field!="row_id" and field!="weekday":
                    featureList.append(float(row[field]))
                elif field=="pollutants":
                    actualY.append(float(row[field]))
        else:
            predictedY = clf.predict(testFeatureVector)
            predictedYs.append(predictedY[0])
            for field in featureFieldsNew:
                if field!="pollutants" and field!="prevPollutants" and field!="row_id" and field!="weekday":
                    featureList.append(float(row[field]))
                elif field=="prevPollutants":
                    featureList.append(float(predictedY[0]))
                elif field=="pollutants":
                    actualY.append(float(row[field]))
            testFeatureVector = []
        testFeatureVector.append(featureList)
    predictedY = clf.predict(testFeatureVector)
    predictedYs.append(float(predictedY[0]))
    testFile.close()
    #store all the predicted y in txt file
    f = open("data/predictedwith.txt","w")
    f.write(str(predictedYs))
    f.close()
    # now calculate R2 value
    #calculateR2(actualY,predictedY)
    calculateMAE(actualY,predictedYs,"regressiontrees.png")

'''
    SVM model
'''
def applySVM():
    actualY = []
    clf = svm.SVR(C=0.1)
    testFeatureVector = []
    predictedYs=[]
    clf.fit(listOfFeatureVector,listOfY)
    testFile = open("data/generatedwith.csv","rb")
    reader = csv.DictReader(testFile,fieldnames=featureFieldsNew)
    featureList = []
    count=0
    for row in reader:
        count+=1
        if count==1:
            continue
        featureList = []
        if count==2:
            for field in featureFieldsNew:
                if field!="pollutants" and field!="row_id" and field!="weekday"  and field!="solar_radiation" and field!="max_pressure":
                    featureList.append(float(row[field]))
                elif field=="pollutants":
                    actualY.append(float(row[field]))
        else:
            predictedY = clf.predict(testFeatureVector)
            predictedYs.append(predictedY[0])
            for field in featureFieldsNew:
                if field!="pollutants" and field!="prevPollutants" and field!="row_id" and field!="weekday"  and field!="solar_radiation" and field!="max_pressure":
                    featureList.append(float(row[field]))
                elif field=="prevPollutants":
                    featureList.append(float(predictedY[0]))
                elif field=="pollutants":
                    actualY.append(float(row[field]))
            testFeatureVector = []
        testFeatureVector.append(featureList)
    predictedY = clf.predict(testFeatureVector)
    predictedYs.append(float(predictedY[0]))
    testFile.close()
    #store all the predicted y in txt file
    f = open("data/predictedwith.txt","w")
    f.write(str(predictedYs))
    f.close()
    # now calculate R2 value
    #calculateR2(actualY,predictedY)
    calculateMAE(actualY,predictedYs,"svm.png")

'''
    This function calls the appropriate machine learning model
'''
def trainAndGetResults():
    #uncomment any of these to apply that model
    #applyANN()
    applySVM()
    #applyRegressionTrees()
    #applyRandomForest()
    #reg = fs.SelectKBest(fs.f_regression, k='all')
    #reg.fit_transform(listOfFeatureVector, listOfY)
    #print reg.scores_

'''
    MAIN
'''
if __name__=="__main__":
    draw(['0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.05',
'0.19',
'0.58',
'0.74',
'0.92',
'0.99',
'0.97',
'0.87',
'0.7',
'0.46',
'0.21',
'0.02',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.05',
'0.31',
'0.58',
'0.79',
'0.93',
'1',
'0.98',
'0.88',
'0.7',
'0.46',
'0.21',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01',
'0.01'])
    #getListOfFeatureVectors()
    #trainAndGetResults()
