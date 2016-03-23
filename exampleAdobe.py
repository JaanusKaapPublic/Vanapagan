########################
#Simple example how to fuzz Win10 Metro apps (MS provided audio and video player apps)
#After detecting the crash, the fuzzer runs same input 4 times again to be sure the crash was not random
#Recommend gflags full page heap for processes Video.UI.exe and WWAHost.exe
#########################

import os 
import time
import subprocess
import psutil
from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.CrashReport import CrashReport
from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging


desc = None
count = 0
crashes = 0
crashCheck = 0
log = FilesystemLoging()
log.dir = "c:/Work/crashes"
run = WinBasic()
mut = FileBitFlipping()
mut.rate=40000
start = time.time()


def killAll():
	proc = subprocess.Popen(["cmd", "/c","taskkill /f /im AcroRd32.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()


while True:
	for f in os.listdir("c:/Work/input"):
		try:
			x = 0
			while True:
				try:
					desc = mut.mutate("c:/Work/input/" + f, "c:/Work/test1.pdf")
					break
				except:
					if x>10:
						raise
					if x>5:
						killAll()
					time.sleep(1)
					x+=1
		
					
			while True:					
				run.run(["C:\\Program Files\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe", "/n", "/s", "/o", "/h", "c:/Work/test1.pdf"])			
				#crash = run.waitForCrash(12)
				crash = None
				for x in xrange(12 + (crashCheck*3)):
					psutil.cpu_percent()
					crash = run.waitForCrash(1)
					usage = psutil.cpu_percent()
					if crash != None:
						break
					if usage<8.0:
						break
				run.close()
				killAll()
				if crash != None:
					if crashCheck == 3:
						crashes += 1
						print "Issue detected at %s" % crash.location
						log.log("c:/Work/test1.pdf", crash, desc)
						crashCheck = 0
						break
					else:
						crashCheck += 1
						time.sleep(4)
						continue
				else:
					crashCheck = 0
				break
				
			count += 1
			if count % 10 == 0:
				ratio = (time.time()-start)/count
				print "Done %d reps (%d crashes) - 1 rep per %f seconds (%d per 24h)" % (count, crashes, ratio, 60*60*24/ratio)
		except:
			raise
			killAll()
			time.sleep(10)