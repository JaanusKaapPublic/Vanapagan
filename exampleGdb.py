########################
#Very simple "fuzzer" for detecting and reporting crash in always crashing elf file
#
#NB: Crash file is 64bit
#########################
from Vanapagan.Detector.LinuxGdb import LinuxGdb
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging

log = FilesystemLoging()
run = LinuxGdb()


run.run(['./Crash'])
crash = run.waitForCrash(4)
if crash != None:
	log.log("./Readme.txt", crash, "TEST")
