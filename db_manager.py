#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import MySQLdb
from helpers import *

class Mysql_Manager(object):
	'management class for the database. It processes requests from the article manager and  establishes a connection to the database, based data from the  configuration file.'

	def start(self):
		debug_mode( "mysql_manager started" )
		self.var_db_prefix=config.get('server','database_prefix')

		self.connected=False
		self.connect_database()


	def connect_database(self):
		debug_mode( "connecting to database" )
		try:
			self.ttrss_db = MySQLdb.connect(host=config.get('server', 'host'),
								  user=config.get('server','user'),
			                      passwd=config.get('server','password'),
			                      db=config.get('server','database')
			                      )
			debug_mode( "connection established" )
			self.db_cursor = self.ttrss_db.cursor()
			self.queries = {
			"starred" : ("SELECT ref_id FROM  "+self.var_db_prefix+"user_entries WHERE (marked = 1) OR (published = 1)"),
			"read" : ("SELECT ref_id FROM " +self.var_db_prefix+"user_entries WHERE (marked = 0) AND (published = 0) AND (unread = 0) "),
			"unread" : ("SELECT ref_id FROM "+self.var_db_prefix+"user_entries WHERE (score = '0')")
			}
			self.connected=True
		except:
			debug_mode("connection failed")
			self.connected=False

	def read_number_ids(self,query_type):
		#Database queries dictionary
		number_ids=self.db_cursor.execute(self.queries[query_type])	 #get number of user entries
		self.db_cursor.fetchall()
		return number_ids

	def read_content(self, query_request, entry_id):
		'returns a dictionary of values from the database'
		__entry_id__=entry_id
		__label__=  query_request
		__query_request__ = self.queries[__query_request__]

		debug_mode("getting content " + __query_request__ )

		self.query_entry= ("SELECT id, title, content FROM " +self.var_db_prefix+"entries WHERE (id="+ str(__entry_id__) +")")
		self.db_cursor.execute(__query_request__)
		self.content_tmp=self.db_cursor.fetchall()
		try:
		#	write to a dictionary being passed through
		#	articles.append(RSSitem( [entry_id, self.content_tmp[0][0],self.content_tmp[0][1],self.label] ) )
			labels= dict('id', 'title', 'content','label')
			tmp_count=0
			for item in labels:
				if item==__label__: labels[item]=__label__
				else:
					item= self.content_tmp[0][tmp_count]
					tmp_count+=1
			return labels

		except:
			return {'label': None}

	def write_score(self):
		return

debug_mode("Test")
database=Mysql_Manager()
database.start()
print "number of id's in requested database: " + str( database.read_number_ids("starred") )
print database.read_content("starred", 1)
