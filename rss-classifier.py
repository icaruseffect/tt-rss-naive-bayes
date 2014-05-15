#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import MySQLdb
import pickle
import re
import sys
import ConfigParser
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import PorterStemmer
from nltk import  clean_html

##open configuration file
config = ConfigParser.RawConfigParser()
config.read('rss-classifier.cfg')

##debug mode
debug=config.getboolean('debug', 'debug_enabled')
def debug_mode(text):
	if debug==True:
		 print text

articles=[]

def fuck_unicode(text):  ###try to clean up the encoding mess 1
	return text.decode('utf-8','ignore')
	#return unicode(text)


class RSSitem(object):
	def __init__(self,id_given,title_given,content_given,label_given):
		self.Id=int(id_given)
		self.Title=title_given
		self.Content=self.clean_content(content_given)
		self.Score_db=None
		self.Score=None
		self.Label=label_given



	def clean_content(self, to_clean):
		debug_mode( "cleaning RSS item" + str(self.Id) )
		tokenizer = WordPunctTokenizer()
		stemmer = PorterStemmer()

		clean= clean_html(to_clean)
		cachedStopWords = pickle.load(open('stopwords.pkl', 'r'))
		clean = tokenizer.tokenize(clean)

		if True==config.getboolean('filter', 'bigram_enabled'):
			bigram_finder = BigramCollocationFinder.from_words(clean)				#not sure if needed
			bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)			#same
			for bigram_tuple in bigrams:											#
				x = "%s %s" % bigram_tuple											#
				clean.append(x)														#

		tokens =  [stemmer.stem(x.lower()) for x in clean if x not in cachedStopWords and len(x) > 1]
		#clean = ' '.join([word for word in clean.split() if word not in cachedStopWords])
		debug_mode("cleaning RSS item finished")
		return tokens


	def show_all(self):
		print self.Id, self.Title, self.Content

class mysql_manager(object):
	#Database queries
	def __init__(self):
		self.var_db_prefix='ttrss_'
		self.queries = {
			"query_starred" : ("SELECT ref_id FROM  "+self.var_db_prefix+"user_entries WHERE (marked = 1) OR (published = 1)"),
			"query_read" : ("SELECT ref_id FROM " +self.var_db_prefix+"user_entries WHERE (marked = 0) AND (published = 0) AND (unread = 0)"),
			"query_unread" : ("SELECT ref_id FROM "+self.var_db_prefix+"user_entries WHERE (score = '0')")
		}

		if debug==True: print "mysql_manager started"
		self.connect_database()

		#self.get_content(self.query_starred)
	def get_settings():
		config=open("config.txt")

	def connect_database(self):
		debug_mode( "connecting to database" )
		self.ttrss_db = MySQLdb.connect(host=config.get('server', 'host'),
							  user=config.get('server','user'),
		                      passwd=config.get('server','password'),
		                      db=config.get('server','database')
		                      )
		debug_mode( "connection established" )
		self.db_cursor = self.ttrss_db.cursor()

	def get_content(self, query_type):
		self.label=  self.queries[query_type]
		self.content=None


		self.list_ids=self.db_cursor.execute(self.label) #get number of user entries
		for entry_id in range(1,self.list_ids):
			self.db_cursor.fetchall()
			self.query_entry= ("SELECT title, content FROM " +self.var_db_prefix+"entries WHERE (id="+ str(entry_id) +")")
			self.db_cursor.execute(self.query_entry)
			self.content_tmp=self.db_cursor.fetchall()
			#if ( self.content_tmp[0][0] and self.content_tmp[0][1] and self.content_tmp[0][2] ) != ' ' or None:
			articles.append(RSSitem( entry_id, self.content_tmp[0][0],self.content_tmp[0][1],self.label))

class train(object):
	def __init__(self):
		self.train_set=[]
		self.count=0

		if debug==True: print "Start creating training data"
		#for article in range(0,len(articles)):
		#	self.trainingdata.append(articles[article].Content)
		#	self.count+=1
		for article in articles:
			features = article.Content
			label = article.Label
			print label, features
		self.train_set = self.train_set + [features,label]
		debug_mode(("Finished creating training data:", self.train_set ))

		debug_mode("Start classification")
		self.classifier = NaiveBayesClassifier.train(self.train_set)
		classifier.show_most_informative_features(20)

def save_all_articles():
	articles_file=open("articles.txt",'w')
	pickle.dump(articles, articles_file)
	if debug==True: print "articles dumped"
def open_all_articles():
	articles_file=open("articles.txt",'r')
	articles=pickle.load(articles_file)
	if debug==True:
		debug_mode("articles re-read")
		debug_mode(articles)

def test():
	#open_all_articles()
	testtext2=("While Netflix and others work on new ways to stream movies to your browser through HTML5 that don't use Flash or Silverlight plugins Hollywoods requirements for DRM to prevent copying have put Mozilla in a bind The DRM proposed means user's don't know exactly what's going on their machines or if it's violating their privacy but without it Firefox will eventually be locked out of streaming most movies and TV shows. As a result Mozilla announced plans to roll it out in the next few months on Windows Mac and Linux versions of the browser so one upside could be official Netflix support on Linux.")
	testtext=('Wie viel beispielsweise von den drei Millionen Dollar, die Osama bin Laden 2002 angeblich für gleichgesinnte Organisationen in Afrika verteilen ließ, bei Boko Haram angekommen sind, ist fraglich. Ebenso, wie viel aus welcher Verbindung heute noch in ihre Taschen fließt und wie viele Anhänger etwa in Somalia, in Libyen noch unter Gaddafi, in Afghanistan oder anderen Ländern trainiert wurden. Ein Motiv für andere Gruppen, den nigerianischen Terror zu unterstützen: Sie haben ein Interesse daran, sich sichere Rückzugs- oder Fluchtorte zu schaffen. Darüber hinaus soll Boko Haram Geld von der in London sitzenden Hilfsorganisation Al-Muntada Trust Fund oder der saudi-arabischen Islamic World Society erhalten haben.')
	#testtext2=fuck_unicode(testtext2)
	for i in range(0,20):
		articles.append(RSSitem(127, "titel test", testtext2,"query_starred") )
		articles.append(RSSitem(127, "Ein anderer Titel", testtext,"query_read") )
		print "article " + str(i+1) +" added"

def create_corpus():
	data_fetcher=mysql_manager()
	data_fetcher.get_content("query_starred")
	data_fetcher.get_content("query_unread")
	save_all_articles()


#test()
#trainer=train()
create_corpus()

