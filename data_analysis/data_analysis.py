from product import Product, Nutrient
import DataCollectionFunctions
import DatabaseFunctions
import CompareProducts
import depricated_functions
import svm as svm
import logit as logit

pythonDatabaseFilename = "convertedDatabase.json"

def getLabels(database, xFilename, yFilename, pFilename, gender, age, activityLevel):
	nutrientValueDict = DataCollectionFunctions.getNutrientValueDict(database)
	nutrientRelationshipsDict = DataCollectionFunctions.readNutrientRelationships()
	recommendedValuesDict = DataCollectionFunctions.getSuggestedIntakes(gender, age, activityLevel)
	recommendedValueDeviationDict = DataCollectionFunctions.getRecommendedValueDeviationDict(nutrientValueDict, recommendedValuesDict)
	productNutrientDict = DataCollectionFunctions.getProductNutrientDict(database, nutrientRelationshipsDict, recommendedValuesDict)
	standardizedProductNutrientDict = DataCollectionFunctions.convertDataToStandardUnits(recommendedValuesDict, recommendedValueDeviationDict, productNutrientDict)
	avgNutrDevDict = DataCollectionFunctions.getAvgNutrDevDict(standardizedProductNutrientDict)
	#DataCollectionFunctions.plotPDF(avgNutrDevDict)
	DataCollectionFunctions.writeProductLabels(avgNutrDevDict, productNutrientDict, xFilename, yFilename, pFilename)
	#DataCollectionFunctions.printBestScores(productScoresDict, pythonDatabase, 2300)
	print
	
def dataCollection(databaseList, filenames, gender, age, activityLevel, pFilename = None):
	for database, filenames in zip(databaseList, filenames):
		getLabels(database, filenames[0], filenames[1], pFilename, gender, age, activityLevel)

def main():
	filenames = [["crossX.json", "crossY.json"], ["trainX.json", "trainY.json"], ["testX.json", "testY.json"]]
	
	#pythonDatabase = DatabaseFunctions.convertFromJson(DatabaseFunctions.readJSON(pythonDatabaseFilename))
	#dataCollection(DatabaseFunctions.randomSample(pythonDatabase, [1.0]), [["databaseX.json", "databaseY.json"]], "male", 22, "very active", pFilename = "productIds.json")

	# Getting Data for Training
	# [percentage of database used for cross validation, percentage of database used for training, percentage of database used for final accuracy testing]
	#databaseList = DatabaseFunctions.randomSample(pythonDatabase, [0.10, 0.70, 0.20])
	#dataCollection(databaseList, filenames, "male", 22, "very active")

	# Training Models
	#svm.trainsvm(filenames)
	#logit.trainLogisticRegression(filenames)

	# Test Models
	svm.testModel("svm.joblib", filenames[2][0], filenames[2][1])
	logit.testModel("logit.joblib", filenames[2][0], filenames[2][1])

	#model = svm.loadModel("svm.joblib")
	#databaseX, databaseY = DataCollectionFunctions.loadData("databaseX.json", "databaseY.json")
	#svmScores = svm.getScores(model, databaseX).tolist()
	#svm.saveScores(svmScores, "svmScores.json")

	#productScoresDict = CompareProducts.createProductScoresDict(CompareProducts.loadProductIds(), CompareProducts.loadScores("svmScores.json"))
	#CompareProducts.compareProducts(45001669, 45001677, productScoresDict)

if __name__ == '__main__':
	main()

	