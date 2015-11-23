from ..CrashReport import CrashReport
import time
import select
import subprocess

class AndroidAdb:
	adbExecutable = "adb"
	deviceTmpFile = "/sdcard/Tmp/test"	
	package = "???"
	mainProc = None
	
	def __init__(self, adbExecutable = None, deviceTmpFile = None):
		if adbExecutable != None:
			self.adbExecutable = adbExecutable
		if deviceTmpFile != None:
			self.deviceTmpFile = deviceTmpFile		
			
		
	def run(self, package, testFile):
		self.package = package
		subprocess.call([self.adbExecutable, "push", testFile, self.deviceTmpFile])
		subprocess.call([self.adbExecutable, "shell", "logcat", "-c"])
		subprocess.call([self.adbExecutable, "shell", "am", "start", "-d", "file://" + self.deviceTmpFile, "-n", package])
				
	def waitForCrash(self, waitTime = 4):
		time.sleep(waitTime)
		result = subprocess.check_output("adb shell logcat -d *:F", shell=True)
		
		if "(SIG" in result:		
			report = CrashReport()
			report.location = "UNKNOWN"
			report.faultAddr = "UNKNOWN"
			report.code = "UNKNOWN"
			report.nearNull = True
			report.type = "UNKNOWN"
			report.stack = "UNKNOWN"
			report.info = result
						
			#Can we find some more data
			lines = result.split("\n")
			for x in xrange(len(lines)):
				if "(SIG" in lines[x]:
					cols = lines[x].split(" ")
					if len(cols)>0:
						report.location = cols[0].replace("/", ".").replace(":", ".")
						
					if "(SIGSIGSEGV" in lines[x]:
						pos1 = lines[x].find("0x")
						pos2 = lines[x].find(" (code=")
						addr = int(lines[x][pos1:pos2])
						if addr > 4095:
							report.nearNull = False
			return report		
		return None
				
	def close(self):
		subprocess.call([self.adbExecutable, "shell", "am", "force-stop", self.package[0:self.package.find('/')]])		
