from product import Product, Nutrient
import DataCollectionFunctions
import DatabaseFunctions
import depricated_functions

pythonDatabaseFilename = "nutrition_database.json"
nutrientCodesFilename = "nutrient_codes.txt"
	
def dataCollection(pythonDatabase, nutrientCodes):
	nutrientValueDict = DataCollectionFunctions.getNutrientValueDict(pythonDatabase)

	nutrientRelationshipsDict = DataCollectionFunctions.readNutrientRelationships()

	idealValuesDict = DataCollectionFunctions.getSuggestedIntakes("male", 22, "very active")

	idealValueDeviationDict = DataCollectionFunctions.getIdealValueDeviationDict(nutrientValueDict, idealValuesDict)

	productNutrientDict = DataCollectionFunctions.getProductNutrientDict(pythonDatabase, nutrientRelationshipsDict, idealValuesDict)

	standardizedProductNutrientDict = DataCollectionFunctions.convertDataToStandardUnits(idealValuesDict, idealValueDeviationDict, productNutrientDict)

	productScoresDict = DataCollectionFunctions.getProductScores(standardizedProductNutrientDict)

	DataCollectionFunctions.writeProductScores(productScoresDict, standardizedProductNutrientDict)

	DataCollectionFunctions.printBestScores(productScoresDict, pythonDatabase, 2300)

	X, Y = DataCollectionFunctions.loadSvmData()

def main():
	#pythonDatabase = DatabaseFunctions.convertFromJson(DatabaseFunctions.readJSON(pythonDatabaseFilename))
	pythonDatabase = DatabaseFunctions.convertFromJson(DatabaseFunctions.readJSON("convertedDatabase.json"))
	#depricated_functions.make_nutrient_frequency_file(pythonDatabase, DatabaseFunctions.getNutrientCodesList("usedNutrientCodes.txt"))
	
	pythonDatabase = DatabaseFunctions.randomSample(pythonDatabase, 0.15)
	nutrientCodes = DatabaseFunctions.getNutrientCodesList(nutrientCodesFilename)
	
	#DatabaseFunctions.performUnitConversionsOnDatabase(pythonDatabase)

	dataCollection(pythonDatabase, nutrientCodes)



if __name__ == '__main__':
	main()

	