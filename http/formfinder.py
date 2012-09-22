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

import urllib2, os, sys
from bs4 import BeautifulSoup
if (os.name == 'nt'):
	for loc, dir, fn in os.walk(os.getcwd()):
		for d in dir: 
			if d is not []: 
				sys.path.append(os.path.join(os.getcwd()+'\\'+d))
else:
	for loc, dir, fn in os.walk(os.getcwd()):
		for d in dir: 
			if d is not []: 
				sys.path.append(os.path.join(os.getcwd()+'/'+d))
import get

class FRMFind:
	def search(self,url,basic,cookie):
		results_get,results_post = {},{}
		soup = get.HTTP().getPage(url,basic,cookie)
		if soup is 0:
			return None,None
		for formTag in soup.findAll('form'):
			if formTag.has_key('action'):
				if (formTag['action'] != "#"):
					if formTag.has_key('method') and formTag['method'] == "post":
						for i in xrange(0,len(soup.findAll('form'))):
							for inputTag in soup.findAll('form')[i].findAll('input'):
								try:
									try:
										results_post[formTag['action']+str(i)] = {inputTag['name']:inputTag['value']}
									except:
										continue
								except:
									try:
										results_post[formTag['action']+str(i)] = {inputTag['name']:0}
									except:
										continue
					else:
						for i in xrange(0,len(soup.findAll('form'))):
							for inputTag in soup.findAll('form')[i].findAll('input'):
								try:
									results_get[formTag['action']+str(i)] = {inputTag['name']:inputTag['value']}
								except:
									try:
										results_get[formTag['action']+str(i)] = {inputTag['name']:0}
									except:
										continue
								i+=1
		return results_get,results_post