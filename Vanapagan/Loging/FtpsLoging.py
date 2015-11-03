import os
import time
import ftplib


class FtpsLoging:
	dir = "crashes/crashesTest"
	host = None
	username = None
	password = None
	workDone = 2
	
	def __init__(self, host, username, password):
		self.host = host
		self.username = username
		self.password = password
		
		
		
	def newDir(self, ftp, dir):
		try:
			ftp.cwd(dir)
		except:
			ftp.mkd(dir)
			ftp.cwd(dir)
			
	def	workDoneFunc(self, buf):
		self.workDone += 1
		
	
	def log(self, file, crashReport = None, fileDesc = None):
		self.workDone = 0
		ftp = ftplib.FTP_TLS(self.host)
		ftp.FtpsLoging = self
		ftp.login(self.username, self.password)
		
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
				
		count = (len(ftp.nlst(""))-2)/2
		ftp.storbinary('STOR ' + ("%04d_crash" % count) + os.path.splitext(file)[1], open(file, 'rb'), callback = self.workDoneFunc)
		fout = open("./TmpDescription.txt", "wb")
		if fileDesc != None:
			fout.write(fileDesc + "\n\n")
		if crashReport != None:
			fout.write(crashReport.getInfo())
		fout.close()
		ftp.storbinary('STOR ' + ("%04d_description.txt" % count), open("./TmpDescription.txt", 'rb'), callback = self.workDoneFunc)
		
		while self.workDone < 2:
			time.sleep(1)
		ftp.close()
		count = 0
		while True:
			try:
				os.remove("./TmpDescription.txt")
				break
			except:
				count += 1
				if count > 3:
					raise
				time.sleep(1)
		