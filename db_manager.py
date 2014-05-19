#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import MySQLdb
import MySQLdb.cursors
from helpers import *

class Database_Manager(object):
	'management class for the database. It processes requests from the article manager and  establishes a connection to the database, based data from the  configuration file.'

	def __init__(self, thread_id=0):
		self.thread_id=thread_id
		debug_mode( "mysql_manager started" ,0 )
		self.var_db_prefix=config.get('server','database_prefix')

		self.connected=False
		self.connect_database()
		self.disconnect_database()

	def disconnect_database(self):
		self.ttrss_db.close()
		debug_mode("connection closed",3)


	def connect_database(self):
		'connects to the mysql database, based on the configuration file with detailed connection to a local/remote host or on a local server with data from my.conf'
		common_parameters= " use_unicode = 'True'  my_conv= {id : int, score : int, content: unicode, title : unicode} "

		if config.get('server','use_my_cfg') == True:
			debug_mode( "connecting to database with my.cnf" ,3 )
			self.ttrss_db = MySQLdb.connect(host=config.get('server', 'host'),
											db=config.get('server','database'),
											read_default_file="~/.my.cnf"
											)

		else:
			debug_mode( "connecting to database with login data from config" ,3 )
			self.ttrss_db = MySQLdb.connect(host=config.get('server', 'host'),
											user=config.get('server','user'),
											passwd=config.get('server','password'),
											db=config.get('server','database')##,
											#port=int (config.get('server','port') )
											)
		debug_mode( "connection established" ,3)
		#self.db_cursor = self.ttrss_db.cursor()
		self.db_cursor = self.ttrss_db.cursor()

		self.connected=True
		return self.connected

	def read_number_ids(self,query_request):
		'returns the number of entries in given database'
		number_ids=self.db_cursor.execute(self.queries[query_request])	 #get number of user entries
		self.db_cursor.fetchall()
		return number_ids

	def read_content(self, query_incoming, entry_id):
		'returns a dictionary of values from the database for the requested id and incoming query'

		query_request = self.queries[query_incoming]

		self.read_number_ids(query_incoming)

		debug_mode("getting content " + query_incoming ,3 )

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


		return

#### rewrite of above functions ###

    ##maybe it is possible to handle all of the three following fucntions, due the fact that translate_request handles them all
    ##so there is only the need to handle the read/write head (in future possible a sub_class, depending on benchmarks)
    ##quick and dirty tuturial: http://ianhowson.com/a-quick-guide-to-using-mysql-in-python.html
	def write_to_table(self, selector_list, content_list):
		'this function handles common reading, writing and updating of tables including the database head'

		#1) execute (select db rows )
		#2) execute ( select content to read/write)
		#3) if read command -> cursor.fetchall()
		return fetchoneDict(c)

	def translate_request(self,request, article_id):
		'translates requests from article manager to mysql selectors based on request type (write,read,update) '
		request_translations={} #update, read,write
		self.queries = {
			"score" :( "UPDATE " + self.var_db_prefix + "user_entries SET score = " + str(score) +" WHERE ref_id =  " + str(entry_id) ),
			"starred" : ("SELECT ref_id FROM  "+self.var_db_prefix+"user_entries WHERE (marked = 1) OR (published = 1)"),
			"read" : ("SELECT ref_id FROM " +self.var_db_prefix+"user_entries WHERE (marked = 0) AND (published = 0) AND (unread = 0) "),
			"unread" : ("SELECT ref_id FROM "+self.var_db_prefix+"user_entries WHERE (score = '0')"),
			"content" : ("SELECT id, title, content FROM " +self.var_db_prefix+"entries WHERE (id="+ str(entry_id) +")"),
			}
		translations= { 'read' : 'SELECT',
						'write' : 'UPDATE',
						'standard1' : ('ref_id FROM ' + self.var_db_prefix + 'user entries WHERE' ),
						'starred' : ('(marked = 1) OR (published = 1)' ),
						'read' : ('(marked = 0) AND (published = 0) AND (unread = 0)' ),
						'unread' : (' score = 0' ),
						'score' : ('SET score = ' + int(content) )
					}
		return

#### usage reference:
database=Database_Manager()
#database.start()
#debug_mode( "number of id's in requested database: " + str( database.read_number_ids("starred") ),4 )
#print database.read_content("read", 3)
