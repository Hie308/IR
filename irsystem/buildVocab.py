import re
import os
import csv
from Stemming import stemming

SW = []
for line in open("stopwords.txt", 'r').readlines():
    SW.append(line.strip())

pathToData = 'data'

dictionary  = []
count = 0

for fileName in os.listdir(pathToData):
	if (os.path.isdir(pathToData + "/" + fileName) ):
		for subfileName in os.listdir(pathToData + "/" + fileName):
			with open(pathToData + '/' + fileName + '/' + subfileName, "r",encoding='utf-8', errors='ignore') as f:
				text = f.read()
			f.close()
			print(count)
			count += 1
			text = text.lower()
			allWord = re.findall("[a-z]+", text)
			for word in allWord:
				word_stemming = stemming(word)
				if(word_stemming not in dictionary):
					dictionary.append(word_stemming)
					
dictionary.sort()

filtered_words = [w for w in dictionary if w not in SW]

f = open("dictionary.txt", "w")
for word in filtered_words:
	f.write(word + '\n')
f.close()

