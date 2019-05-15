# coding: utf-8
import json
import pandas as pd
import numpy as np

import DataCollectionFunctions

from sklearn.linear_model import LogisticRegression
from sklearn import svm
#import pylab as pl
from sklearn.model_selection import train_test_split 
from sklearn.model_selection import GridSearchCV
#getting value with assigned age among each nutrient from Dietary_Reference_Intakes table
#another for loop assigning t
'''
	#save into a dictionary, key: nutrient id, value: ideal value
	#return idealValueDict
	#a dict with all id and {203, 123.4},{...}
'''
'''
def getSuggestedIntakes(nutrientCodes):
	# Zurui
	# adjustedIdealValue = (idealValue/day) * 1/(suggestedCaloricIntake/day)
	# process into a dictionary of the form
	# nutrinetID : adjustedIdealValue
	
	idealValuesDict = dict()
	refIntakes = pd.read_csv('Dietary_Reference_Intakes.csv')
	for n in range(1,18):
		for nutrient in refIntakes:
			idealIntake = refIntakes[nutr][n]/refIntakes[Calories][n]
			for nutrientID in nutrientCodes:
				if nutrient in nutrientCodes:
					nID = nutrientCodes[0,2] 
					idealValuesDict[nID] = idealIntake
		#suggested = refIntakes[nutr][yr]
	return idealValuesDict
'''


#X: each base value of nutrients, like [cal, pot, sod...],
#each column refers to each product 
def svmprac():
	X = []
	y = []
	X, y = DataCollectionFunctions.loadSvmData()

#general
	#clf = svm.SVC(kernel='linear',C=1, probability=True).fit(X, y)

#svm - 10 folder cross validation
	#svc = svm.SVC(kernel = 'linear')
	#Cs = range(1, 20)
	#clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs), cv = 10)
	clf = svm.SVC(kernel = 'linear', C=1)
	clf.fit(X, y)

#w values
	#Wvalues = clf.best_estimator_.coef_
	#print Wvalues
#b values
	#print clf.best_estimator_.intercept_
#estimated C
#	
	#print("Accuracy: %0.2f (+/- %0.2f)" % (clf.best_estimator_.coef_.mean(), clf.best_estimator_.coef_.std() * 2))
	#print "The estimated C after the grid search for 10 fold cross validation: "
	#print clf.best_params_

#logistic regression 
	#lr = LogisticRegression()
	#lr.fit(X,y)
#prediction
	test = []
	file = open("predictTest.json","r+")
	for tx in file:
		test.append(json.loads(tx))
	testX = []
	for productNutri in test:
		temp = []
		for n in productNutri:
			temp.append(float(n))
		testX.append(temp)

	CVtestY = clf.predict(testX)

	testY = []
	file = open("testLabels.json","r+")
	for tx in file:
		testY.append(json.loads(tx))
	
	print clf.score(testX, testY)

	for i in range(len(test)):
		print "%2d | %2d" % (CVtestY[i], test[i])
	
'''
	predictedFile = open("predictedProduct.json","w+")
	pred = []
	for label in testY:
		for each in testX:
			pred.append(str(label)+","+str(each))
	for line in pred:
		predictedFile.write(line)
#get score from SVM, try graph
'''

def main():
	svmprac()
	#getSuggestedIntakes()
if __name__ == '__main__':()
main()