from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.Mutator.FileByteValues import FileByteValues

#test = WinBasic()
#test.run(['calc'])
#rep = test.waitForCrash(10, True)
#if rep != None:
#	print rep.getInfo()
#test.close()
test = FileByteValues()
print test.mutate("test.txt", "output.txt")