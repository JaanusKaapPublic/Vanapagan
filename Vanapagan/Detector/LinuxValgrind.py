from ..CrashReport import CrashReport
import time
import select
import sys
import subprocess

class LinuxValgrind:
	valgrindExec = "valgrind"
	mainProc = None
			
		
	def run(self, executable):
		self.mainProc = subprocess.Popen([self.valgrindExec, "--tool=memcheck"] + executable, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				
	def close(self, forced = False):
		if forced:
			subprocess.call(["kill", "-9", str(self.mainProc.pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)		
		else:
			subprocess.call(["kill", str(self.mainProc.pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)		

	def readPollStr(self, poll_obj):
		result = ""
		while True:
				poll_result = poll_obj.poll(1)
				if poll_result:
					line = self.mainProc.stderr.read(1)
					if line == "":
						break
					result += line
				else:
					break
		return result
				
	def waitForCrash(self, waitTime = 4):
		time.sleep(waitTime)
		poll_obj = select.poll()
		poll_obj.register(self.mainProc.stderr, select.POLLIN)   
		result = self.readPollStr(poll_obj)
		
		pos1 = result.find("Invalid read")
		pos2 = result.find("Invalid write")
		pos3 = result.find("Invalid free")
		
		if pos1 != -1 or pos2 != -1 or pos3 != -1:
			report = CrashReport()
			report.location = "UNKNOWN"
			report.faultAddr = "UNKNOWN"
			report.code = "UNKNOWN"
			report.nearNull = True
			report.type = "UNKNOWN"
			report.stack = "UNKNOWN"
			report.info = ""
		
			if pos1 == -1:
				pos1 = 0xFFFFFFFF
			if pos2 == -1:
				pos2 = 0xFFFFFFFF
			if pos3 == -1:
				pos3 = 0xFFFFFFFF
			pos0 = None
				
			#Type
			if pos1<=pos2 and pos1<=pos2:
				report.type = "Read"
				pos0 = pos1
			elif pos2<=pos1 and pos2<=pos3:
				report.type = "Write"
				pos0 = pos2
			if pos3<=pos1 and pos3<=pos2:
				report.type = "DblFree"
				pos0 = pos3
				
			
			loc1 = pos0 + result[pos0:].find("at 0x")+3
			loc2 = loc1 + result[loc1:].find(": ")
			report.location = result[loc1:loc2][-3:] #-3 because of the ASLR for now
			
			loc2 = loc1 + result[loc1:].find("\n")
			loc1 = loc1 + result[loc1:].find(": ")+2
			parts = result[loc1:loc2].split("/")
			if len(parts)>2:
				if " (in " in parts[0]:
					report.location = parts[len(parts)-1][:-1] + "_" + parts[0][:-5] + "_" + report.location
				else:
					report.location = parts[len(parts)-1][:-1] + "_" + report.location
			
			loc1 = pos0 + result[pos0:].find("Address 0x")+8
			loc2 = loc1 + result[loc1:].find(" ")
			addr = int(result[loc1:loc2], 16)
			report.faultAddr = result[loc1:loc2]
			if addr>0x1000:
				report.nearNull = False		

			report.info = result[pos0:]
			return report		
		return None
		