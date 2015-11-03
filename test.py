import os 
import time
import subprocess
from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.Mutator.FileBitFlipping import FileBitFlipping
from Vanapagan.Mutator.XmlBitFlipping import XmlBitFlipping
from Vanapagan.Loging.FtpsLoging import FtpsLoging
from Vanapagan.Utils.WinUtils import *
from Vanapagan.Utils.ZipFiles import *


count = 0
log = FtpsLoging("HOST", "USERNAME", "PASSWORD")
run = WinBasic()
mut = XmlBitFlipping()
mut.rate=80000


run.run(['crash'])
crash = run.waitForCrash(10, True)
if crash != None:
	log.log("./Readme.txt", crash, "TEST")
