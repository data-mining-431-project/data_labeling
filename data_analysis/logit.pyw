# coding: utf-8
import json
import pandas as pd
import numpy as np
import DataCollectionFunctions
from sklearn.linear_model import LogisticRegressionCV
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
	trainX, trainY = DataCollectionFunctions.loadData(trainXfilename, trainYfilename)
	model = LogisticRegressionCV(solver = 'lbfgs', verbose = 1, cv = 3, max_iter = 1000)
	print "Training Model..."
	model.fit(trainX, trainY)
	print "Done\n"

	# Prediction
	testX, testY = DataCollectionFunctions.loadData("testX.json", "testY.json")
	print("Model Accuracy: %0.2f\n" % (100*model.score(testX, testY)))

	# Save Model
	saveModel(model, "newLogisticRegressionModel.joblib")

	# Load Model
	#LoadedModel = loadModel()
	#print("Loaded Model Accuracy: %0.2f\n" % (100*loadedModel.score(testX, testY)))

def saveModel(model, filename):
	# Save Model
	print "Saving Model..."
	joblib.dump(model, filename)
	print "Done\n"

def loadModel(filename):
	# Load Model
	print "Loading Model..."
	model = joblib.load(filename)
	print "Done\n"
	return model

def testModel(filename, testXfilename, testYfilename):
	testModel = loadModel(filename)
	testX, testY = DataCollectionFunctions.loadData(testXfilename, testYfilename)
	print("Test Model Accuracy: %0.2f\n" % (100*testModel.score(testX, testY)))

def getScores(model, X):
	# Get Scores
	print "Getting Scores..."
	scores = model.decision_function(X)
	print "Done\n"
	return scores

def saveScores(scores, filename):
	# Save Scores
	f = open(filename, 'w+')
	print "Saving Scores..."
	for score in scores:
			json.dump(score, f)
			f.write('\n')
	f.close()
	print "Done\n"