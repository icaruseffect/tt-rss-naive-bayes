#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import MySQLdb
from helpers import *

class Database_Manager(object):
	'management class for the database. It processes requests from the article manager and  establishes a connection to the database, based data from the  configuration file.'

	def start(self):
		debug_mode( "mysql_manager started" )
		self.var_db_prefix=config.get('server','database_prefix')

		self.connected=False
		self.connect_database()


	def connect_database(self):
		'connects to the mysql database'
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
			"unread" : ("SELECT ref_id FROM "+self.var_db_prefix+"user_entries WHERE (score = '0')"),
			}

			self.connected=True
		except:
			debug_mode("connection failed")
			self.connected=False
		return self.connected

	def read_number_ids(self,query_request):
		#Database queries dictionary
		number_ids=self.db_cursor.execute(self.queries[query_request])	 #get number of user entries
		self.db_cursor.fetchall()
		return number_ids

	def read_content(self, query_incoming, entry_id):
		'returns a dictionary of values from the database for the requested id and incoming query'

		query_request = self.queries[query_incoming]
		self.read_number_ids(query_incoming)

		debug_mode("getting content " + query_incoming)

		query_entry= ("SELECT id, title, content FROM " +self.var_db_prefix+"entries WHERE (id="+ str(entry_id) +")")
		self.db_cursor.execute(query_entry)
		self.content_tmp=self.db_cursor.fetchall()

		try:
			labels= {
			'id' :int(self.content_tmp[0][0]),
			'title': unicode(self.content_tmp[0][1]),
			'content': unicode(self.content_tmp[0][2]),
			'label' : query_incoming
			}

		except:
			labels = {'label': None}
		return labels

	def write_score(self,entry_id, score=0):
		query_entry = ( "UPDATE "+ str(config.get('server','database') ) + "." + self.var_db_prefix + "user_entries SET score = " + str(score) +" WHERE ref_id =  " + str(entry_id) )



		return

#### usage reference:
#database=Mysql_Manager()
#database.start()
#print "number of id's in requested database: " + str( database.read_number_ids("starred") )
#print database.read_content("read", 3)
