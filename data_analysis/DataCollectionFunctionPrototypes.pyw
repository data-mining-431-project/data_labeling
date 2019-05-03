def getNutrientValueDict(python_database):
	# assembles a dictionary from the python_database in the form
	# nutrientID : listOfAllNutrientValues
	return nutrientValueDict

def readNutrientRelationships(filename):
	# Read in the nutrient relationship data
	# assemble into a dictionary of the form
	# nutrientID : flag
	# where the flag is a string "normal", "tooLittleBad", "tooMuchBad"
	return nutrientRelationshipsDict

def getSuggestedIntakes():
	# Zurui
	# adjustedIdealValue = (idealValue/day) * 1/(suggestedCaloricIntake/day)
	# process into a dictionary of the form
	# nutrinetID : adjustedIdealValue
	return idealValuesDict

def idealValueDeviation(nutrientValueDict, idealValuesDict):
	# Calculate the deviation from the ideal value
	# Calculate deviation for all values and return a dict of the form
	# nutrientID : idealValueDeviation
	return idealValueDeviationDict

def getProductNutrientDict(pythonDatabase, nutrientRelationshipsDict, idealValuesDict):
	# productNutrientsDict dict of form
	# productID : nutrientDict
	# where nutrientDict is a dictionary of form
	# nutrientID : adjustedNutrientValue
	# where adjustedNutrientValue depends on if-else block
	# tentative code below assumes adjustedNutrientValue = nutrientValue/calories has already been done

	for nutrientID, nutrientValue in nutrientDict:
		if nutrientRelationshipsDict[nutrientID] == "lessThanBad":
			if nutrientValue > idealValuesDict[nutrientID]:
				nutrientValue = idealValuesDict[nutrientID]
		elif nutrientRelationshipsDict[nutrientID] == "moreThanBad" and nutrientValue:
			if nutrientValue < idealValuesDict[nutrientID]:
				nutrientValue = idealValuesDict[nutrientID]
		else:
			adjustedNutrientValue = nutrientValue/calories
	return productNutrientDict

def convertDataToStandardUnits(idealValuesDict, idealValueDeviationDict, productNutrientDict):
	# convert data into standard units
	# Add in accounting for nutrientRelationships
	# normal - do nothing

	for productID, nutrientDict in productNutrientDict:
		for nutrientID, nutrientValue in nutrientDict:
			nutrientValue = (nutrientValue - idealValuesDict[nutrientID])/idealValueDeviationDict[nutrientID]

	return productNutrientDict

def getProductScores(productNutrientDict):
	productScoresDict = dict()
	for productID, nutrientDict in productNutrientDict:
		score = 0
		for nutrientID, nutrientValue in nutrientDict:
			score += nutrientValue
		productScoresDict[productID] = score

	return productScoresDict

def writeProductScores(productScoresDict):
	# write a json file with format:
	# 0, productID
	# 1, productID
	# where 0 means a bad score and 1 means a good score
	pass