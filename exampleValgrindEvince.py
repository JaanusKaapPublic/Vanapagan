import os 
import time
import subprocess
from Vanapagan.Detector.LinuxValgrind import LinuxValgrind
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging
from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping

count = 0
crashes = 0
log = FilesystemLoging()
run = LinuxValgrind()
mut = FileBitFlipping()
mut.rate=12000



while True:
	try:
		for f in os.listdir("./input"):
			desc = mut.mutate("./input/" + f, "/home/jaanus/MysTuff/0day/__share__/Test/Vanapagan/test.pdf")
			run.run(["/usr/bin/evince", "/home/jaanus/MysTuff/0day/__share__/Test/Vanapagan/test.pdf"])
			crash = run.waitForCrash(30)
			if crash != None:
				crashes += 1
				print "Something happened at %s!!!" % crash.location
				log.log("/home/jaanus/MysTuff/0day/__share__/Test/Vanapagan/test.pdf", crash, desc)	
			run.close(False)

			count += 1
			if count % 5 == 0:
				print "Done %d reps, found %d crashes" % (count, crashes)
	except:
		raise
