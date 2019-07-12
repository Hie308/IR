from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

def stemming(word):
	stemmer = WordNetLemmatizer()
	return stemmer.lemmatize(word)
