import win32api
import win32gui
import win32con
import os
import time
import subprocess
import psutil
import sys
import random
from fuzzConf import fuzzConf
from Vanapagan.Detector.WinBasic import WinBasic
from Vanapagan.Utils.WinUtils import getPidsByImg
from pydoc import locate


def deleteRegs(regsToDelete):
	for regElement in regsToDelete:
		runCommand("REG DELETE %s /f" % regElement)

def deleteFiles(filesToDelete):
	for regElement in filesToDelete:
		if os.name == 'nt':
			runCommand("del /f /q %s" % regElement)
		else:
			raise Exception("deleteFiles not implemented for OS '%s'" % os.name)

def saveSituation(filename, startTime, count):
	f = open("." + os.path.sep + "situation.txt", "w")
	f.write(filename + "\n")
	f.write(str(int(startTime)) + "\n")
	f.write(str(count))
	f.close()

def loadSituation():
	fileVal = None
	timeVal = time.time()
	countVal = 0
	try:
		if os.path.isfile("." + os.path.sep + "situation.txt"):
			f = open("." + os.path.sep + "situation.txt", "r")
			fileVal = f.readline().strip()
			timeVal = int(f.readline().strip())
			countVal = int(f.readline().strip())
			f.close()
	except:
		fileVal = None
		timeVal = time.time()
		countVal = 0
	return (fileVal, timeVal, countVal)

def clearSituation():
	runCommand("del ." + os.path.sep + "situation.txt")

def runCommand(command):
	if os.name == 'nt':
		proc = subprocess.Popen(["cmd", "/c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		for x in xrange(20):
			if proc.poll() != None:
				return True
			time.sleep(0.5)
		return False
	else:
		raise Exception("runCommand not implemented for OS '%s'" % os.name)


def killProc(exename):
	if os.name == 'nt':
		return runCommand("taskkill /f /im %s" % exename)
	else:
		raise Exception("killProc not implemented for OS '%s'" % os.name)

def clearAll(configurations):
	if not killProc(configurations.executable):
		raise Exception("Could not kill process")
	deleteRegs(configurations.regsToDelete)
	deleteFiles(configurations.filesToDelete)

def pidsStoped(processes, imgs):
	try:
		stopped = True
		for proc in processes:
			usage = proc.cpu_percent()
			if usage > 0.0:
				stopped = False

		if stopped:
			for img in imgs:
				pids = getPidsByImg(img)
				for pid in pids:
					exists = False
					for proc in processes:
						if proc.pid == pid:
							exists = True
					if not exists:
						proc = psutil.Process(pid)
						proc.cpu_percent()
						processes.append(proc)
						stopped = False
		return stopped
	except:
		return True

def restart():
	os.system("del ." + os.path.sep + "situation.txt")
	exit()

def enumHandler(hwnd, conf):
	if win32gui.IsWindowVisible(hwnd):
		if conf.windowToInteract in win32gui.GetWindowText(hwnd):
			hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
			win32api.PostMessage(hwndChild, win32con.WM_CHAR, ord(conf.windowToInteractKey), 0)


print "Setting working directory to '%s'" % os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) > 1:
	configurations = fuzzConf(sys.argv[1])
else:
	configurations = fuzzConf("default.json")

desc = None
count = 0
crashes = 0
crashCheck = 0
logs = []
mutators = []

for logConf in configurations.logging:
	logClass = locate('Vanapagan.Loging.' +logConf["type"] + "." + logConf["type"])
	if logClass is None:
		raise Exception("Not implemented logging type '%s'" % logConf["type"])
	log = logClass()
	log.setConf(logConf)
	logs.append(log)

for mutConf in configurations.mutators:
	mutClass = locate('Vanapagan.Mutator.' + mutConf["type"] + "." + mutConf["type"])
	if mutClass is None:
		raise Exception("Not implemented mutation type '%s'" % logConf["type"])
	mut = mutClass()
	mut.setConf(mutConf)
	mutators.append(mut)

run = WinBasic()
start = time.time()
outputFileOwner = None
outputFile = None
startFilename = None

print "Sleeping 4 seconds for possible cancelation"
time.sleep(4)

print "Loading last position(if any)"
(startFilename, start, count) = loadSituation()

print "Deleting useless stuff"
clearAll(configurations)

while True:
	for f in os.listdir(configurations.input):
		if startFilename is not None:
			if f == startFilename:
				startFilename = None
				print "Skipped to %s" % f
			else:
				continue
		else:
			saveSituation(f, start, count)
				
		try:
			if outputFile != None:
				for x in xrange(8):
					try:
						if os.path.isfile(outputFile):
							os.remove(outputFile)
						break
					except:
						time.sleep(0.5)

			inputFile = configurations.input + os.path.sep + f
			unique = "%08X" % random.randint(0, 0xFFFFFFFF)
			outputFile = "." + os.path.sep + unique + os.path.splitext(f)[1]

			desc = mutators[count % len(mutators)].mutate(inputFile, outputFile)
						
			crashLocation = None
			for crashCount in xrange(configurations.retry):
				crash = None
				run.mainProcs = []
				run.run([configurations.executable, outputFile])
				pids = []
				pidsStoped(pids, configurations.binaries)
				if configurations.windowToInteract is not None:
					win32gui.EnumWindows(enumHandler, configurations)
			
				for x in xrange(configurations.maxWait):
					crash = run.waitForCrash(1)
					if crash != None:
						break
					if pidsStoped(pids, configurations.binaries):
						break
					if configurations.windowToInteract is not None:
						win32gui.EnumWindows(enumHandler, configurations)
			
				run.close()
				clearAll(configurations)
				if crash != None and (not crash.nearNull or configurations.logNullCrashes):
					if crashCount != configurations.retry-1:
						print "Issue detected(%d-th time) %s" % (crashCount+1, crash.location)
						if crashLocation is not None:
							if crashLocation != crash.location:
								print "  Not same as before: %s" % crashLocation
								break
						else:
							crashLocation = crash.location
						continue
					crashes += 1
					print "Issue detected & loged at %s" % crash.location
					for log in logs:
						log.log(inputFile, outputFile, crash, desc)
					break
				else:
					break
				
			count += 1
			if count % 10 == 0:
				ratio = (time.time()-start)/count
				print "Done %d reps (%d crashes) - 1 rep per %f seconds (%d per 24h)" % (count, crashes, ratio, 60*60*24/ratio)					
		except:
			if configurations.restartWhenException:
				restart()
			raise
	
	os.system("del ." + os.path.sep + "situation.txt")
	if configurations.restartWhenLoop:
		restart()