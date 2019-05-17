# -*- coding: utf-8 -*-

from product import Product, Nutrient
import json
import math
import DatabaseFunctions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def readUsedNutrientCodes(filename = "usedNutrientCodes.txt"):
	nutrientCodes = []
	f = open(filename)
	for line in f.readlines():
		nutrientCodes.append(int(line))
	f.close()
	return nutrientCodes

def getNutrientValueDict(pythonDatabase):
	# assembles a dictionary from the python_database in the form
	# nutrientID : listOfAllNutrientValues

	print "Assembling Nutrient Value Dictionary..."

	nutrientCodes = readUsedNutrientCodes()
	nutrientValueDict = dict()

	for nutrientID in nutrientCodes:
		nutrientValueList = []
		for productID, product in pythonDatabase.items():
			try:
				nutrientValueList.append(product.nutrients[nutrientID].value/product.nutrients[208].value)
			except:
				nutrientValueList.append(0.0)
		nutrientValueDict[nutrientID] = nutrientValueList

	print "Done"

	return nutrientValueDict

def readNutrientRelationships(filename = "NutrientRelationshipFile.txt"):
	# Read in the nutrient relationship data
	# assemble into a dictionary of the form
	# nutrientID : flag
	# where the flag is a string "normal", "notepad
	# "normal", "tooLittleBad", "tooMuchBad"

	print "Assembling Nutrient Relationships Dictionary..."

	nutrientRelationshipsDict = dict()
	nutrientCodes = readUsedNutrientCodes()

	# Placeholder
	for code in nutrientCodes:
		nutrientRelationshipsDict[code] = "normal"
	#

	print "Done"

	return nutrientRelationshipsDict

def getSuggestedIntakes(gender, age, activity):
	# Zurui
	# adjustedIdealValue = (idealValue/day) / (suggestedCaloricIntake/day)
	# process into a dictionary of the form
	# nutrinetID : adjustedIdealValue

	# Mac

	print "Assembling Ideal Values Dictionary..."

	if gender == "male":
		caloricIntakes = pd.read_csv('Recommended_Male_Caloric_Intakes.csv')
		nutrientIntakes = pd.read_csv('Recommended_Male_Nutrient_Intakes.csv')
	elif gender == "female":
		caloricIntakes = pd.read_csv('Recommended_Female_Caloric_Intakes.csv')
		nutrientIntakes = pd.read_csv('Recommended_Female_Nutrient_Intakes.csv')
	else:
		print "Error:\nIncorrect Input for parameter: Gender"

	if age > 51:
		caloricAge = 51
	else:
		caloricAge = age

	if activity == "not active":
		dailyCaloriesList = caloricIntakes.values.tolist()
		dailyCalories = dailyCaloriesList[caloricAge-2][0].split(';')[1]
	elif activity == "somewhat active":
		dailyCaloriesList = caloricIntakes.values.tolist()
		dailyCalories = dailyCaloriesList[caloricAge-2][0].split(';')[2]
	elif activity == "very active":
		dailyCaloriesList = caloricIntakes.values.tolist()
		dailyCalories = dailyCaloriesList[caloricAge-2][0].split(';')[3]
	else:
		print "Error:\nIncorrect Input for parameter: Activity Level"


	if age > 71:
		nutrientAge = 71
	else:
		nutrientAge = age

	nutrientCodes = readUsedNutrientCodes()

	dailyNutrientsList = nutrientIntakes.values.tolist()
	dailyNutrients = dailyNutrientsList[nutrientAge-2][0].split(';')

	idealValuesDict = dict()
	for i in range(len(nutrientCodes)):
		idealValuesDict[nutrientCodes[i]] = float(dailyNutrients[i])/float(dailyCalories)

	print "Done"
	
	# Zurui
	#idealValuesDict = dict()
	#refIntakes = pd.read_csv('Dietary_Reference_Intakes.csv')
	#print refIntakes
	#for n in range(1,18):
	#	for nutrient in refIntakes:
	#		idealIntake = refIntakes[nutrient][n]/refIntakes[dailyCalories][n]
	#		for nutrientID in nutrientCodes:
	#			if nutrient in nutrientCodes:
	#				nID = nutrientCodes[n] 
	#				idealValuesDict[nID] = idealIntake

	return idealValuesDict

def getIdealValueDeviationDict(nutrientValueDict, idealValuesDict):
	# Calculate the deviation from the ideal value: sigma
	# Calculate deviation for all values and return a dict of the form
	# nutrientID : idealValueDeviation

	print "Calculating and Assembling the Deviation from the Ideal Value Dictionary..."

	idealValueDeviationDict = dict()

	for nutrientID in idealValuesDict.keys():
		squaredSum = 0
		for nutrientValue in nutrientValueDict[nutrientID]:
			squaredSum+=(nutrientValue-idealValuesDict[nutrientID])**2
		idealValueDeviationDict[nutrientID] = math.sqrt(squaredSum/len(nutrientValueDict[nutrientID]))

	print "Done"

	return idealValueDeviationDict

def getProductNutrientDict(pythonDatabase, nutrientRelationshipsDict, idealValuesDict):
	# productNutrientDict dict of form
	# productID : nutrientDict
	# where nutrientDict is a dictionary of form
	# nutrientID : adjustedNutrientValue
	# where adjustedNutrientValue depends on if-else block

	print "Assembling Product-Nutrient Dictionary..."

	productNutrientDict = dict()

	for productID, product in pythonDatabase.items():
		nutrientDict = dict()
		for nutrientID in nutrientRelationshipsDict.keys():
			try:
				nutrientDict[nutrientID] = product.nutrients[nutrientID].value/product.nutrients[208].value
			except:
				nutrientDict[nutrientID] = 0.0
			if nutrientRelationshipsDict[nutrientID] == "tooMuchBad" and nutrientDict[nutrientID] > idealValuesDict[nutrientID]:
				nutrientDict[nutrientID] = idealValuesDict[nutrientID]
			elif nutrientRelationshipsDict[nutrientID] == "tooLittleBad" and nutrientDict[nutrientID] < idealValuesDict[nutrientID]:
				nutrientDict[nutrientID] = idealValuesDict[nutrientID]
		productNutrientDict[productID] = nutrientDict

	print "Done"

	return productNutrientDict

def convertDataToStandardUnits(idealValuesDict, idealValueDeviationDict, productNutrientDict):
	# convert data into standard units
	# (x-iv)/ivDev

	print "Converting to Standard Units and Assembling a Standardized Product-Nutrient Dictionary..."

	standardizedProductNutrientDict = dict()
	
	for productID, nutrientDict in productNutrientDict.items():
		newNutrientDict = dict()
		for nutrientID, nutrientValue in nutrientDict.items():
			newNutrientDict[nutrientID] = (nutrientValue - idealValuesDict[nutrientID])/idealValueDeviationDict[nutrientID]
		standardizedProductNutrientDict[productID] = newNutrientDict

	print "Done"

	return standardizedProductNutrientDict

def getProductScores(standardizedProductNutrientDict):

	print "Calculating Product Scores and Assembling Product Scores Dictionary..."

	productScoresDict = dict()
	
	for productID, nutrientDict in standardizedProductNutrientDict.items():
		score = 0
		for nutrientID, nutrientValue in nutrientDict.items():
			score += abs(nutrientValue)
		#productScoresDict[productID] = score
		productScoresDict[productID] = score/len(nutrientDict)

	print "Done"

	return productScoresDict

def getX():
	DatabaseFunctions.getNutrientCodesList()

def writeProductScores(productScoresDict, productNutrientDict, xFilename, yFilename, pFilename = None):
	# write a json file with format:
	# 0, productID
	# 1, productID
	# where 0 means a bad score and 1 means a good score

	print "Writing to SVM Files..."
	
	labeledData = dict()

	scores = sorted(productScoresDict.values())
	hyperParameter = scores[len(scores)/2]

	for productID, score in productScoresDict.items():
		if abs(score) < hyperParameter:
			labeledData[productID] = 1
		else:
			labeledData[productID] = 0

	X = []
	Y = []
	productIdList = []
	nutrientCodes = readUsedNutrientCodes()
	for productID, label in labeledData.items():
		nutrientValueList = []
		for nutrientID in nutrientCodes:
			nutrientValueList.append(productNutrientDict[productID][nutrientID])
		X.append(nutrientValueList)
		Y.append(label)
		productIdList.append(productID)
	f = open(yFilename, 'w+')
	g = open(xFilename, 'w+')
	for y in Y:
		json.dump(y, f)
		f.write('\n')
	for x in X:
		json.dump(x, g)
		g.write('\n')
	f.close()
	g.close()

	if not pFilename == None:
		h = open(pFilename, 'w+')
		for productId in productIdList:
			json.dump(productId, h)
			h.write('\n')
		h.close()

	print "Done"

def loadData(xFilename, yFilename):

	print "Loading Data..."
	f = open(yFilename)
	g = open(xFilename)
	X = []
	Y = []
	for line in g.readlines():
		X.append(json.loads(line))
	for line in f.readlines():
		Y.append(json.loads(line))
	f.close()
	g.close()
	print "Done"

	return X, Y
	# X, Y = loadSvmData()

def printBestScores(productScoresDict, pythonDatabase, numScoresToPrint = 100):
	sortedProductScoresList = []

	for productID, score in productScoresDict.items():
		sortedProductScoresList.append([productID, abs(score)])
	sortedProductScoresList = sorted(sortedProductScoresList, key=lambda product: product[1])

	for i in range(numScoresToPrint):
		try:
			print "%100s | %8d | %3.4f" % (pythonDatabase[sortedProductScoresList[i][0]].name, sortedProductScoresList[i][0], sortedProductScoresList[i][1])
		except:
			pass

def plotPDF(productScoresDict):
	df = pd.DataFrame(data=np.array(productScoresDict.values()))
	plt.figure()

	sns.set_style('darkgrid')
	sns.distplot(df,hist=False)
	plt.title("Probability Distribution")
	plt.ylabel("Probabilities")
	plt.xlabel("Scores")
	plt.xlim(0, 20)
	plt.show()
