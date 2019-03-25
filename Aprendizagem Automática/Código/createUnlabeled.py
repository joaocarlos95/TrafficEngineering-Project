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

	while True:

		if not (isNumber(fileNumber) and (1 <= int(fileNumber) <= 4)):
			fileNumber = input("What file do you want? (choose between 1 and 4) \nYour choise: ")

		else:
			break

	mainFunction.createUnlabeled(fileNumber)
	


main()