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

import sys,os
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

class Crawl:
	def crawl(self,url,depth,restrict,basic,cookie):
		soup = get.HTTP().getPage(url,basic,cookie)
		globalqueue,urlqueue = [],[]
		for formTag in soup.findAll('a'):
			if formTag.has_key('href') and (formTag['href'] != "#"):
					if (restrict is not None):
						if (restrict not in formTag['href']):
							urlqueue.append(formTag['href'])
						else:
							continue
					else:
						urlqueue.append(formTag['href'])
		for urli in urlqueue:
			soup = get.HTTP().getPage(urli,basic,cookie)
			if soup is not 0:
				for formTag in soup.findAll('a'):
					if formTag.has_key('href') and (formTag['href'] != "#"):
						if (restrict is not None):
							if (restrict not in formTag['href']):
								globalqueue.append(formTag['href'])
							else:
								continue
						else:
							globalqueue.append(formTag['href'])	
		dupeFilter = []					
		for url in globalqueue:
			if url not in dupeFilter:
				dupeFilter.append(url)
		return dupeFilter
