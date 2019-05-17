# coding: utf-8
import json
import pandas as pd
import numpy as np
import DataCollectionFunctions
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import joblib

#X: each base value of nutrients, like [cal, pot, sod...],
#each column refers to each product 
def trainLogisticRegression(filenames):
	crossXfilename = filenames[0][0]
	crossYfilename = filenames[0][1]
	trainXfilename = filenames[1][0]
	trainYfilename = filenames[1][1]
	testXfilename = filenames[2][0]
	testYfilename = filenames[2][1]

	# Train Actual Model
	testX, testY = DataCollectionFunctions.loadData(testXfilename, testYfilename)
	model = LogisticRegression()
	print "Training Model..."
	model.fit(testX, testY)
	print "Done\n"

	# Prediction
	testX, testY = DataCollectionFunctions.loadSvmData("testX.json", "testY.json")
	print("Model Accuracy: %0.2f\n" % (100*model.score(testX, testY)))

	# Save Model
	saveModel(model, "logisticRegressionModel.joblib")

	# Load Model
	#LoadedModel = loadModel()
	#print("Loaded Model Accuracy: %0.2f\n" % (100*loadedModel.score(testX, testY)))

def saveModel(model, filename):
	# Save Model
	print "Saving Model..."
	joblib.dump(model, filename)
	print "Done\n"

def loadModel():
	# Load Model
	print "Loading Model..."
	model = joblib.load('model.joblib')
	print "Done\n"
	return model