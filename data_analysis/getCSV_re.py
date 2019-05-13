# coding: utf-8
from __future__ import division
from sklearn.datasets import load_iris

import json
import pandas as pd
import numpy as np
import math
from sklearn.linear_model import LogisticRegression
from sklearn import svm
#import pylab as pl
from sklearn.model_selection import train_test_split 
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



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
	#print X
#general
	#clf = svm.SVC(kernel='linear',C=1, probability=True).fit(X, y)

#svm - 10 folder cross validation
	svc = svm.SVC(kernel='linear')
	Cs = range(1,20)
	clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs), cv = 10)
	clf.fit(X, y)

#estimated w values
	Wvalues = clf.best_estimator_.coef_
	print Wvalues
#estimated b values
	bvalue = clf.best_estimator_.intercept_
	print bvalue
#best parameters 
	bestParaDict = clf.best_params_
	print bestParaDict
	print("Accuracy: %0.2f (+/- %0.2f)" % (clf.best_estimator_.coef_.mean(), clf.best_estimator_.coef_.std() * 2))
	#print clf.param_grid

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

#get score from SVM, try graph
#achieve best parameters
	bestW = Wvalues[bestParaDict['C']-1]
	bestW = bestW.tolist()
	print bestW

	#1/sqrt(w*w)
	bestb = bvalue[bestParaDict['C']-1]

	sumtop = 0
	sumbottom = 0
	counter = []
	frameVal = []
	n = 0
	for eachProduct in X:
		counter.append(n) 
		n += 1
		for i in range(len(eachProduct)):
			sumtop = sumtop + (eachProduct[i]*bestW[i])
			summulti = bestW[i]*bestW[i]
			sumbottom += summulti
		topCalc = abs(sumtop + bestb)
		bottomCalc = math.sqrt(sumbottom)
		distance = topCalc/bottomCalc 
		frameVal.append(distance)

		#print distance
		#Correlation matrix plot
	#data= load_iris()
	#print data
	#df= pd.DataFrame(data= data['data'], columns= data['feature_names'])

	df = pd.DataFrame(data=X)#list(zip(X)))
	plt.matshow(df.corr())
	plt.colorbar()
	plt.title('Correlation matrix plot')
	plt.ylabel(df.columns.values,fontsize=10)
	plt.xlabel(df.columns.values,fontsize=10)
#	plt.show()


	df1 = pd.DataFrame(data=frameVal)
	plt.figure()

	sns.set_style('darkgrid')
	sns.distplot(df1,hist=False)
	plt.title("Probability Distribution")
	plt.ylabel("Probabilities")
	plt.xlabel("Scores")
	plt.show()

'''
	distance = lambda x,y: (abs(x*y + bestb)/(math.sqrt(x*x))) if x!=0 else 0

	dataValue = []
	for eachProduct in X:
		func = np.vectorize(distance)	
		score = func(bestW,eachProduct)
		score = score.tolist()
		print score


	#Convert to dataframe
	#for 
	#Correlation matrix plot
	data = pd.read(score)
	plt.figure()
	plt.title('Correlation matrix plot')
	plt.matshow(data.corr())
	plt.colorbar()
	plt.ylabel(data.columns.values,fontsize=5)
	plt.xlabel(data.columns.values,fontsize=5)
	plt.show()

	predictedFile = open("predictedProduct.json","w+")
	pred = []
	for label in testY:
		for each in testX:
			pred.append(str(label)+","+str(each))
	for line in pred:
		predictedFile.write(line)
'''




def main():
	svmprac()
	#getSuggestedIntakes()
if __name__ == '__main__':()
main()