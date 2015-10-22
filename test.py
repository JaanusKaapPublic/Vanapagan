from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.Mutator.FileByteValues import FileByteValues
from Vanapagan.Loging.FilesystemLoging import FilesystemLoging

log = FilesystemLoging()
test = WinBasic()
test.run(['crash'])
rep = test.waitForCrash(10, True)

if rep != None:
	print rep.getInfo()
	log.log("test.txt", rep, "SOME CHANGES IN FILE")
#test.close()
#test = FileByteValues()
#xxx = test.mutate("test.txt", "output.txt")
#print xxx
#test.restore("output.txt", "output2.txt", xxx.split("\n")[0].split("|")[0])