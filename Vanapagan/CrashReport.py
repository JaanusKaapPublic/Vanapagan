class CrashReport:
	location = None
	faultAddr = None
	code = None
	nearNull = None
	type = None
	stack = None
	info = None
	
	def getInfo(self):
		response = ""
		response += "Location: " + self.location + "\n"
		response += "Fault address: " + self.faultAddr + "\n"
		response += "Code: " + self.code + "\n"
		response += "Is near null: " + str(self.nearNull) + "\n"
		response += "Type: " + self.type + "\n\n\n"
		response += "Stack\n----------\n" + self.stack + "\n----------\n\n\nINFO\n----------\n"
		response += self.info
		return response
		