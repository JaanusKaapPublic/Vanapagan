import os 
import time
import subprocess
from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging
from Vanapagan.Utils.WinUtils import *
from Vanapagan.Utils.ZipFiles import *


count = 0
log = FilesystemLoging()
log.dir = "c:/Fuzz/crashAdobe"
run = WinBasic()
mut = FileBitFlipping()
mut.rate=8000


up = zip_unpack("Test.zip", "./Test")
print up
for x in xrange(50):
	print "%02d: %s" % (x, zip_randFile(up))


#while True:
#	try:
#		for f in os.listdir("c:/Fuzz/input"):
#			while True:
#				try:
#					desc = mut.mutate("c:/Fuzz/input/" + f, "c:/Fuzz/test.pdf")
#					break
#				except:
#					time.sleep(1)
#				
#			#clearEvents()
#			#subprocess.Popen(["C:\\Program Files\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe", "c:\\Fuzz\\test.pdf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#			subprocess.Popen(["C:\\Program Files\\Foxit Software\\Foxit Reader\\FoxitReader.exe", "c:\\Fuzz\\test.pdf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#			time.sleep(8)
#			killByImg("FoxitReader.exe")
#			if isEvent():
#				log.log("c:/Fuzz/test.pdf", "CRASHED :(", desc)
#				print "Issue detected!"
#			
#			count += 1
#			if count % 5 == 0:
#				print "Done %d reps" % count
#	except:
		#raise
#		killByImg("FoxitReader.exe")
#		time.sleep(1)


#while True:
#	for f in os.listdir("c:/Fuzz/input"):
#		clearEvents()
#		os.system("c:\\Work\\Fuzzers\\Vanapagan\\Crash.exe")
#		if isEvent():
#			print "CRASH"
			

#while True:
#	for f in os.listdir("c:/Fuzz/input"):
#		desc = mut.mutate("c:/Fuzz/input/" + f, "c:/Fuzz/test.pdf")
#		run.run(["C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe", "c:/Fuzz/test.pdf"])
#		crash = run.waitForCrash(6)
#		run.close()
#		if crash != None:
#			log.log("c:/Fuzz/test.pdf", crash, desc)
#			print "Issue detected at %s" % crash.location
#		
#		count += 1
#		if count % 5 == 0:
#			print "Done %d reps" % count


#test.run(['crash'])
#rep = test.waitForCrash(10, True)

#if rep != None:
#	print rep.getInfo()
#	log.log("test.txt", rep, "SOME CHANGES IN FILE")
#test.close()
#test = FileByteValues()
#xxx = test.mutate("test.txt", "output.txt")
#print xxx
#test.restore("output.txt", "output2.txt", xxx.split("\n")[0].split("|")[0])