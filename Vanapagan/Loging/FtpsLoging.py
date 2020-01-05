import os
import time
import ftplib
import tempfile

class FtpsLoging:
	dir = None
	host = None
	username = "anonymous"
	password = ""
	workDone = 3

	def setConf(self, conf):
		if "dir" not in conf:
			raise Exception("Parameter 'dir' missing from 'FtpsLoging' logging conf")
		if "host" not in conf:
			raise Exception("Parameter 'host' missing from 'FtpsLoging' logging conf")

		if "username" in conf:
			self.username = conf["username"]
		if "password" in conf:
			self.password = conf["password"]

		self.host = conf["host"]
		self.dir = conf["dir"]
		while self.dir[-1] in ["\\", "/"]:
			self.dir = self.dir[0:-1]
		
	def newDir(self, ftp, dir):
		try:
			ftp.cwd(dir)
		except:
			ftp.mkd(dir)
			ftp.cwd(dir)
			
	def	workDoneFunc(self, buf):
		self.workDone += 1
		
	
	def log(self, fileOrgignal, fileCrash, crashReport = None, fileDesc = None, maxPerIssue=25):
		self.workDone = 0
		ftp = ftplib.FTP_TLS(self.host)
		ftp.FtpsLoging = self
		#ftp.login(self.username, self.password)
		ftp.sendcmd("USER " + self.username)
		ftp.sendcmd("PASS " + self.password)
		
		tmpDir = self.dir
		self.newDir(ftp, tmpDir)
		
		if crashReport != None:
			if crashReport.nearNull:
				tmpDir = "nearNull"
			else:
				tmpDir = "notNearNull"
			self.newDir(ftp, tmpDir)
				
			tmpDir = crashReport.type
			self.newDir(ftp, tmpDir)
				
			tmpDir = crashReport.location.replace(":",".")
			self.newDir(ftp, tmpDir)
				
		count = 0
		try:       
			flist = []
			ftp.retrlines('MLSD', flist.append)
			count = len(flist)/3
		except:
			count = (len(ftp.nlst("")))/3
        
		if count >= maxPerIssue:
			ftp.close()
			return

		ftp.storbinary('STOR ' + ("%04d_crash" % count) + os.path.splitext(fileCrash)[1], open(fileCrash, 'rb'), callback = self.workDoneFunc)
		ftp.storbinary('STOR ' + ("%04d_original" % count) + os.path.splitext(fileOrgignal)[1], open(fileOrgignal, 'rb'), callback = self.workDoneFunc)
		fout = tempfile.TemporaryFile()
		if fileDesc != None:
			fout.write(fileDesc + "\n\n")
		if crashReport != None:
			fout.write(crashReport.getInfo())
		fout.seek(0)
		ftp.storbinary('STOR ' + ("%04d_description.txt" % count), fout, callback = self.workDoneFunc)
		
		while self.workDone < 3:
			time.sleep(1)
		fout.close()
		ftp.close()
		count = 0
		