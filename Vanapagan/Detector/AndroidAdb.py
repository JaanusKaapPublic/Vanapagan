from ..CrashReport import CrashReport
import time
import select
import subprocess
import tempfile
import os

class AndroidAdb:
	adbExecutable = "adb"
	deviceTmpFile = "/sdcard/Tmp/test"	
	device = None
	package = "???"
	mainProc = None
	
	def __init__(self, adbExecutable = None, deviceTmpFile = None, device = None):
		if adbExecutable != None:
			self.adbExecutable = adbExecutable
		if deviceTmpFile != None:
			self.deviceTmpFile = deviceTmpFile		
		if device != None:
			self.device = device		
			
		
	def run(self, package, testFile):
		self.package = package
		if self.device == None:
			subprocess.call([self.adbExecutable, "push", testFile, self.deviceTmpFile])
			subprocess.call([self.adbExecutable, "shell", "logcat", "-c"])
			subprocess.call([self.adbExecutable, "shell", "su", "-c","rm /data/tombstones/*"])
			subprocess.call([self.adbExecutable, "shell", "am", "start", "-a" "android.intent.action.VIEW", "-n", package, "file://" + self.deviceTmpFile])
		else:
			subprocess.call([self.adbExecutable, "-s", self.device, "push", testFile, self.deviceTmpFile])
			subprocess.call([self.adbExecutable, "-s", self.device, "shell", "logcat", "-c"])
			subprocess.call([self.adbExecutable, "-s", self.device, "shell", "su", "-c","rm /data/tombstones/*"])
			subprocess.call([self.adbExecutable, "-s", self.device, "shell", "am", "start", "-a" "android.intent.action.VIEW", "-n", package, "file://" + self.deviceTmpFile])
				
	def waitForCrash(self, waitTime = 4):
		time.sleep(waitTime)
		result = None
		if self.device == None:
			result = subprocess.check_output(self.adbExecutable + " shell logcat -d *:F", shell=True)
		else:
			result = subprocess.check_output(self.adbExecutable + " -s " + self.device + " shell logcat -d *:F", shell=True)
		
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
					#logcat data
					cols = lines[x].split(" ")
					if len(cols)>0:
						report.location = cols[0].replace("/", ".").replace(":", ".")
						
					if "(SIGSEGV" in lines[x]:
						pos1 = lines[x].find("0x")
						pos2 = lines[x].find(" (code=")
						addr = int(lines[x][pos1:pos2], 16)
						if addr > 4095:
							report.nearNull = False
						pos1=pos2+7
						pos2 = pos1 + lines[x][pos1:].find(")")
						if pos2-pos1>0:
							report.type = lines[x][pos1:pos2]
							
					#tombstone
					content = ""
					(fhandler, fname) = tempfile.mkstemp()
					os.close(fhandler)
					if self.device == None:
						subprocess.call([self.adbExecutable, "shell", "su", "-c", "chmod 777 /data/tombstones"])
						subprocess.call([self.adbExecutable, "shell", "su", "-c", "chmod 777 /data/tombstones/tombstone_00"])
						subprocess.call([self.adbExecutable, "pull", "/data/tombstones/tombstone_00", fname])
					else:
						subprocess.call([self.adbExecutable, "-s", self.device, "shell", "su", "-c", "chmod 777 /data/tombstones"])
						subprocess.call([self.adbExecutable, "-s", self.device, "shell", "su", "-c", "chmod 777 /data/tombstones/tombstone_00"])
						subprocess.call([self.adbExecutable, "-s", self.device, "pull", "/data/tombstones/tombstone_00", fname])
					with open(fname, 'r') as content_file:
						content = content_file.read()
					report.info += "\n\n" + content

					#Let's now parse the shit out of the tombstone data
					pos1 = content.find("backtrace")
					pos1 += content[pos1:].find("\n") + 1
					pos2 = pos1 + content[pos1:].find("\n")
					parts = content[pos1:pos2].split()
					if parts[0] == "#00":
						parts2 = parts[3].split("/")
						report.location = parts2[len(parts2)-1] + "_" + parts[2]
			return report		
		return None
				
	def close(self):
		if self.device == None:
			subprocess.call([self.adbExecutable, "shell", "am", "force-stop", self.package[0:self.package.find('/')]])		
		else:
			subprocess.call([self.adbExecutable, "-s", self.device, "shell", "am", "force-stop", self.package[0:self.package.find('/')]])		
