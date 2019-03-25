
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import random, math


# Class for P2P or Not P2P values
##########################################################################################
class DataNetwork:

	def __init__(self):
		self.parameters = ['Addresses', 'Connections', 'Bandwidth', 'PacketSize', 'Time']
		self.number = 0
		
		self.dictionaryValues = {}
		self.dictionaryValues['Addresses'] = {}
		self.dictionaryValues['Connections'] = {}
		self.dictionaryValues['Bandwidth'] = {}
		self.dictionaryValues['PacketSize'] = {}
		self.dictionaryValues['Time'] = {}

		self.dictionaryProbabilities = {}


	def addElement(self, values):

		mixVectors = zip(self.parameters, values)
		dictValues = set(mixVectors)
		
		for values in dictValues:
			if values[1] in self.dictionaryValues[values[0]]:
				self.dictionaryValues[values[0]][values[1]] += 1
			else:
				self.dictionaryValues[values[0]][values[1]] = 1

	def createProbabilities(self):

		self.dictionaryProbabilities = copy.deepcopy(self.dictionaryValues)

		for key1 in self.dictionaryProbabilities:
			for key2 in self.dictionaryProbabilities[key1]:
				self.dictionaryProbabilities[key1][key2] /= self.number


# Vector Learning and Test
##########################################################################################

def getVectorLines(numberLines, percentageLearning):

	learningLines = math.modf(percentageLearning * numberLines)[1]

	vectorTotal = list(range(0,numberLines))
	vectorLearning = []
	while len(vectorLearning) < learningLines:
		line = random.randint(0, numberLines-1)
		if line not in vectorLearning:
			vectorLearning.append(line)
	
	vectorTest = [u for u in vectorTotal if u not in set(vectorLearning)]

	return vectorLearning, vectorTest



# Learning Process
##########################################################################################
def learningProcess(peer, notPeer, file, vectorLearning):
	
	lineNumber = 0
	for line in file:

		if lineNumber in vectorLearning:
			values = line.split(',')
			peerNotPeer = values[-1].rstrip()
			values = values[:-1]

			if peerNotPeer == "p2p":
				peer.addElement(values)
				peer.number += 1
			
			elif peerNotPeer == "not p2p":
				notPeer.addElement(values)
				notPeer.number += 1

			else:
				print("Error...")
		
		lineNumber += 1



# Test Process
##########################################################################################
def testProcess(peer, notPeer, file, vectorTest):

	truePositives = 0
	trueNegatives = 0
	falsePositives = 0
	falseNegatives = 0

	lineNumber = 0
	for line in file:

		if lineNumber in vectorTest:
			values = line.split(',')
			peerNotPeer = values[-1].rstrip()
			values = values[:-1]

			peerProbability = calculateProbabilityUnkown(peer, values)
			peerProbability *= peer.number / (peer.number + notPeer.number)

			notPeerProbability = calculateProbabilityUnkown(notPeer, values)
			notPeerProbability *= notPeer.number / (peer.number + notPeer.number)


			if peerProbability >= notPeerProbability:
				answer = "p2p"
			else:
				answer = "not p2p"

			if answer == "p2p" and peerNotPeer == "p2p":
				truePositives += 1
			elif answer == "p2p" and peerNotPeer == "not p2p":
				falsePositives += 1
			elif answer == "not p2p" and peerNotPeer == "p2p":
				falseNegatives += 1
			elif answer == "not p2p" and peerNotPeer == "not p2p":
				trueNegatives += 1
			else:
				print("Something wrong...")

		lineNumber += 1

	return truePositives, trueNegatives, falsePositives, falseNegatives



# Test Process
##########################################################################################
def appendUnlabeled(peer, notPeer, file, fileOut):


	lineNumber = 0
	for line in file:

		valuesTemp = line.split(',')
		values = []
		for value in valuesTemp:
			values.append(value.rstrip())

		peerProbability = calculateProbabilityUnkown(peer, values)
		peerProbability *= peer.number / (peer.number + notPeer.number)

		notPeerProbability = calculateProbabilityUnkown(notPeer, values)
		notPeerProbability *= notPeer.number / (peer.number + notPeer.number)


		if peerProbability > notPeerProbability:
			answer = "p2p"
		else:
			answer = "not p2p"

		fileOut.write(line.rstrip() + "," + answer + "\n")

		lineNumber += 1



def calculateProbabilityUnkown(peerNotPeer, values):

	mixVectors = zip(peerNotPeer.parameters, values)
	dictValues = set(mixVectors)

	probabilityPeerNotPeer = 1
	for values in dictValues:

		if values[1] in peerNotPeer.dictionaryProbabilities[values[0]]:
			valueProbability = peerNotPeer.dictionaryProbabilities[values[0]][values[1]]
		else:
			valueProbability = 0

		probabilityPeerNotPeer *=  valueProbability

	return probabilityPeerNotPeer


def verifyPerformance(truePositives, trueNegatives, falsePositives, falseNegatives):

	print(truePositives, trueNegatives, falsePositives, falseNegatives)

	numberPatterns = truePositives + trueNegatives + falsePositives + falseNegatives
	numberErrors = falsePositives + falseNegatives
	numberCorrects = truePositives + trueNegatives

	accuracy = numberCorrects / numberPatterns
	errorRate = numberErrors / numberPatterns

	precision = truePositives / (truePositives + falsePositives)
	recall = truePositives / (truePositives + falseNegatives)
	negativeRate = trueNegatives / (trueNegatives + falsePositives)

	FMeasure = 2 * (precision * recall) / (precision + recall)

	print("Number Patterns = " + str(numberPatterns))
	print("Number Errors = " + str(numberErrors))
	print("Number Corrects = " + str(numberCorrects))
	print("Accuracy = " + str(accuracy))
	print("Error Rate = " + str(errorRate))
	print("Precision = " + str(precision))
	print("Recall = " + str(recall))
	print("Negative Rate = " + str(negativeRate))
	print("F-Measure = " + str(FMeasure))



# TestPerformance
##########################################################################################
def testPerformance(fileNumber, percentageLearning):


	fileName = "../P2PData/" + str(fileNumber) + "-labeled.dat"
	file = open(fileName, "r")

	peer = DataNetwork()
	notPeer = DataNetwork()

	numberLines = sum(1 for line in open(fileName))

	vectorLearning, vectorTest = getVectorLines(numberLines, percentageLearning)

	learningProcess(peer, notPeer, file, vectorLearning)
	
	peer.createProbabilities()
	notPeer.createProbabilities()
	
	file.seek(0)
	
	truePositives, trueNegatives, falsePositives, falseNegatives = testProcess(peer, notPeer, file, vectorTest)

	file.close()

	return truePositives, trueNegatives, falsePositives, falseNegatives


# TestPerformance
##########################################################################################
def createUnlabeled(fileNumber):

	fileName = "../P2PData/" + str(fileNumber) + "-labeled.dat"
	file = open(fileName, "r")

	peer = DataNetwork()
	notPeer = DataNetwork()

	percentageLearning = 1
	numberLines = sum(1 for line in open(fileName))

	vectorLearning, vectorTest = getVectorLines(numberLines, percentageLearning)

	learningProcess(peer, notPeer, file, vectorLearning)
	
	peer.createProbabilities()
	notPeer.createProbabilities()
	
	file.close()
	fileName = "../P2PData/" + str(fileNumber) + "-unlabeled.dat"
	file = open(fileName, "r")
	fileNameOut = "../Results/out-" + str(fileNumber) + "-unlabeled.dat"
	fileOut = open(fileNameOut, "w")


	appendUnlabeled(peer, notPeer, file, fileOut)



	'''
	print("\nDictionary for P2P Connections Values\n-------------------------------------")	
	for k, v in peer.dictionaryValues.items(): print(k, v)
	print("\nDictionary for P2P connections Probabilities\n--------------------------------------------")	
	for k, v in peer.dictionaryProbabilities.items(): print(k, v)
		

	print("\nDictionary for Not P2P Connections Values\n-------------------------------------")	
	for k, v in notPeer.dictionaryValues.items(): print(k, v)
	print("\nDictionary for Not P2P connections Probabilities\n--------------------------------------------")	
	for k, v in notPeer.dictionaryProbabilities.items(): print(k, v)

	'''



