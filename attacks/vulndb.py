#--
#
# Description:
#       This tool is used to exploit poorly sanitized user input in PHP 
#       web applications. 
#
#       Author: Level @ CORE Security Technologies, CORE SDI Inc.
#       Email: level@coresecurity.com
#
#
# Copyright (c) CORE Security, CORE SDI Inc.
# All rights reserved.
#
# This computer software is owned by Core SDI Inc. and is
# protected by U.S. copyright laws and other laws and by international
# treaties.  This computer software is furnished by CORE SDI Inc.
# pursuant to a written license agreement and may be used, copied,
# transmitted, and stored only in accordance with the terms of such
# license and with the inclusion of the above copyright notice.  This
# computer software or any other copies thereof may not be provided or
# otherwise made available to any other person.
#
#
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED. IN NO EVENT SHALL CORE SDI Inc. BE LIABLE
# FOR ANY DIRECT,  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY OR
# CONSEQUENTIAL  DAMAGES RESULTING FROM THE USE OR MISUSE OF
# THIS SOFTWARE
#
#--

import sqlite3

class VulnDB:
	def connect(self):
		conn = sqlite3.connect('attacks\phpmap3.db')
		cursor = conn.cursor()
		return conn,cursor
		
	def is_vuln(self,type,**kwargs):
		conn,cursor = self.connect()
		if (type == 'form') or (type == 'crawl'):
			for key in kwargs:
				if (key == 'url'): url = kwargs[key]
				if (key == 'param'): param = kwargs[key]
				if (key == 'originalvalue'): originalValue = kwargs[key]
				if (key == 'payload'): payload = kwargs[key]
				if (key == 'formName'): formName = kwargs[key]
				if (key == 'method'): method = kwargs[key]	
		if (type == 'get'):
			for key in kwargs:
				if (key == 'url'): url = kwargs[key]
				if (key == 'param'): param = kwargs[key]
				if (key == 'originalvalue'): originalValue = kwargs[key]
				if (key == 'payload'): payload = kwargs[key]
				formName = "url"
				method = type
		cursor.execute("SELECT * FROM vulndb WHERE url = ?", [url])
		result = cursor.fetchone()
		if result:
			return True, result
		else:
			return False, None
		
	def new_vuln(self,type,**kwargs):
		conn,cursor = self.connect()
		if (type == 'form') or (type == 'crawl'):
			for key in kwargs:
				if (key == 'url'): url = kwargs[key]
				if (key == 'param'): param = kwargs[key]
				if (key == 'originalvalue'): originalValue = kwargs[key]
				if (key == 'payload'): payload = kwargs[key]
				if (key == 'formName'): formName = kwargs[key]
				if (key == 'method'): method = kwargs[key]	
		if (type == 'get'):
			for key in kwargs:
				if (key == 'url'): url = kwargs[key]
				if (key == 'param'): param = kwargs[key]
				if (key == 'originalvalue'): originalValue = kwargs[key]
				if (key == 'payload'): payload = kwargs[key]
				formName = "url"
				method = type
		cursor.execute("INSERT INTO vulndb VALUES (?,?,?,?,?,?)", (url,param,originalValue,payload,formName,method))
		conn.commit()
		conn.close()
		return
		
	def clear_vulns(self):
		conn,cursor = self.connect()
		cursor.execute("DELETE from vulndb")
		conn.commit()
		conn.close()
		return
		