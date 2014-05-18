#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pickle
from helpers import *
#from nltk import FreqDist
#import sqlite3

from article import Article
from db_manager import Database_Manager

class Article_manager(object):
	def __init__(self):
		self.articles_list=[]
		self.start_database()
		self.collect_articles("starred")

	def start_database(self):
		debug_mode("starting database",1)
		self.database = Database_Manager()
		self.database.start()



	def collect_articles(self, query_request):
		self.start_database()
		if self.database.connected == True:
			debug_mode("Database is connected, collecting articles",2)
			number_ids= self.database.read_number_ids(query_request)
			for query_outgoing in range(0, number_ids):
				requested_data= self.database.read_content( query_request,  query_outgoing)
				tmp_article=Article(requested_data)
				print requested_data
				self.articles_list.append(tmp_article)



	def create_bag_of_words(self):
		self.bag_of_words =[]




	def save_all_articles(self):
		articles_file=open("articles.txt",'w')
		for article in articles: pickle.dump(article, articles_file)
		if debug==True: print "articles dumped"

	def open_all_articles(self):
		articles_file=open("articles.txt",'r')
		articles=pickle.load(articles_file)
		debug_mode("articles re-read")
		debug_mode(articles)

article_man=Article_manager()
