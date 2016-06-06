from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging


log = FilesystemLoging()
run = WinBasic()


run.run(['crash'])
crash = run.waitForCrash(10, True)
if crash != None:
	log.log("./Readme.txt", crash, "TEST")
