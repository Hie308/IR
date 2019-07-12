from nltk.corpus import stopwords
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from stop_words import get_stop_words
'''
print(len(stopwords.words('english')))
print(len(ENGLISH_STOP_WORDS))
print(len(list(get_stop_words('en'))))
'''

SW = []
for line in open("stopwords_en.txt", 'r').readlines():
    SW.append(line.strip())

sklearn_word = list(ENGLISH_STOP_WORDS)
nltk_words = list(stopwords.words('english'))

STOP_WORDS = list(get_stop_words('en'))

for w in nltk_words:
	if(w not in STOP_WORDS):
		STOP_WORDS.append(w)

for w in sklearn_word:
	if(w not in STOP_WORDS):
		STOP_WORDS.append(w)

for w in SW:
	if(w not in STOP_WORDS):
		STOP_WORDS.append(w)

print(len(STOP_WORDS))

f = open("stopwords.txt", "w")
for word in STOP_WORDS:
	f.write(word + '\n')
f.close()
