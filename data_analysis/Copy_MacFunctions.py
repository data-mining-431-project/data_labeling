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
			nutrientValueList.append(product.nutrients[nutrientID].value)
		nutrientValueDict[nutrientID] = nutrientValueList

	return nutrientValueDict

def readNutrientRelationships(filename):
	# Read in the nutrient relationship data
	# assemble into a dictionary of the form
	# nutrientID : flag
	# where the flag is a string "normal", "tooLittleBad", "tooMuchBad"

	nutrientRelationshipsDict = dict()
	NutrientRelationshipFilename = "NutrientRelationshipFile.txt"

	for nutrientID in nutrientRelationshipsDict.keys()

	f = open(NutrientRelationshipFilename,"r") #opens file with name of "test.txt"
	myList = []
	for line in f:
    	myList.append(line)
		print(myList)
	f.close()

	return nutrientRelationshipsDict

def getSuggestedIntakes():
	# Zurui
	# adjustedIdealValue = (idealValue/day) * 1/(suggestedCaloricIntake/day)
	# process into a dictionary of the form
	# nutrinetID : adjustedIdealValue

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

def getProductNutrientDict(pythonDatabase, nutrientRelationshipsDict, idealValuesDict):
	# productNutrientDict dict of form
	# productID : nutrientDict
	# where nutrientDict is a dictionary of form
	# nutrientID : adjustedNutrientValue
	# where adjustedNutrientValue depends on if-else block

	productNutrientDict = dict()

	for productID, product in pythonDatabase.items():
		nutrientDict = dict()
		for nutrientID, nutrientValue in product.nutrients.items():
			nutrientDict[nutrientID] = nutrientValue/product.nutrients[208]
			if nutrientRelationshipsDict[nutrientID] == "lessThanBad" and nutrientDict[nutrientID] > idealValuesDict[nutrientID]:
				nutrientDict[nutrientID] = idealValuesDict[nutrientID]
			elif nutrientRelationshipsDict[nutrientID] == "moreThanBad" and nutrientDict[nutrientID] < idealValuesDict[nutrientID]:
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
	json.dump(obj, f)