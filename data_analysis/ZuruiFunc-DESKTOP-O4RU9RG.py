import pandas as pd
import numpy as np

#getting value with assigned age among each nutrient from Dietary_Reference_Intakes table
#another for loop assigning t

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

	return idealValuesDict



def main():

	#python_database = convert_from_json(readJSON(python_database_filename))
	#nutrient_codes = get_nutrient_codes_list(nutrient_codes_filename)
	getSuggestedIntakes()

if __name__ == '__main__':()
main()