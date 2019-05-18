# coding: utf-8
import json
import pandas as pd
import numpy as np
import DataCollectionFunctions
from sklearn import svm
from sklearn.model_selection import GridSearchCV
import joblib

#X: each base value of nutrients, like [cal, pot, sod...],
#each column refers to each product 
def trainsvm(filenames):
	crossXfilename = filenames[0][0]
	crossYfilename = filenames[0][1]
	trainXfilename = filenames[1][0]
	trainYfilename = filenames[1][1]
	testXfilename = filenames[2][0]
	testYfilename = filenames[2][1]
	crossX, crossY = DataCollectionFunctions.loadData(crossXfilename, crossYfilename)
	#svm - 10 folder cross validation
	crossModel = svm.SVC(kernel = 'linear')
	Cs = range(20,31)
	for i in [40, 50, 60, 70, 80, 90, 100]:
		Cs.append(i)
	crossModel = GridSearchCV(estimator=crossModel, param_grid=dict(C=Cs), n_jobs = 1, cv = 3, verbose = 10)
	print "Performing Cross Validation..."
	crossModel.fit(crossX, crossY)
	print "Done\n"
	#w values
	#Wvalues = gridSearchModel.best_estimator_.coef_
	#print Wvalues
	#b values
	#print gridSearchModel.best_estimator_.intercept_
	#estimated C
	print "The estimated C after the grid search for 10 fold cross validation: "
	crossModelParameter = crossModel.best_params_
	print crossModelParameter
	print

	# Train Actual Model
	trainX, trainY = DataCollectionFunctions.loadData(trainXfilename, trainYfilename)
	model = svm.SVC(kernel = 'linear', C=crossModelParameter['C'], verbose = True)

	print "Training Model..."
	model.fit(trainX, trainY)
	print "Done\n"

	# Prediction
	testX, testY = DataCollectionFunctions.loadData(testXfilename, testYfilename)
	print("Model Accuracy: %0.2f\n" % (100*model.score(testX, testY)))

	# Save Model
	saveModel(model, "newSvmModel.joblib")

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