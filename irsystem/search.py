import csv
import math
import re
from irsystem.Stemming import stemming

def quicksortlist(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x[0] > pivot[0]]
    middle = [x for x in arr if x[0] == pivot[0]]
    right = [x for x in arr if x[0] < pivot[0]]
    return quicksortlist(left) + middle + quicksortlist(right)


def searchQuery(QUERY):
	################### load dictionary.txt into dictionary
	dictionary = []
	for line in open("irsystem/dictionary.txt", 'r').readlines():
		dictionary.append(line.strip())

	######################### load docID.csv into docID
	docID = {}
	with open("irsystem/docID.csv", 'r') as csv_file:
			reader = csv.reader(csv_file)
			docIDBuffer = dict(reader)

	for i in docIDBuffer:
		tp = re.findall("[\w\.]+",docIDBuffer[i])
		docID[ int(i) ] = tp[0]

	######################### load IDF.csv into IDF
	IDF = {}
	with open("irsystem/IDF.csv", 'r') as csv_file:
			reader = csv.reader(csv_file)
			IDFBuffer = dict(reader)

	for i in IDFBuffer:
		IDF[i] = float(IDFBuffer[i])

	######################### load weightNorm.csv into weightNorm
	weightNorm = {}
	with open("irsystem/weightNorm.csv", 'r') as csv_file:
			reader = csv.reader(csv_file)
			weightNormBuffer = dict(reader)

	for term in weightNormBuffer:
			weightNorm[term] = {}
			allDocID = re.split(",", weightNormBuffer[term])
			for docid_tf in allDocID:
				docID_TF = re.findall("[\d\.]+",docid_tf)
				weightNorm[term][int(docID_TF[0])] = float(docID_TF[1])

	########################## compute vecQuery
	vecQuery = {}
	query = QUERY.lower()
	allWord = re.findall("[a-z]+", query)
	for word1 in allWord:
		word = stemming(word1)
		if(word in dictionary):
			if(word in vecQuery):
				vecQuery[word] += 1
			else:
				vecQuery[word] = 1

	normOfQuery	= 0
	for term in vecQuery:
		vecQuery[term] = (1 + math.log10(vecQuery[term])) * IDF[term]
		normOfQuery += (1 + math.log10(vecQuery[term])) * IDF[term] * (1 + math.log10(vecQuery[term])) * IDF[term]

	normOfQuery = math.sqrt(normOfQuery)

	for term in vecQuery:
		vecQuery[term] = vecQuery[term] / normOfQuery

	######################### getting all docID which have any term in vecQuery, return result
	result = {}
	for term in vecQuery:
		for docid in weightNorm[term]:
			if (docid not in result):
				result[docid] = vecQuery[term] * weightNorm[term][docid]
			else:
				result[docid] += vecQuery[term] * weightNorm[term][docid]
	######################### finalResult
	finalResult = []
	for docid in result:
		finalResult.append([ result[docid], docID[docid]])

	finalResult = quicksortlist(finalResult)
	return finalResult[0:20]
##############################################################################################################################################

print(searchQuery("will forward or apex located controls be effective at low subsonic speeds and how do they compare with conventional trailing edge flaps"))
