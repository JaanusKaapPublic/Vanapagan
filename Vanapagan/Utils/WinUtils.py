from winappdbg import System
import subprocess
import ctypes
import win32evtlog



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
	win32evtlog.CloseEventLog(elog)
	return (nr>0)