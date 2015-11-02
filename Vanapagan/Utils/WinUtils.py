from winappdbg import System
import subprocess
import ctypes
import win32evtlog
from ..CrashReport import CrashReport



def killByPid(pid, forced = True):
	if not forced:
		subprocess.call(["taskkill", "/pid", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if forced:
		subprocess.call(["taskkill", "/f", "/pid", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		
def killByImg(img, forced = True):
	if not forced:
		subprocess.call(["taskkill", "/im", str(img)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if forced:
		subprocess.call(["taskkill", "/f", "/im", str(img)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
def isAliveByPid(pid):
	process = ctypes.windll.kernel32.OpenProcess(0x100000, 0, pid)
	if process != 0:
		kernel32.CloseHandle(process)
		return True
	else:
		return False
		
def getPidByImg(img):
	system = System()
	system.scan_processes()
	for ( process, name ) in system.find_processes_by_filename( img ):
		return process.get_pid()
	return 0
		
def getPidsByImg(img):
	result = []
	system = System()
	system.scan_processes()
	for ( process, name ) in system.find_processes_by_filename( img ):
		result.append(process.get_pid())
	return result
	
def clearEvents():
	elog = win32evtlog.OpenEventLog(None, "Application")
	win32evtlog.ClearEventLog(elog, None)
	win32evtlog.CloseEventLog(elog)
	
def isEvent():
	elog = win32evtlog.OpenEventLog(None, "Application")
	nr = win32evtlog.GetNumberOfEventLogRecords(elog)
	if nr>0:
		events = win32evtlog.ReadEventLog(elog, win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ,0)
		if events:
			for event in events:
				if int(event.EventID) == 1000 and int(event.EventCategory) == 100:
					#Of course it's not enough but at least something
					data = event.StringInserts
					crash = CrashReport()
					crash.location = data[0] + "!" +data[3]
					crash.faultAddr = "UNKNOWN"
					crash.code = "UNKNOWN"
					crash.nearNull = True
					crash.type = data[6]
					crash.stack = "UNKNOWN"
					crash.info = "UNKNOWN"
					return crash
	return None