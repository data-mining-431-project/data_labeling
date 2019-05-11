from product import Product, Nutrient
import DataCollectionFunctions
import DatabaseFunctions

pythonDatabaseFilename = "nutrition_database.json"
nutrientCodesFilename = "nutrient_codes.txt"

def main():
	pythonDatabase = DatabaseFunctions.convertFromJson(DatabaseFunctions.readJSON(pythonDatabaseFilename))
	nutrientCodes = DatabaseFunctions.getNutrientCodesList(nutrientCodesFilename)
	
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

if __name__ == '__main__':
	main()