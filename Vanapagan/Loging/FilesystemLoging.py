import os
import shutil


class FilesystemLoging:
	dir = "./crashes"

	def setConf(self, conf):
		if "dir" in conf:
			self.dir = conf["dir"]
			while self.dir[-1] in ["\\", "/"]:
				self.dir = self.dir[0:-1]
	
	def log(self, fileOrgignal, fileCrash, crashReport = None, fileDesc = None, maxPerIssue=25):
		tmpDir = "" + self.dir		
		if not os.path.isdir(tmpDir):
			os.makedirs(tmpDir)	
		
		if crashReport != None:
			if crashReport.nearNull:
				tmpDir += "/nearNull"
			else:
				tmpDir += "/notNearNull"
			if not os.path.isdir(tmpDir):
				os.makedirs(tmpDir)	
				
			tmpDir += "/" + crashReport.type
			if not os.path.isdir(tmpDir):
				os.makedirs(tmpDir)	
				
			tmpDir += "/" + crashReport.location.replace(":",".")
			if not os.path.isdir(tmpDir):
				os.makedirs(tmpDir)
				
		count = len(os.listdir(tmpDir))/3
		if count >= maxPerIssue:
			return
		shutil.copy2(fileOrgignal, tmpDir  + ("/%04d_original" % count) + os.path.splitext(fileOrgignal)[1])
		shutil.copy2(fileCrash, tmpDir  + ("/%04d_crash" % count) + os.path.splitext(fileCrash)[1])
		fout = open(tmpDir + ("/%04d_description.txt" % count), "wb")
		if fileDesc != None:
			fout.write(fileDesc + "\n\n")
		if crashReport != None:
			fout.write(crashReport.getInfo())
		fout.close()
		
		