from ..CrashReport import CrashReport
import time
import select
import subprocess

class LinuxGdb:
	mainProc = None
			
		
	def run(self, executable):
		self.mainProc = subprocess.Popen(["gdb", "--args"] + executable, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				
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
					line = self.mainProc.stdout.read(1)
					result += line
				else:
					break
		return result
				
	def waitForCrash(self, waitTime = 4):
		self.mainProc.stdin.write("run\n")
		time.sleep(waitTime)
		poll_obj = select.poll()
		poll_obj.register(self.mainProc.stdout, select.POLLIN)   
		result = self.readPollStr(poll_obj)
		
		if " SIGSEGV" in result:
			report = CrashReport()
			report.location = "UNKNOWN"
			report.faultAddr = "UNKNOWN"
			report.code = "UNKNOWN"
			report.nearNull = True
			report.type = "UNKNOWN"
			report.stack = "UNKNOWN"
			report.info = ""
		
			pos1 = result.find(" SIG")+1
			pos2 = result.find(",", pos1)
			pos3 = result.find(" ", pos1)
			if pos3<pos2 and pos3!=-1:
				pos2=pos3
			report.type=result[pos1:pos2]
			
			

			self.mainProc.stdin.write("p $_siginfo._sifields._sigfault.si_addr\n")
			time.sleep(3)
			crashLocation = self.readPollStr(poll_obj)
			pos1 = crashLocation.find("0x")+2
			pos2 = crashLocation.find("(gdb)")-1
			if pos2==-1:
				pos2=len(crashLocation[pos1:])
			if pos2-pos1<4:
				report.nearNull = True
			else:
				report.nearNull = False
			result += "\n\n\n---CRASH ADDRESS---\n"
			result += crashLocation
				

			self.mainProc.stdin.write("x/i $pc\n")
			time.sleep(3)
			result += "\n\n\n---DISASM---\n"
			result += self.readPollStr(poll_obj)

			self.mainProc.stdin.write("info registers\n")
			time.sleep(3)
			result += "\n\n\n---REGISTERS---\n"
			result += self.readPollStr(poll_obj)

			self.mainProc.stdin.write("bt\n")
			time.sleep(3)
			result += "\n\n\n---BACKTRACES---\n"
			result += self.readPollStr(poll_obj)
	
			report.info = result				

			if " in " in result:
				pos1 = result.find(" in ")+4
				pos2 = result.find("(", pos1)
				pos3 = result.find("\n", pos1)
				if pos2 == -1 or pos2>pos3:
					pos2 = pos3
				report.location = result[pos1:pos2]	
			return report
		
		return None
		