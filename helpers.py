#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.cfg')
debug_enabled=config.getboolean('debug', 'debug_enabled')

def debug_mode(text):
	if debug_enabled==True:
		#if type(text) == 'str':
		#	print text
		#else: return text
		try:
			print text
		except:
			return text

debug_mode("config read")
