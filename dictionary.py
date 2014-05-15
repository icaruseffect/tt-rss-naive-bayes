#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import pickle

def remove_stopwords(text):
	print "cleaning"
	cachedStopWords = pickle.load(open('stopwords.pkl', 'r'))
	text=text.lower()
	text = ' '.join([word for word in text.split() if word not in cachedStopWords])
	return text

#######Example#############
#input_text="Dies ist ein Test von der stoppwoerter funktion in Python! \n this is a test of the stopword function in python. \n Dit is een toets voor de stopwoorden functie in python"
#print input_text
#print remove_stopwords(input_text.lower())
