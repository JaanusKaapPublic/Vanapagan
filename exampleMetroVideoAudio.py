########################
#Simple example how to fuzz Win10 Metro apps (MS provided audio and video player apps)
#After detecting the crash, the fuzzer runs same input 4 times again to be sure the crash was not random
#Recommend gflags full page heap for processes Video.UI.exe and WWAHost.exe
#########################

import os 
import time
import subprocess
from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.CrashReport import CrashReport
from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging
from Vanapagan.Utils.WinUtils import *


desc = None
count = 0
first = 0
log = FilesystemLoging()
log.dir = "\\\\vboxsrv\\__share__\\crashesMedia"
run = WinBasic()
mut = FileBitFlipping()
mut.rate=50000



while True:
	try:
		for f in os.listdir("c:/Work/input"):
			while True:
				extension = os.path.splitext(f)[1]
				if first == 0:
					while True:
						try:
							desc = mut.mutate("c:/Work/input/" + f, "c:/Work/test" + extension)
							break
						except:
							time.sleep(1)
				else:
					time.sleep(4)
				proc1 = subprocess.Popen(["cmd", "/c","start c:/Work/input/" + f], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					
				pid = 0
				countFailure = 0
				while True:
					pid = getPidByImg("Video.UI.exe")
					if pid != 0:
						break
					pid = getPidByImg("WWAHost.exe")
					if pid != 0:
						break
					countFailure += 1
					if countFailure > 10:
						killByPid(proc1.pid)					
						raise Exception("Fuck it")
					time.sleep(1)
				
				run.attachPid(pid)			
				proc2 = subprocess.Popen(["cmd", "/c","start c:/Work/test" + extension], stdout=subprocess.PIPE, stderr=subprocess.PIPE)			
				crash = run.waitForCrash(6)
				run.close()
				if crash != None:
					if first == 4:
						print "Issue detected at %s" % crash.location
						log.log("c:/Work/test" + extension, crash, desc)
						first = 0
					else:
						first += 1
				else:
					first = 0
			
				killByImg("Video.UI.exe")
				killByImg("WWAHost.exe")
				killByPid(proc1.pid)
				killByPid(proc2.pid)
			
				count += 1
				if count % 5 == 0:
					print "Done %d reps" % count					
					
				if first == 0:
					break
	except:
		killByImg("MicrosoftEdge.exe")
		killByImg("Video.UI.exe")
		killByImg("WWAHost.exe")
		time.sleep(10)