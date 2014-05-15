#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import nltk
import MySQLdb
import pickle
import re
import ascii_with_complaints
import codecs
import itertools
from reverend.thomas import Bayes

debug=True
articles=[]
export_file="articles_Export.txt"
import_file="articles_Import.txt"
classifier_data="classification.txt"

def debug_mode(text):
	if debug==True:
		 print text


def fuck_unicode(text):  ###try to clean up the encoding mess 1
	#return text.encode('ascii','ignore')
	return text.encode('utf-8','ignore')
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
		debug_mode( "cleaning RSS item")
		clean= nltk.clean_html(to_clean)
		cachedStopWords = pickle.load(open('stopwords.pkl', 'r'))
		clean=clean.lower()
		clean = ' '.join([word for word in clean.split() if word not in cachedStopWords])
		debug_mode("cleaning RSS item finished")
		return clean


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
		self.get_content(self.query_starred)


	def connect_database(self):
		if debug==True: print "connecting to database"
		self.ttrss_db = MySQLdb.connect(host='127.0.0.1',
							  user='ttrss',
		                      passwd="dMhDMsDU6Czfmot4vd",
		                      db="ttrss")
		if debug==True: print "connection established"
		self.db_cursor = self.ttrss_db.cursor()

	def get_content(self, query_type):
		self.label=  self.queries[query_type]
		self.content=None


		self.list_ids=self.db_cursor.execute(self.label)
										#get number of user entries
		for entry_id in range(1,self.list_ids):
			self.db_cursor.fetchall()
			self.query_entry= ("SELECT id,title, content FROM " +self.var_db_prefix+"entries WHERE (id="+ unicode(entry_id) +")")
			self.db_cursor.execute(self.query_entry)
			self.content_tmp=unicode( self.db_cursor.fetchall() )
			articles.append(RSSitem( self.content_tmp[0][0],self.content_tmp[0][1],self.content_tmp[0][2],self.label))

class train(object):
	def __init__(self):
		#self.trainingdata=dict()
		self.count=0
		debug_mode( "Start training" )
		self.learn_data=[]

		#for article in articles:
		#	self.count+=1
		#	#self.trainingdata = dict(article.Content ,article.Label)
		#	for article in articles:
		#		self.trainingdata.append ((article.Content, article.Label))
		#		debug_mode("Training: article" + unicode(article.Id) + " added" )

		#self.trainingdata= [(article.Title, article.Label) for article in articles]
		self.classifier=Bayes()

		for item in articles:
			print "Title: ", item.Title, "Label: ", item.Label
			#tup = (item.Content, item.Label)  # tup is a 2-element tuple
			self.classifier.train(item.Title, item.Label)
		#self.classifier = nltk.NaiveBayesClassifier.train(self.learn_data)
		self.classifier.save(classifier_data)
		#self.classifier.train(self.learn_data)


def save_all_articles():
	articles_file=open(export_file,'w')
	pickle.dump(articles, articles_file)
	#for article in articles:
	#	articles_file.writelines((article.Title , article.Content))
	if debug==True: print "\n articles dumped"
def open_all_articles():
	articles_file=open(import_file,'r')
	articles=pickle.load(articles_file)
	##debug
	debug_mode("articles re-read")
	debug_mode(articles)

def test():
	#open_all_articles()
	testtext2=(u"While Netflix and others work on new ways to stream movies to your browser through HTML5 that don't use Flash or Silverlight plugins, Hollywood's requirements for DRM to prevent copying have put Mozilla in a bind. The DRM proposed means user's don't know exactly what's going on their machines or if it's violating their privacy, but without it Firefox will eventually be locked out of streaming most movies and TV shows. As a result, Mozilla announced plans to roll it out in the next few months on Windows, Mac and Linux versions of the browser, so one upside could be official Netflix support on Linux.")
	testtext=(u'Wie viel beispielsweise von den drei Millionen Dollar, die Osama bin Laden 2002 angeblich für gleichgesinnte Organisationen in Afrika verteilen ließ, bei Boko Haram angekommen sind, ist fraglich. Ebenso, wie viel aus welcher Verbindung heute noch in ihre Taschen fließt und wie viele Anhänger etwa in Somalia, in Libyen noch unter Gaddafi, in Afghanistan oder anderen Ländern trainiert wurden. Ein Motiv für andere Gruppen, den nigerianischen Terror zu unterstützen: Sie haben ein Interesse daran, sich sichere Rückzugs- oder Fluchtorte zu schaffen. Darüber hinaus soll Boko Haram Geld von der in London sitzenden Hilfsorganisation Al-Muntada Trust Fund oder der saudi-arabischen Islamic World Society erhalten haben.')
	#testtext2=fuck_unicode(testtext2)
	for i in range(1,25):
		articles.append(RSSitem(i, "Dies ist ein Test Titel", unicode(testtext),"query_starred") )
		articles.append(RSSitem(i, "Das ist der Bart von Merkel", unicode(testtext2),"query_read") )
		debug_mode(" article " +  unicode(i+1) +" added")


test()

trainer=train()
save_all_articles()
print "testing classifier: \n"
classifier=Bayes()
classifier.load(classifier_data)
for article in articles:
	print article.Title ,classifier.guess(article.Title)
