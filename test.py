from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.Mutator.FileByteValues import FileByteValues

#test = WinBasic()
#test.run(['calc'])
#rep = test.waitForCrash(10, True)
#if rep != None:
#	print rep.getInfo()
#test.close()
test = FileByteValues()
xxx = test.mutate("test.txt", "output.txt")
print xxx
test.restore("output.txt", "output2.txt", xxx.split("\n")[0].split("|")[0])