from product import Product, Nutrient
import json
import random
import os, sys

pythonDatabaseFilename = "nutrition_database.json"
nutrientCodesFilename = "nutrient_codes.txt"

# Writes a list of Objects to a File in JSON format
def writeJSON(objList, fileName, flagAppend = False):
	print "Writing to File"
	items_processed = 0.0
	total_items = len(objList)
	if flagAppend == False:
		f = open(fileName, 'w+')
	else:
		f = open(fileName, 'a+')
	for obj in objList:
		json.dump(obj, f)
		f.write('\n')
		# Progress Indicator
		items_processed = items_processed + 1
		progress_percent = (items_processed/total_items)*100.0
		if items_processed%10000 == 0:
			print ("%05.2f%%" % progress_percent)
	print "Done\n"
	f.close()

# Reads JSON strings from a File and returns a List of Objects that the JSON strings represented
def readJSON(fileName):
	print "Loading JSON Database File..."
	f = open(fileName, 'r+')
	objList = []
	for line in f.readlines():
		objList.append(json.loads(line))
	f.close()
	print "Done\n"
	return objList

def convertToJson(python_database):
	print "Converting to JSON..."
	items_processed = 0.0
	total_items = len(python_database.values())
	json_database = []
	products = python_database.values()
	for i in range(len(products)):
		json_database.append(products[i].convert_to_json())
		# Progress Indicator
		items_processed = items_processed + 1
		progress_percent = (items_processed/total_items)*100.0
		if items_processed%10000 == 0:
			print ("%05.2f%%" % progress_percent)
	print "Done\n"
	return json_database

def convertFromJson(json_database):
	print "Converting from JSON..."
	python_database = dict()
	items_processed = 0.0
	total_items = len(json_database)
	for i in range(total_items):
		product = json_database[i]
		id = product[0]
		python_database[id] = Product(None, True)
		python_database[id].id = product[0]

		python_nutrients_list = []
		json_nutrients_list = product[1]
		for json_nutrient in json_nutrients_list:
			nutrient = Nutrient(None, True)
			nutrient.nutrient_type = json_nutrient[0]
			nutrient.nutrient_code = json_nutrient[1]
			nutrient.derivation_code = json_nutrient[2]
			nutrient.value = json_nutrient[3]
			nutrient.unit = json_nutrient[4]
			python_nutrients_list.append(nutrient)
		python_nutrients_dict = dict()
		for nutrient in python_nutrients_list:
			python_nutrients_dict[nutrient.nutrient_code] = nutrient
		python_database[id].nutrients = python_nutrients_dict

		python_database[id].name = product[2]
		python_database[id].unique_code = product[3]
		python_database[id].manufacturer = product[4]
		python_database[id].ingredients = product[5]

		# Progress Indicator
		items_processed = items_processed + 1
		progress_percent = (items_processed/total_items)*100.0
		if items_processed%10000 == 0:
			print ("%05.2f%%" % progress_percent)
	print "Done\n"
	return python_database

def getNutrientCodesList(fileName):
	print "Loading Nutrient Codes From File..."
	f = open(fileName, 'r+')
	codeList = []
	for line in f.readlines():
		codeList.append(int(line[0:3]))
	f.close()
	print "Done\n"
	return codeList

# Takes a Random Sample of the database
def randomSample(python_database, sample_percent):
	number_of_samples = 0
	sub_python_database = dict()
	keys = python_database.keys()
	total_items = sample_percent*len(python_database)
	items_processed = 0.0
	print "Getting Random Sample..."
	
	random.shuffle(keys)
	for i in range(int(sample_percent*len(python_database))):
		sub_python_database[keys[i]] = python_database[keys[i]]
		# Progress Indicator
		items_processed = items_processed + 1
		progress_percent = (items_processed/total_items)*100.0
		if items_processed%1000 == 0:
			print ("%05.2f%%" % progress_percent)

	print "Done\n"
	return sub_python_database

def printDatabase(python_database):
	for id, product in pythonDatabase.items():
		try:
			print ("ID: %d" % id)
			print ("Product Name: %s" % product.name)
		except:
			pass

# Unit Conversions
def performUnitConversionGramsToMilligrams(grams):
	# grams to milligrams
	# nutrients that need this conversion: Sodium, Potassium, 
	return grams*1000

def performUnitConversionMilligramsToGrams(milligrams):
	# milligrams to grams
	# nutrients that need this conversion: Sodium, Potassium
	return milligrams/1000

def performUnitConversionMilligramsToMicrorams(milligrams):
	# milligrams to micrograms
	# nutrients that need this conversion: Sodium, Potassium, 
	return milligrams*1000

# IU Conversions are different for each Nutrient
def performUnitConversionVitaminA(IU):
	# IU to micrograms
	return IU/1.667

def performUnitConversionVitaminD(IU):
	# IU to micrograms
	return IU/40

def performUnitConversionVitaminE(IU):
	# IU to milligrams
	return IU/1.35

def performUnitConversionsOnDatabase(pythonDatabase):
	for productID, product in pythonDatabase.items():
		for nutrientID, nutrient in product.nutrients.items():
			# Vitamin A
			if nutrientID == "318":
				nutrient.value = performUnitConversionVitaminA(nutrient.value)
			# Vitamin D
			elif nutrientID == "328":
				nutrient.value = performUnitConversionVitaminD(nutrient.value)
			# Vitamin E
			elif nutrientID == "340":
				nutrient.value = performUnitConversionVitaminE(nutrient.value)
			# Copper
			elif nutrientID == "312":
				nutrient.value = performUnitConversionMilligramsToMicrorams(nutrient.value)
			# Potassium
			elif nutrientID == "306":
				nutrient.value = performUnitConversionMilligramsToGrams(nutrient.value)
			# Sodium
			elif nutrientID == "307":
				nutrient.value = performUnitConversionMilligramsToGrams(nutrient.value)
	
	writeJSON(convertToJson(pythonDatabase), "convertedDatabase.json")