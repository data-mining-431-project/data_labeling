from product import Product, Nutrient
import DataCollectionFunctions
import DatabaseFunctions

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

pythonDatabaseFilename = "nutrition_database.json"
nutrientCodesFilename = "nutrient_codes.txt"

def main():
	pythonDatabase = convertFromJson(readJSON(pythonDatabaseFilename))
	nutrientCodes = getNutrientCodesList(nutrientCodesFilename)
	


if __name__ == '__main__':
	main()