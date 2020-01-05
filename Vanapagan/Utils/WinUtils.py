from winappdbg import System

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
