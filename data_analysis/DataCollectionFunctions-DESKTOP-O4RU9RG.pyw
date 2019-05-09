# -*- coding: utf-8 -*-

from product import Product, Nutrient
import json
import math
import DatabaseFunctions

def getNutrientValueDict(pythonDatabase, nutrientCodes):
	# assembles a dictionary from the python_database in the form
	# nutrientID : listOfAllNutrientValues

	nutrientValueDict = dict()

	for nutrientID in nutrientCodes:
		nutrientValueList = []
		for productID, product in pythonDatabase.items():
			try:
				nutrientValueList.append(product.nutrients[nutrientID].value)
			except:
				nutrientValueList.append(0.0)
		nutrientValueDict[nutrientID] = nutrientValueList

	return nutrientValueDict

def readNutrientRelationships(filename, nutrientCodes):
	# Read in the nutrient relationship data
	# assemble into a dictionary of the form
	# nutrientID : flag
	# where the flag is a string "normal", "notepad
	# ", "tooMuchBad"
	nutrientRelationshipsDict = dict()
	for code in nutrientCodes:
		nutrientRelationshipsDict[code] = "normal"

	return nutrientRelationshipsDict

def getSuggestedIntakes(nutrientCodes):
	# Zurui
	# adjustedIdealValue = (idealValue/day) * 1/(suggestedCaloricIntake/day)
	# process into a dictionary of the form
	# nutrinetID : adjustedIdealValue
	
	idealValuesDict = dict()
	refIntakes = pd.read_csv('Dietary_Reference_Intakes.csv')
	for n in range(1,18):
		for nutrient in refIntakes:
			idealIntake = refIntakes[nutr][n]/refIntakes[Calories][n]
			for nutrientID in nutrientCodes:
				if nutrient in nutrientCodes:
					nID = nutrientCodes[n] 
					idealValuesDict[nID] = idealIntake

	return idealValuesDict

def idealValueDeviation(nutrientValueDict, idealValuesDict):
	# Calculate the deviation from the ideal value: sigma
	# Calculate deviation for all values and return a dict of the form
	# nutrientID : idealValueDeviation

	idealValueDeviationDict = dict()

	for nutrientID in idealValuesDict.keys():
		squaredSum = 0
		for nutrientValue in nutrientValueDict[nutrientID]:
			squaredSum+=(nutrientValue-idealValuesDict[nutrientID])^2
		idealValueDeviationDict[nutrientID] = math.sqrt(squaredSum/len(nutrientValueDict[nutrientID]))

	return idealValueDeviationDict

def getProductNutrientDict(pythonDatabase, nutrientCodes, nutrientRelationshipsDict, idealValuesDict):
	# productNutrientDict dict of form
	# productID : nutrientDict
	# where nutrientDict is a dictionary of form
	# nutrientID : adjustedNutrientValue
	# where adjustedNutrientValue depends on if-else block

	productNutrientDict = dict()

	for productID, product in pythonDatabase.items():
		nutrientDict = dict()
		for nutrientID in nutrientRelationshipsDict.keys():
			try:
				nutrientDict[nutrientID] = product.nutrients[nutrientID].value/product.nutrients[208]
			except:
				nutrientDict[nutrientID] = 0.0
			if nutrientRelationshipsDict[nutrientID] == "tooMuchBad" and nutrientDict[nutrientID] > idealValuesDict[nutrientID]:
				nutrientDict[nutrientID] = idealValuesDict[nutrientID]
			elif nutrientRelationshipsDict[nutrientID] == "tooLittleBad" and nutrientDict[nutrientID] < idealValuesDict[nutrientID]:
				nutrientDict[nutrientID] = idealValuesDict[nutrientID]

	return productNutrientDict

def convertDataToStandardUnits(idealValuesDict, idealValueDeviationDict, productNutrientDict):
	# convert data into standard units
	# (x-iv)/ivDev

	for productID, nutrientDict in productNutrientDict.items():
		for nutrientID, nutrientValue in nutrientDict.items():
			nutrientValue = (nutrientValue - idealValuesDict[nutrientID])/idealValueDeviationDict[nutrientID]

	return productNutrientDict

def getProductScores(productNutrientDict):
	productScoresDict = dict()
	for productID, nutrientDict in productNutrientDict.items():
		score = 0
		for nutrientID, nutrientValue in nutrientDict.items():
			score += nutrientValue
		productScoresDict[productID] = score

	return productScoresDict

def writeProductScores(productScoresDict):
	# write a json file with format:
	# 0, productID
	# 1, productID
	# where 0 means a bad score and 1 means a good score
	
	labeledData = dict()
	labeledDataFilename = "labeledData.data"

	for productID, score in productScoresDict.items():
		if score >= 0:
			labeledData[productID] = 1
		else:
			labeledData[productID] = 0

	f = open(labeledDataFilename, 'w+')
	json.dump(labeledData, f)