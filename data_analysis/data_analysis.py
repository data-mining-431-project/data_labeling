from product import Product, Nutrient
import DataCollectionFunctions
import DatabaseFunctions

pythonDatabaseFilename = "nutrition_database.json"
nutrientCodesFilename = "nutrient_codes.txt"

def main():
	pythonDatabase = DatabaseFunctions.convertFromJson(DatabaseFunctions.readJSON(pythonDatabaseFilename))
	nutrientCodes = DatabaseFunctions.getNutrientCodesList(nutrientCodesFilename)
	
	nutrientValueDict = DataCollectionFunctions.getNutrientValueDict(pythonDatabase, nutrientCodes)
	nutrientRelationshipsDict = DataCollectionFunctions.readNutrientRelationships("", nutrientCodes)
	idealValuesDict = DataCollectionFunctions.getSuggestedIntakes(nutrientCodes)
	idealValueDeviationDict = DataCollectionFunctions.getIdealValueDeviationDict(nutrientValueDict, idealValuesDict)
	productNutrientDict = DataCollectionFunctions.getProductNutrientDict(pythonDatabase, nutrientRelationshipsDict, idealValuesDict)
	productNutrientDict = DataCollectionFunctions.convertDataToStandardUnits(idealValuesDict, idealValueDeviationDict, productNutrientDict)
	productScoresDict = DataCollectionFunctions.getProductScores(productNutrientDict)
	DataCollectionFunctions.writeProductScores(productScoresDict)


if __name__ == '__main__':
	main()