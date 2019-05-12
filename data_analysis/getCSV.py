# coding: utf-8
import json
import pandas as pd
import numpy as np

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
	labelFile = open("productLabelsY.json","r+")

	for label in labelFile:
		label = json.dumps(label)
		y.append(label)
	labelFile.close()


	productNutrientsSTD = open("productNutrientValuesX.json","r+")
	for eachProduct in productNutrientsSTD:
		eachProduct = json.loads(eachProduct)
		X.append(eachProduct)
	productNutrientsSTD.close()

#general
	#clf = svm.SVC(kernel='linear',C=1, probability=True).fit(X, y)

#svm - 10 folder cross validation
	svc = svm.SVC(kernel='linear')
	Cs = range(1, 20)
	clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs), cv = 10)
	clf.fit(X, y)

#w values
	Wvalues = clf.best_estimator_.coef_
	print Wvalues
#b values
	print clf.best_estimator_.intercept_
#estimated C
#	print clf.best_params_
	print("Accuracy: %0.2f (+/- %0.2f)" % (clf.best_estimator_.coef_.mean(), clf.best_estimator_.coef_.std() * 2))

#logistic regression 
	lr = LogisticRegression()
	lr.fit(X,y)
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
	LRtestY = lr.predict(testX)
	#print CVtestY
	#print LRtestY
	CVcounter = 0
	for arr in CVtestY:
		Ynum1 = int(arr[1])
		CVcounter = CVcounter + Ynum1
	LRcounter = 0
	for arr in LRtestY:
		Ynum2 = int(arr[1])
		LRcounter = LRcounter + Ynum2	
	print "total number of testing nutrients by Cross Validation: {} ({} are predicted as positives, {} are predicted as negatives)".format(len(CVtestY), CVcounter, len(CVtestY) - CVcounter)
	print "total number of testing nutrients by Logistic Regression: {} ({} are predicted as positives, {} are predicted as negatives)".format(len(LRtestY), LRcounter, len(LRtestY) - LRcounter)
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