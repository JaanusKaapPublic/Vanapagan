import os
import shutil


class MutatorBase:		
	def myRand(self, min, max):
		val = ord(os.urandom(1)) * 0x100000 + ord(os.urandom(1)) * 0x10000 + ord(os.urandom(1)) * 0x100 + ord(os.urandom(1))
		return min + (val % (max-min+1))
		
	def isInXmlValue(self, f, pos, len):
		quotes = False
		f.seek(pos)
		for x in xrange(len):
			c = f.read(1)
			if c == "<" or c == ">" or c == "\"":
				return False
		
		c = f.read(1)
		quotes = 0
		while c != "" and c != None:
			if c=="\"":
				quotes += 1
			if c==">":
				if quotes % 2 == 0:
					return False
				else:
					return True				
			if c=="<":
				return True
			c = f.read(1)
		return False
		
	def restore(self, src, dest, signature):
		signatures = signature.split('|')
		if src!=dest:
			shutil.copy2(src, dest)
		
		f=open(dest, "r+b")
		for sign in signatures:
			pos = int(sign[0:8], 16)
			val = int(sign[8:10], 16)
			f.seek(pos)
			f.write(chr(val))
		f.close()

	def setConf(self, conf):
		return True