from product import Product, Nutrient
import DataCollectionFunctions
import DatabaseFunctions

pythonDatabaseFilename = "nutrition_database.json"
nutrientCodesFilename = "nutrient_codes.txt"

def dataCollection(pythonDatabase, nutrientCodes):
	nutrientValueDict = DataCollectionFunctions.getNutrientValueDict(pythonDatabase)

	nutrientRelationshipsDict = DataCollectionFunctions.readNutrientRelationships("")

	idealValuesDict = DataCollectionFunctions.getSuggestedIntakes("male", 22, "very active")

	idealValueDeviationDict = DataCollectionFunctions.getIdealValueDeviationDict(nutrientValueDict, idealValuesDict)

	productNutrientDict = DataCollectionFunctions.getProductNutrientDict(pythonDatabase, nutrientRelationshipsDict, idealValuesDict)

	standardizedProductNutrientDict = DataCollectionFunctions.convertDataToStandardUnits(idealValuesDict, idealValueDeviationDict, productNutrientDict)

	productScoresDict = DataCollectionFunctions.getProductScores(standardizedProductNutrientDict)

	DataCollectionFunctions.writeProductScores(productScoresDict, standardizedProductNutrientDict)

	DataCollectionFunctions.printBestScores(productScoresDict, pythonDatabase)

	X, Y = DataCollectionFunctions.loadSvmData()

	for i in range(10):
		print str(Y[i]) + ": " + str(X[i])

def main():
	pythonDatabase = DatabaseFunctions.convertFromJson(DatabaseFunctions.readJSON(pythonDatabaseFilename))
	pythonDatabase = DatabaseFunctions.randomSample(pythonDatabase, 0.01)
	nutrientCodes = DatabaseFunctions.getNutrientCodesList(nutrientCodesFilename)
	
	DatabaseFunctions.performUnitConversionsOnDatabase(pythonDatabase)

	pythonDatabase = DatabaseFunctions.convertFromJson(DatabaseFunctions.readJSON("convertedDatabase.json"))

	dataCollection(pythonDatabase, nutrientCodes)

if __name__ == '__main__':
	main()