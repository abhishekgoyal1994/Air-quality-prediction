from sklearn import svm
from sklearn import tree
import csv
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from copy import deepcopy
import numpy as np

listOfFeatureVector = []
listOfFeatureVectorFloat = []
listOfY = []
listOfYFloat = []


featureFields = ['row_id','weekday','hour','solar_radiation','wind_speed','max_temp','min_temp','pressure','min_pressure','max_pressure','pollutants']
featureFieldsNew = ['row_id','weekday','hour','solar_radiation','wind_speed','max_temp','min_temp','pressure','min_pressure','max_pressure','prevPollutants','pollutants']


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
                if field!="pollutants" and field!="row_id" and field!="weekday":
                    featureList.append(row[field])
                elif field=="pollutants":
                    listOfY.append(row['pollutants'])
        if count==2:
            featureList.append(row['pollutants'])
        else:
            featureList.append(listOfY[len(listOfY)-2])
        listOfFeatureVector.append(featureList)
    featureFile.close()

def calculateMSE(actualY,predictedY):
    numFloat = 0.0
    yp = 0
    ya = 0
    for i in range(len(predictedY)):
        #get the nearest integer
        yp = float(predictedY[i])
        ya = float(actualY[i])
        numFloat += (yp - ya)*(yp - ya)

    print "value of MSE is " + str(numFloat/len(predictedY))

def calculateMAE(actualY,predictedY):

    numFloat = 0.0
    yp = 0
    ya = 0
    for i in range(len(predictedY)):
        #get the nearest integer
        yp = float(predictedY[i])
        ya = float(actualY[i])
        print yp, ya
        numFloat += abs(yp - ya)
    temp = numFloat/len(predictedY)
    print "value of MAE is " + str(temp)
    return temp

def calculateR2(actualY,predictedY):
    actualYSum = 0
    for y in actualY:
        actualYSum += int(y)
    actualYAverage = (float(actualYSum))/len(actualY)
    #numerator calculation
    numFloat = 0.0
    denomFloat = 0.0
    for y in predictedY:
        #get the nearest integer
        y = int(round(float(y)))
        numFloat += (y - actualYAverage)*(y-actualYAverage)
    #denominator calculation
    for y in actualY:
        denomFloat += (int(y) - actualYAverage)*(int(y)-actualYAverage)
    print "value of R2 is " + str(numFloat/denomFloat)


def ANN():
    actualY = []
    min_val = 100.00
    rs_val = 0
    l = (0,0,0) 
    listOfFeatureVectorFloat = deepcopy(listOfFeatureVector)
    listOfYFloat = deepcopy(listOfY)
    print "apply ANN"
    '''
    for rs in range(100,110):
        #clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=rs)
        for l1 in range(13,18):
            for l2 in range(13,18):
                for l3 in range(13,18):
                    print l1,l2,l3
                    #clf = MLPRegressor(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(l,np.random.randint(10,20),np.random.randint(10,20),), random_state=rs)
                    clf = MLPRegressor(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(l1,l2,l3,), random_state=rs)
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
                    MAE = calculateMAE(actualY,predictedYs)
                    if (min_val > MAE):
                        for i in range(len(predictedYs)):
                            #get the nearest integer
                            yp = float(predictedYs[i])
                            ya = float(actualY[i])
                            print yp, ya
                        min_val = MAE
                        rs_val = rs
                        l = (l1,l2,l3)
    print min_val , rs_val, l'''

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
    MAE = calculateMAE(actualY,predictedYs)


def trainAndGetResults():
    actualY = []
    ANN()
    #clf = svm.SVR(C=10)
    clf = tree.DecisionTreeRegressor(random_state=0)
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
    calculateMAE(actualY,predictedYs)


if __name__=="__main__":
    getListOfFeatureVectors()
    trainAndGetResults()
