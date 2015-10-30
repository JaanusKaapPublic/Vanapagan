import shutil
import os
import random


class XmlBitFlipping:
	rate = 20000
	min = 2
	max = 100
	skip = 0

	def mutate(self, src, dest):
		ret_signature = []
		ret_text = ""
		try:
			ret_text += "Mutating file %s into file %s using FileBitFlipping mutator\n\n" % (src, dest)
			shutil.copy2(src, dest)
			size = os.path.getsize( dest )		
			count = int(round(size / self.rate))
			if int(count) < self.min:
				count = self.min
			if self.max > 0 and int(count) > self.max:
				count = self.max
		
			f=open(dest, "r+b")
			for x in xrange(int(count)):
				while True:
					pos = self.myRand(self.skip, size-1)
					
					if not self.isInXmlValue(f, pos, 1):
						continue

					f.seek(pos)
					c = f.read(1)
					if c != None:
						val=ord(c)
						oldVal = val
						f.seek(pos)
						val=self.modify(val)
						f.write(chr(val))
						ret_signature.append("%08X%02X%02X" % (pos, oldVal, val))
						ret_text += "Mutating byte at 0x%X (%d) from 0x%02X to 0x%02X\n" % (pos, pos, oldVal, val)
					break
			f.close()
		except:
			raise  #Just for now
			return None
		return "|".join(ret_signature) + "\n" + ret_text
		
	def restore(self, src, dest, signature):
		signatures = signature.split('|')
		shutil.copy2(src, dest)
		
		f=open(dest, "r+b")
		for sign in signatures:
			pos = int(sign[0:8], 16)
			val = int(sign[8:10], 16)
			f.seek(pos)
			f.write(chr(val))
		f.close()
		
		
		
	def modify(self, byte):
		return byte  ^ [1,2,4,8,16,32,64][self.myRand(0, 6)] 
		
		
	def myRand(self, min, max):
		try: 
			val = ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1)) + ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1)) + ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1))
			return min + (val % (max-min+1))
		except:
			return random.randint(min, max)
		
	def isInXmlValue(self, f, pos, len):
		quotes = False
		f.seek(pos)
		for x in xrange(len):
			c = f.read(1)
			if c == ">":
				return False
			if c == "<":
				return False
		for x in xrange(pos):
			f.seek(pos-x)
			c = f.read(1)
			if quotes:
				if c == "=":
					return True
				else:
					quotes = False
			if c == ">":
				return True
			if c == "<":
				return False
			if c == "\"":
				quotes = True
		return False