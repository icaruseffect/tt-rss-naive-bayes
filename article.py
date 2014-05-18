#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from nltk.tokenize import WordPunctTokenizer
from nltk.stem import PorterStemmer
from nltk import  clean_html
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

class Article(object):
	'This is an article object. It cleans the content to prepare it for an filter'

	def __init__(self, data_given):
		for item in data_given:
			self.item = data_given[item]


	def clean_content(self, to_clean):
		debug_mode( "cleaning RSS item" + str(self.Id) )
		tokenizer = WordPunctTokenizer()
		stemmer = PorterStemmer()

		clean= clean_html(to_clean)
		cachedStopWords = pickle.load(open('stopwords.pkl', 'r'))
		clean = tokenizer.tokenize(clean)

		if True==config.getboolean('filter', 'bigram_enabled'):
			bigram_finder = BigramCollocationFinder.from_words(clean)
			bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)
			for bigram_tuple in bigrams:
				x = "%s %s" % bigram_tuple
				clean.append(x)

		tokens =  [stemmer.stem(x.lower()) for x in clean if x not in cachedStopWords and len(x) > 1]

		debug_mode("cleaning RSS item finished")
		return tokens

	def show_all(self):
		print self.Id, self.Title, self.Content
