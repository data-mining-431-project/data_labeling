from product import Product, Nutrient
import json
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import random
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pylab as pl
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import os, sys
import matplotlib.cm as cm
import math

import pandas as pd

python_database_filename = "nutrition_database.json"
nutrient_codes_filename = "nutrient_codes.txt"
dir_path = os.path.dirname(os.path.realpath(__file__))

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

def convert_to_json(python_database):
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

def convert_from_json(json_database):
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

def get_nutrient_codes_list(fileName):
	print "Loading Nutrient Codes From File..."
	f = open(fileName, 'r+')
	codeList = []
	for line in f.readlines():
		codeList.append(int(line[0:3]))
	f.close()
	print "Done\n"
	return codeList

def get_suggested_intakes():
	ref_intakes = pd.read_csv('Dietary_Reference_Intakes.csv')
	#print ref_intakes
	for i in ref_intakes:
		for val in i:
			print val

def main():
	python_database = convert_from_json(readJSON(python_database_filename))
	nutrient_codes = get_nutrient_codes_list(nutrient_codes_filename)
	get_suggested_intakes()

if __name__ == '__main__':()
main()