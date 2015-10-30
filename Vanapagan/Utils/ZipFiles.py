import zipfile
import os

def unpack(file, dir = "./unpacked"):
	result = []
	if not os.path.isdir(dir):
		os.makedirs(dir)
	ziph = open(file,'rb')
	zip = zipfile.ZipFile(ziph)
	for name in zip.namelist():
		zip.extract(name, dir)
		result.append(name)
	ziph.close()
	zip.close()
	return result
	
def pack(dir, file = "./packed.zip"):
	zip = zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(dir):
		for fn in files:
			absfn = os.path.join(root, fn)
			zfn = absfn[len(dir)+len(os.sep):]
			zip.write(absfn, zfn)