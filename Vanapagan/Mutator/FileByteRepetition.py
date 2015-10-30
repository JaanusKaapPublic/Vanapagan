import shutil
import os
import random


class FileByteRepetition:
	rate = 80000
	min = 1
	max = 6
	minlen = 2
	maxlen = 1024
	skip = 0

	def mutate(self, src, dest):
		ret_signature = []
		ret_text = ""
		try:
			ret_text += "Mutating file %s into file %s using FileByteRepetition mutator\n\n" % (src, dest)
			positions = []
			size = os.path.getsize( src )		
			count = int(round(size / self.rate))
			if int(count) < self.min:
				count = self.min
			if self.max > 0 and int(count) > self.max:
				count = self.max
			for x in xrange(count):
				positions.append(self.myRand(self.skip, size-1))
		
			fin = open(src, "rb")
			fout = open(dest, "wb")
				
			byte = fin.read(1)
			pos = 0
			while byte != "":
				fout.write(byte)
				if pos in positions:
					reps = self.myRand(self.minlen, self.maxlen)
					fout.write(byte * reps)
					ret_signature.append("%08X%04X%02X" % (pos, reps, ord(byte)))
					ret_text += "Adding %02X byte %04X times to position %08X(%d)\n" % (ord(byte), reps, pos, pos)
				byte = fin.read(1)			
				pos += 1
				
			fin.close()
			fout.close()
		except:
			raise #Just for now
			return None
		return "|".join(ret_signature) + "\n" + ret_text
						
		
	def myRand(self, min, max):
		try: 
			val = ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1)) + ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1)) + ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1))
			return min + (val % (max-min+1))
		except:
			return random.randint(min, max)