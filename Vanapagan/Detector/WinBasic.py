from winappdbg import Debug, Crash, win32, HexDump
from time import time
from winappdbg.util import MemoryAddresses
from ..CrashReport import CrashReport
import subprocess

class WinBasic:
	debugger = None
	mainProc = None
	alwaysCatchExceptions=[win32.STATUS_ACCESS_VIOLATION, win32.STATUS_ILLEGAL_INSTRUCTION, win32.STATUS_ARRAY_BOUNDS_EXCEEDED]
	
	def __init__(self, killOnExit = True):
		self.debugger = Debug(bKillOnExit = killOnExit)
		self.mainProcs = []
		
		
	def run(self, executable, children = True):
		tmp = self.debugger.execv(executable, bFollow = children )
		self.mainProcs.append(tmp)
		return tmp.get_pid()
		
		
	def attachPid(self, pid):	
		self.mainProcs.append(self.debugger.attach(pid))
		

	def attachImg(self, img):	
		self.debugger.system.scan_processes()
		for ( process, name ) in self.debugger.system.find_processes_by_filename( img ):
			self.attachPid(process.get_pid())		
				
	def close(self, kill = True, taskkill = True, forced = True):	
		pids = self.debugger.get_debugee_pids()
		
		self.debugger.detach_from_all( True )	
		for pid in pids:				
			if kill:
				try:
					proc = self.debugger.system.get_process(pid)
					proc.kill()
				except:
					pass
			
			#Taskkill
			if taskkill and not forced:
				subprocess.call(["taskkill", "/pid", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if taskkill and forced:
				subprocess.call(["taskkill", "/f", "/pid", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				
				
	def waitForCrash(self, waitTime = 4, checkAlive = False):
		event = None
		endDebuging = False
		endTime = time() + waitTime
		
		while time() < endTime:
			if checkAlive:
				for proc in self.mainProcs:
					if not proc.is_alive():
						return None
		
			try:
				event = self.debugger.wait(1000)
			except WindowsError, e:
				if e.winerror in (win32.ERROR_SEM_TIMEOUT, win32.WAIT_TIMEOUT):
					continue
				raise
			
			crash = self.handler(event)
			if crash != None:			
				return crash
			else:
				try:
					self.debugger.dispatch()
				except:
					pass
				finally:
					self.debugger.cont()
		return None
		
		
	def handler(self, event):
		if event.get_event_code() == win32.EXCEPTION_DEBUG_EVENT and event.get_exception_code() != win32.STATUS_BREAKPOINT and (event.is_last_chance() or event.get_exception_code() in self.alwaysCatchExceptions):
			crash = Crash(event)
			report = CrashReport()
			
			crash = Crash(event)
			(exploitable, type, info) = crash.isExploitable()			
			try:
				report.code = event.get_thread().disassemble( crash.pc, 0x10 ) [0][2]
			except:
				report.code = "Could not disassemble"
			
				
						
			if crash.faultAddress is None or MemoryAddresses.align_address_to_page_start(crash.faultAddress) == 0:
				report.nearNull = True
			else:
				report.nearNull = False			
			report.type = type
			
			lib = event.get_thread().get_process().get_module_at_address(crash.pc)
			if lib != None:
				report.location = lib.get_label_at_address(crash.pc)
			else:
				report.location = HexDump.address(crash.pc, event.get_thread().get_process().get_bits())[-4:]
				
			if crash.faultAddress == None:
				crash.faultAddress = 0
			report.faultAddr = HexDump.address(crash.faultAddress, event.get_thread().get_process().get_bits())
			
			report.stack = ""
			stList = self.getStackTraceRelList(event.get_thread())
			if len(stList)>0:
				for ra in stList:
					lib = event.get_thread().get_process().get_module_at_address(ra)
					if lib != None:
						report.stack += lib.get_label_at_address(ra) + " " + HexDump.address(ra, event.get_thread().get_process().get_bits()) + "\n"
					else:
						report.stack += HexDump.address(ra, event.get_thread().get_process().get_bits()) + "\n"
			if report.stack == "":
				report.stack = "NO_STACK"			
			report.info= crash.fullReport()
			
			return report
		return None
		
	def getStackTraceRelList(self, thread):
		ret = []
		
		try:
			sp = thread.get_sp()		
			ebp = thread.get_context(win32.CONTEXT_CONTROL)['Ebp']
			for x in xrange(0,10):
				addr = thread.get_process().peek_pointer(ebp + 4)
				if addr == None:
					break
				ebp = thread.get_process().peek_pointer(ebp)
				lib = thread.get_process().get_module_at_address(addr)
				if thread.get_process().is_address_executable(addr) and lib != None:
					ret.append(addr)
				else:
					break
		except:
			pass
		return ret