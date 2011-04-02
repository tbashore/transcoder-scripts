# Parent codec class.
class Codec:
	def __init__(self):
		pass
   
	@staticmethod
	def GetExtension(self):
		pass

class DecodingError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return str(self.value)

class EncodingError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return str(self.value)
