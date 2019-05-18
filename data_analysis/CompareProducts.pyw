# coding: utf-8
import json
import pandas as pd
import numpy as np
import DataCollectionFunctions
from sklearn import svm
from sklearn.model_selection import GridSearchCV
import joblib

def compareProducts(productId1, productId2, productScoresDict):
	print "%19s | %19s" % ("Product 1: " + str(productId1), "Product 2: " + str(productId2))
	print "%9s: %8f | %9s: %8f" % ("Score 1", round(productScoresDict[productId1], 4), "Score 2", round(productScoresDict[productId2], 4))
	
def loadProductIds():
	f = open("productIds.json", 'r+')
	productIds = []
	for line in f.readlines():
		productIds.append(json.loads(line))
	f.close()
	return productIds

def loadScores(filename):
	f = open(filename, 'r+')
	scores = []
	for line in f.readlines():
		scores.append(json.loads(line))
	f.close()
	return scores

def createProductScoresDict(productIds, scores):
	productScoresDict = dict()
	for productId, score in zip(productIds, scores):
		productScoresDict[productId] = score
	return productScoresDict