import os
import shutil


class FilesystemLoging:
	dir = "./crashes"
	
	def log(self, file, crashReport = None, fileDesc = None, maxPerIssue=25):
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
				
		count = len(os.listdir(tmpDir))/2
		if count >= maxPerIssue:
			return
		shutil.copy2(file, tmpDir  + ("/%04d_crash" % count) + os.path.splitext(file)[1])
		fout = open(tmpDir + ("/%04d_description.txt" % count), "wb")
		if fileDesc != None:
			fout.write(fileDesc + "\n\n")
		if crashReport != None:
			fout.write(crashReport.getInfo())
		fout.close()
		
		