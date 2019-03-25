#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mainFunction



# Verify if string is a number
##########################################################################################
def isNumber(number):

	try:
		float(number)
		return True
	except ValueError:
		pass

	try:
		import unicodedata
		unicodedata.numeric(number)
		return True
	except (TypeError, ValueError):
		pass

	return False



# Main
##########################################################################################
def main():

	fileNumber = ""
	percentageLearning = ""
	nrRepetitions = ""

	while True:

		if not (isNumber(fileNumber) and (1 <= int(fileNumber) <= 4)):
			fileNumber = input("What file do you want? (choose between 1 and 4) \nYour choise: ")

		elif not(isNumber(percentageLearning)):
			percentageLearning = input("What percentage do you want for the learning process? \nYour choise:")

		elif not(isNumber(nrRepetitions)):
			nrRepetitions = input("How many times do you want to repeat the tests? \nYour choise:")

		else:
			break


	truePositives = []
	trueNegatives = []
	falsePositives = []
	falseNegatives = []

	for i in range(int(nrRepetitions)):

		x1, x2, x3, x4 = mainFunction.testPerformance(fileNumber, float(percentageLearning))
		truePositives.append(x1)
		trueNegatives.append(x2)
		falsePositives.append(x3)
		falseNegatives.append(x4)

	truePositives = sum(truePositives) / len(truePositives)
	trueNegatives = sum(trueNegatives) / len(trueNegatives)
	falsePositives = sum(falsePositives) / len(falsePositives)
	falseNegatives = sum(falseNegatives) / len(falseNegatives)

	mainFunction.verifyPerformance(truePositives, trueNegatives, falsePositives, falseNegatives)


main()