import os 
import time
import subprocess
import sys
from Vanapagan.Detector.AndroidAdb import AndroidAdb
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging
from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping

count = 0
crashes = 0
notNull = 0 
log = FilesystemLoging()
run = AndroidAdb(deviceTmpFile = "/sdcard/Tmp/test.pdf")
mut = FileBitFlipping()
mut.rate=12000

if len(sys.argv)>1:
	run.device = sys.argv[1]

while True:
	try:
		for f in os.listdir("./input"):
			desc = mut.mutate("./input/" + f, "/home/jaanus/MysTuff/0day/__share__/Test/Vanapagan/test.pdf")
			run.run("com.foxit.mobile.pdf.lite/com.fuxin.read.RD_ReadActivity", "/home/jaanus/MysTuff/0day/__share__/Test/Vanapagan/test.pdf")
			crash = run.waitForCrash(5)
			if crash != None:
				crashes += 1
				if not crash.nearNull:
					notNull += 1
				print "##########Something happened in %s###########" % crash.location
				log.log("/home/jaanus/MysTuff/0day/__share__/Test/Vanapagan/test.pdf", crash, desc)	
			run.close()

			count += 1
			if count % 5 == 0:
				print "######Done %d reps, found %d crashes (%d not null)" % (count, crashes, notNull)
	except:
		raise
