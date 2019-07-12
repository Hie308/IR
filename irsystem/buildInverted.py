import re
import os
import csv
import math
from Stemming import stemming

pathToData = "data"
pathToVocab = "dictionary.txt"
numOfDoc = 0

################### load vocab into dictionary
dictionary = []
for line in open("dictionary.txt", 'r').readlines():
    dictionary.append(line.strip())

################### initialaziton invertedIndex and Weight and weightNorm
invertIndex = {}
weight = {} 
weightNorm = {}
for term in dictionary:
	invertIndex[term] = {}
	weight[term] = {}
	weightNorm[term] = {}

################### docMatrix
docMatrix = {}

################### build inverted index & build docID ----- docID[doc_ID] [nameFile]
docID = {}
doc_ID = 1

for fileName in os.listdir(pathToData):
	if (os.path.isdir(pathToData + "/" + fileName) ):
		for subfileName in os.listdir(pathToData + "/" + fileName):
			with open(pathToData + "/" + fileName + "/" + subfileName, "r",encoding= "utf-8", errors= "ignore") as f:
				text = f.read()
			f.close()
			text = text.lower()
			allWord = re.findall("[a-z]+", text)
			docID[doc_ID] = [subfileName]
			docMatrix[doc_ID] = {}
			print(numOfDoc)			
			numOfDoc += 1
			for word1 in allWord:
				word = stemming(word1)
				if(word in dictionary):										
					if(doc_ID not in invertIndex[word]):
						invertIndex[word][doc_ID] = 1
					else:
						invertIndex[word][doc_ID] += 1
				
					if(word in docMatrix[doc_ID]):
						docMatrix[doc_ID][word] += 1
					else:
						docMatrix[doc_ID][word] = 1
			doc_ID += 1

#################### compute normalization IDF for each term and nomarlization for TF and build weight
IDF = {}
for term in invertIndex:
	IDF[term] = 1 + math.log10(numOfDoc/len(invertIndex[term]))
	for doc_id in invertIndex[term]:
		invertIndex[term][doc_id] = 1 + math.log10(invertIndex[term][doc_id])
		weight[term][doc_id] = invertIndex[term][doc_id] * IDF[term]

#################### compute Norm for each Doccument
Norm = {}
for doc in docMatrix:
	Norm[doc] = 0
	for term in docMatrix[doc]:
		Norm[doc] += ( 1 + math.log10(docMatrix[doc][term]) ) * IDF[term] * ( 1 + math.log10(docMatrix[doc][term]) ) * IDF[term]
	Norm[doc] = math.sqrt(Norm[doc])

#################### build weightNorm 
for term in weight:
	for doc_id in weight[term]:
		weightNorm[term][doc_id] = weight[term][doc_id] / Norm[doc_id]

#################### save weightNorm, IDF & docID
with open('IDF.csv','w') as csvfile:
	writer = csv.writer(csvfile)
	for key,value in IDF.items():
		writer.writerow([key,value])

with open('docID.csv','w') as csvfile:
	writer = csv.writer(csvfile)
	for key,value in docID.items():
		writer.writerow([key,value])

with open('weightNorm.csv','w') as csvfile:
	writer = csv.writer(csvfile)
	for key,value in weightNorm.items():
		writer.writerow([key,value])































