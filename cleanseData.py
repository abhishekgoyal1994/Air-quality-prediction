import csv

features = {}
listTarget = []
prevrow={}

def findMissingPollutants(listData):
	sum = 0.0
	for data in listData:
		sum += float(data)
	return str(sum)

def findpollutants(listData):
	sumPollutant = 0.0
	for pollutantList in listData:
		try:
			sumPollutant += float(find(pollutantList))
		except:
			print listData
			sys.exit(0)
	return str(sumPollutant)

def findmax(listData):
	someData = False
	for x in listData:
		if x!='NA':
			someData = True
			break
	if not someData:
		return 'NA'
	mx = -1.0
	for x in listData:
		if x!= 'NA':
			mx = max(mx,float(x))
	return str(mx)

def findmin(listData):
	someData = False
	for x in listData:
		if x!='NA':
			someData = True
			break
	if not someData:
		return 'NA'
	mn = 100000000.0
	for x in listData:
		if x!= 'NA':
			mn = min(mn,float(x))
	return str(mn)

def find(listData):
	someData = False
	for x in listData:
		if x!='NA':
			someData = True
			break
	if not someData:
		return 'NA'
	sum = 0.0
	instanceCount = 0
	for x in listData:
		if x!='NA':
			sum += float(x)
			instanceCount += 1
	return str(float(sum)/instanceCount)

def refineData():
	featureFields = ["rowID","chunkID","position_within_chunk","month_most_common","weekday","hour","Solar.radiation_64","WindDirection..Resultant_1","WindDirection..Resultant_1018",
	"WindSpeed..Resultant_1","WindSpeed..Resultant_1018","Ambient.Max.Temperature_14","Ambient.Max.Temperature_22","Ambient.Max.Temperature_50","Ambient.Max.Temperature_52",
	"Ambient.Max.Temperature_57","Ambient.Max.Temperature_76","Ambient.Max.Temperature_2001","Ambient.Max.Temperature_3301","Ambient.Max.Temperature_6005",
	"Ambient.Min.Temperature_14","Ambient.Min.Temperature_22","Ambient.Min.Temperature_50","Ambient.Min.Temperature_52","Ambient.Min.Temperature_57","Ambient.Min.Temperature_76",
	"Ambient.Min.Temperature_2001","Ambient.Min.Temperature_3301","Ambient.Min.Temperature_6005","Sample.Baro.Pressure_14","Sample.Baro.Pressure_22","Sample.Baro.Pressure_50",
	"Sample.Baro.Pressure_52","Sample.Baro.Pressure_57","Sample.Baro.Pressure_76","Sample.Baro.Pressure_2001","Sample.Baro.Pressure_3301","Sample.Baro.Pressure_6005",
	"Sample.Max.Baro.Pressure_14","Sample.Max.Baro.Pressure_22","Sample.Max.Baro.Pressure_50","Sample.Max.Baro.Pressure_52","Sample.Max.Baro.Pressure_57",
	"Sample.Max.Baro.Pressure_76","Sample.Max.Baro.Pressure_2001","Sample.Max.Baro.Pressure_3301","Sample.Max.Baro.Pressure_6005","Sample.Min.Baro.Pressure_14",
	"Sample.Min.Baro.Pressure_22","Sample.Min.Baro.Pressure_50","Sample.Min.Baro.Pressure_52","Sample.Min.Baro.Pressure_57","Sample.Min.Baro.Pressure_76",
	"Sample.Min.Baro.Pressure_2001","Sample.Min.Baro.Pressure_3301","Sample.Min.Baro.Pressure_6005","target_1_57","target_10_4002","target_10_8003","target_11_1",
	"target_11_32","target_11_50","target_11_64","target_11_1003","target_11_1601","target_11_4002","target_11_8003","target_14_4002","target_14_8003","target_15_57",
	"target_2_57","target_3_1","target_3_50","target_3_57","target_3_1601","target_3_4002","target_3_6006","target_4_1","target_4_50","target_4_57","target_4_1018",
	"target_4_1601","target_4_2001","target_4_4002","target_4_4101","target_4_6006","target_4_8003","target_5_6006","target_7_57","target_8_57","target_8_4002","target_8_6004",
	"target_8_8003","target_9_4002","target_9_8003"]

	newFeatureFields = ['row_id','weekday','hour','solar_radiation','wind_speed','max_temp','min_temp','pressure','min_pressure','max_pressure','pollutants']
	featureFieldstargets = ['target_1_57']
	oiriginalTrainingFile = open("data/TrainingData.csv","rb")
	newTrainingFile = open("data/Training_Data_Refined_192_hours.csv","w")
	
	reader = csv.DictReader(oiriginalTrainingFile,fieldnames=featureFields)
	writer = csv.DictWriter(newTrainingFile,fieldnames=newFeatureFields,lineterminator='\n')

	for field in newFeatureFields:
		features[field] = field
	writer.writerow(features)
	count=0
	for row in reader:
		count += 1
		if count==1:
			continue
		if count==194:
			break
		features['row_id'] = row['rowID']

		features['weekday'] = row['weekday']

		features['hour'] = row['hour']
		
		features['solar_radiation'] = row['Solar.radiation_64']
		
		features['wind_speed'] = find([row['WindSpeed..Resultant_1'],row['WindSpeed..Resultant_1018']])
		
		features['max_temp'] = findmax([row["Ambient.Max.Temperature_14"],row["Ambient.Max.Temperature_22"],row["Ambient.Max.Temperature_50"],row["Ambient.Max.Temperature_52"]
	,row["Ambient.Max.Temperature_57"],row["Ambient.Max.Temperature_76"],row["Ambient.Max.Temperature_2001"],row["Ambient.Max.Temperature_3301"],row["Ambient.Max.Temperature_6005"]])
		
		features['min_temp'] = findmin([row["Ambient.Min.Temperature_14"],row["Ambient.Min.Temperature_22"],row["Ambient.Min.Temperature_50"],row["Ambient.Min.Temperature_52"]
	,row["Ambient.Min.Temperature_57"],row["Ambient.Min.Temperature_76"],row["Ambient.Min.Temperature_2001"],row["Ambient.Min.Temperature_3301"],row["Ambient.Min.Temperature_6005"]])
		
		features['pressure'] = find([row["Sample.Baro.Pressure_14"],row["Sample.Baro.Pressure_22"],row["Sample.Baro.Pressure_50"],
	row["Sample.Baro.Pressure_52"],row["Sample.Baro.Pressure_57"],row["Sample.Baro.Pressure_76"],row["Sample.Baro.Pressure_2001"],row["Sample.Baro.Pressure_3301"],row["Sample.Baro.Pressure_6005"]])
		
		features['min_pressure'] = findmin([row["Sample.Min.Baro.Pressure_14"],row["Sample.Min.Baro.Pressure_22"],row["Sample.Min.Baro.Pressure_50"],row["Sample.Min.Baro.Pressure_52"]
	,row["Sample.Min.Baro.Pressure_57"],row["Sample.Min.Baro.Pressure_76"],row["Sample.Min.Baro.Pressure_2001"],row["Sample.Min.Baro.Pressure_3301"],row["Sample.Min.Baro.Pressure_6005"]])
		
		features['max_pressure'] = findmax([row["Sample.Max.Baro.Pressure_14"],row["Sample.Max.Baro.Pressure_22"],row["Sample.Max.Baro.Pressure_50"],row["Sample.Max.Baro.Pressure_52"]
	,row["Sample.Max.Baro.Pressure_57"],row["Sample.Max.Baro.Pressure_76"],row["Sample.Max.Baro.Pressure_2001"],row["Sample.Max.Baro.Pressure_3301"],row["Sample.Max.Baro.Pressure_6005"]])

		if(count==2):
			for field in featureFields:
				if field[:6]=="target":
					if row[field]!="NA":
						listTarget.append(field)
						print field

		currList = []
		for feat in listTarget:
			if row[feat]=="NA":
				currList.append(prevrow[feat])
			else:
				currList.append(row[feat])
				prevrow[feat] = row[feat]

		features['pollutants'] = findMissingPollutants(currList)
		
		writer.writerow(features)

	oiriginalTrainingFile.close()
	newTrainingFile.close()

if __name__=="__main__":
	refineData()