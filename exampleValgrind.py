from Vanapagan.Detector.LinuxValgrind import LinuxValgrind
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging

log = FilesystemLoging()
run = LinuxValgrind()


run.run(['./Crash'])
crash = run.waitForCrash(4)
if crash != None:
	log.log("./Readme.txt", crash, "TEST")
