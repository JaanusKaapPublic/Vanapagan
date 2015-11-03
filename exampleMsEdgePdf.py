########################
#Simple example how to fuzz MS Edge (native pdf reader part) with crash detection by Windows events
#After detecting the crash, the fuzzer runs same input again to be sure the crash was not random
#Recommend gflags full page heap for processes MicrosoftEdge.exe and MicrosoftEdgecp.exe
#
#NB: It is not 100% stable, usually between 10K and 20K of testcases, the Windows doesn't want 
#  to work anymore (errors about startup and stuff crashing). Don't know exact reason yet
#########################

import os 
import time
import subprocess
from Vanapagan.CrashReport import CrashReport
from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging
from Vanapagan.Utils.WinUtils import *


count = 0
proc = None
first = True
log = FilesystemLoging()
log.dir = "\\\\vboxsrv\\__share__\\crashesEdge"
mut = FileBitFlipping()
mut.rate=12000



while True:
	try:
		for f in os.listdir("c:/Work/input"):
			extension = os.path.splitext(f)[1]
			if first:
				while True:
					try:
						desc = mut.mutate("c:/Work/input/" + f, "c:/Work/test" + extension)
						break
					except:
						time.sleep(1)
			else:
				time.sleep(4)
					
			while getPidByImg("MicrosoftEdge.exe")!=0:
				time.sleep(1)
				
			clearEvents()
			proc = subprocess.Popen(["cmd", "/c","start c:/Work/test" + extension], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			time.sleep(5)
			killByImg("MicrosoftEdge.exe")
			killByPid(proc.pid)
			
			crash = isEvent()
			if crash != None:
				if first:
					first = False
				else:
					log.log("c:/Work/test.pdf", crash, desc)
					print "Issue detected!"
					first = True
			else:
				first = True
			
			count += 1
			if count % 5 == 0:
				print "Done %d reps" % count
	except:
		raise
		killByImg("MicrosoftEdge.exe")
		time.sleep(1)

