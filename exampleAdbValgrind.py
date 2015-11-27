import os 
import time
import subprocess
import sys
from Vanapagan.Detector.AndroidAdbValgrind import AndroidAdbValgrind
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging
from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping

myNr = "MY"
count = 0
crashes = 0
notNull = 0 
log = FilesystemLoging()
log.dir = "./crashesAdobeReader"
run = AndroidAdbValgrind(deviceTmpFile = "/sdcard/Tmp/test.pdf")
mut = FileBitFlipping()
mut.rate=12000

if len(sys.argv)>1:
	run.device = sys.argv[1]
if len(sys.argv)>2:
	myNr = sys.argv[2]

while True:
	try:
		for f in os.listdir("./input"):
			desc = mut.mutate("./input/" + f, "./test_" + myNr + ".pdf")
			run.run("com.adobe.reader/com.adobe.reader.AdobeReader", "./test_" + myNr + ".pdf")
			crash = run.waitForCrash(60)
			if crash != None:
				crashes += 1
				if not crash.nearNull:
					notNull += 1
				print "##########Something happened in %s###########" % crash.location
				log.log("./test_" + myNr + ".pdf", crash, desc)	
			run.close()

			count += 1
			if count % 5 == 0:
				print "######Done %d reps, found %d crashes (%d not null)" % (count, crashes, notNull)
	except:
		raise
