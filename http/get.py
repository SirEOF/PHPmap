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

from bs4 import BeautifulSoup
import urllib2, base64

class HTTP:	
	def getPage(self,url,basic,cookie):
		request = urllib2.Request(url)
		if (basic is not None and cookie is None):
			try:
				request.add_header("Authorization", "Basic %s" % base64.b64encode("%s:%s" % (basic.split(":")[0],basic.split(":")[0])).replace("\n",""))
			except:
				print "[*] userpass not in valid format (ex username:password)"
		elif (cookie is not None and basic is None):
			try:
				request.add_header('Cookie', cookie)
			except:
				print "[*] cookie not in valid format"
		elif (cookie is not None and basic is not None):
			print "[*] can not use Cookie(s) and Basic Auth at the same time"
		try:
			page = urllib2.urlopen(request)
			try:
				soup = BeautifulSoup(markup=page.read(),features='html')
			except:
				print "[*] could not parse page"
				soup = 0
		except:
			print "[*] error grabbing page.."
			soup = 0
			
		if (soup is not 0): return soup
		else: return 0