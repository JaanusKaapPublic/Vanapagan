########################
#Simple example how to fuzz Win10 Metro apps (MS provided audio and video player apps)
#After detecting the crash, the fuzzer runs same input 4 times again to be sure the crash was not random
#Recommend gflags full page heap for processes Video.UI.exe and WWAHost.exe
#########################

from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping
from Vanapagan.Mutator.FileByteRepetition import FileByteRepetition
from Vanapagan.Mutator.FileByteValues import FileByteValues
from Vanapagan.Mutator.XmlBitFlipping import XmlBitFlipping
from Vanapagan.Mutator.XmlByteValues import XmlByteValues


mut1 = FileBitFlipping()
mut2 = FileByteRepetition()
mut3 = FileByteValues()
mut4 = XmlBitFlipping()
mut5 = XmlByteValues()


print mut1.mutate("input.txt", "output1.txt")
print mut2.mutate("input.txt", "output2.txt")
print mut3.mutate("input.txt", "output3.txt")
print mut4.mutate("input.txt", "output4.txt")
print mut5.mutate("input.txt", "output5.txt")
