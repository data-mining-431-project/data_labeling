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

# Takes a Random Sample of the database
def random_sample(python_database, sample_percent):
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

def get_nutrient_codes_list(fileName):
	print "Loading Nutrient Codes From File..."
	f = open(fileName, 'r+')
	codeList = []
	for line in f.readlines():
		codeList.append(int(line[0:3]))
	f.close()
	print "Done\n"
	return codeList

def make_nutrient_frequency_file(python_database, nutrient_codes):
	nutrient_frequency = dict()
	for nutrient_code in nutrient_codes:
		nutrient_frequency[nutrient_code] = 0

	for id, product in python_database.items():
		for nutrient_code in nutrient_codes:
			try:
				throw = product.nutrients[nutrient_code].value
				nutrient_frequency[nutrient_code] += 1
			except:
				pass
	
	nutrient_frequency_list = []
	for key, value in zip(nutrient_frequency.keys(), nutrient_frequency.values()):
		nutrient_frequency_list.append([key, value])

	nutrient_frequency_list = sorted(nutrient_frequency_list, key = lambda nutrient_frequency_list: nutrient_frequency_list[1], reverse = True)
	writeJSON(nutrient_frequency_list, "nutrient_frequency_list.JSON")

def make_adjusted_nutrient_code_file():
	nutrient_frequency_list = sorted(readJSON("nutrient_frequency_list.JSON"), key = lambda nutrient_frequency_list: nutrient_frequency_list[0])
	nutrient_code_list = []
	for nutrient_code in nutrient_frequency_list:
		nutrient_code_list.append(nutrient_code[0])

	f = open(nutrient_codes_filename, 'w+')
	g = open("all_nutrient_codes.txt", 'r+')
	for line in g.readlines():
		if int(line[0:3]) in nutrient_code_list:
			f.write(line)
	g.close()
	f.close()

def get_X(python_database, nutrient_codes):
	X = []
	for id, product in python_database.items():
		x = []
		for nutrient_code in nutrient_codes:
			try:
				x.append(product.nutrients[nutrient_code].value)
			except:
				x.append(0.0)
		X.append(x)
	return X

def find_k(X, low_cluster_limit, high_cluster_limit):
	x = range(low_cluster_limit, high_cluster_limit+1)
	y = []
	items_processed = 0.0
	total_items = len(x)

	print "Calculating k-values..."
	for k in x:
		km = KMeans(n_clusters = k, n_init = 100, n_jobs = -2)
		km.fit(X)
		y.append(km.inertia_)
		# Progress Indicator
		items_processed = items_processed + 1
		progress_percent = (items_processed/total_items)*100.0
		if items_processed%1 == 0:
			print ("%05.2f%%" % progress_percent)
	print "Done\n"

	plt.xlabel("k-Clusters")
	plt.ylabel("SSE")
	plt.title("Nutrients K-Means")
	plt.plot(x,y)
	plt.grid(b=True, which='both')
	plt.show()

def run_kmeans(python_database, nutrient_codes, low_cluster_limit, high_cluster_limit):
	X = get_X(python_database, nutrient_codes)
	find_k(X, low_cluster_limit, high_cluster_limit)

def main():
	python_database = convert_from_json(readJSON(python_database_filename))
	nutrient_codes = get_nutrient_codes_list(nutrient_codes_filename)

	# Settings
	low_cluster_limit = 1
	high_cluster_limit = 20
	# Find best k
	run_kmeans(python_database, nutrient_codes, low_cluster_limit, high_cluster_limit)
	

if __name__ == '__main__':
	main()