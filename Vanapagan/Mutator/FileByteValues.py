import shutil
import os
import MutatorBase


class FileByteValues(MutatorBase.MutatorBase):
	byteValues = [[0x00], [0xFF], [0xFE], [0xFF,0xFF], [0xFF,0xFE], [0xFE,0xFF], [0xFF,0xFF,0xFF,0xFF], [0xFF,0xFF,0xFF,0xFE], [0xFE,0xFF,0xFF,0xFF], [0x7F], [0x7E], [0x7F,0xFF], [0x7F,0xFE], [0xFF,0x7F], [0xFE,0x7F], [0x7F,0xFF,0xFF,0xFF], [0x7F,0xFF,0xFF,0xFE], [0xFF,0xFF,0xFF,0x7F], [0xFE,0xFF,0xFF,0x7F]]
	rate = 20000
	min = 2
	max = 100
	skip = 0

	def mutate(self, src, dest):
		ret_signature = []
		ret_text = ""
		try:
			if src!=dest:
				shutil.copy2(src, dest)
			size = os.path.getsize( dest )		
			count = int(round(size / self.rate))
			if int(count) < self.min:
				count = self.min
			if self.max > 0 and int(count) > self.max:
				count = self.max
		
			f=open(dest, "r+b")
			for x in xrange(int(count)):
				newVal = self.byteValues[self.myRand(0, len(self.byteValues)-1)]
				pos = self.myRand(self.skip, size-len(newVal))
				for y in xrange(len(newVal)):
					f.seek(pos+y)
					oldVal = f.read(1)
					f.seek(pos+y)
					f.write(chr(newVal[y]))					
					ret_signature.append("%08X%02X%02X" % (pos+y, ord(oldVal), newVal[y]))
					ret_text += "Mutating byte at 0x%X (%d) from 0x%02X to 0x%02X\n" % (pos, pos, ord(oldVal), newVal[y])
			f.close()
		except:
			raise #Just for now
			return None
		return "|".join(ret_signature) + "\n" + ret_text