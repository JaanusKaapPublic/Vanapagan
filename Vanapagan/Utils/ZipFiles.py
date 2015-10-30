import zipfile
import os
		
def zip_myRand(min, max):
	try: 
		val = ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1)) + ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1)) + ord(os.urandom(1)) * ord(os.urandom(1)) * ord(os.urandom(1))
		return min + (val % (max-min+1))
	except:
		return random.randint(min, max)

def zip_unpack(file, dir = "./unpacked"):
	result = []
	if not os.path.isdir(dir):
		os.makedirs(dir)
	ziph = open(file,'rb')
	zip = zipfile.ZipFile(ziph)
	for name in zip.namelist():
		zip.extract(name, dir)
		result.append([name, os.stat(dir + "/" + name).st_size])
	ziph.close()
	zip.close()
	return result
	
def zip_pack(dir, file = "./packed.zip"):
	zip = zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(dir):
		for fn in files:
			absfn = os.path.join(root, fn)
			zfn = absfn[len(dir)+len(os.sep):]
			zip.write(absfn, zfn)
			
def zip_randFile(fileInput):
	files = []
	total = 0
	
	for f in fileInput:
		if f[1] > 0:
			total += f[1]
			files.append(f)
	
	if total==0:
		return None
			
	location = zip_myRand(1, total)	
	for f in files:
		location -= f[1]
		if location < 1:
			return f[0]

	#WTF???
	return files[0][0]