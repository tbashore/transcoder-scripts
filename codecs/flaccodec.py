import os
from threading import Thread
from codec import *

class FLACCodec(Codec):
	def __init__(self):
		Codec.__init__(self)

	class DecoderThread(Thread):
		def __init__(self, source_file):
			Thread.__init__(self)
			self.capabilities = {}
			self.capabilities['input'] = '.flac'
			self.capabilities['output'] = '.wav'

			self.source_file = source_file
			self.target_file = (os.path.splitext(source_file))[0] + self.capabilities['output']

		def GetCapabilities(self):
			self.capabilities
		
		def run(self):
			if self.source_file.endswith(self.capabilities['input']) == False:
				raise DecodingError('The source file\'s extension is incompatible with this decoder.')

			execstring = 'flac -d "' + self.source_file + '" -o "' + self.target_file + '" 2>&1 > /dev/null'
			print 'Decoding "' + self.source_file + '" to "' + self.target_file + '"...'
			outputfd = os.popen(execstring)
			output = outputfd.readlines()
			exitcode = outputfd.close()

	class EncoderThread(Thread):
		def __init__(self, source_file):
			Thread.__init__(self)
			self.capabilities = {}
			self.capabilities['input'] = '.wav'
			self.capabilities['output'] = '.flac'

			self.source_file = source_file
			self.target_file = (os.path.splitext(source_file))[0] + self.capabilities['output']

		def GetCapabilities(self):
			self.capabilities
		
		def run(self):
			if self.source_file.endswith(self.capabilities['input']) == False:
				raise EncodingError('The source file\'s extension is incompatible with this encoder.')

			execstring = 'flac "' + self.source_file + '" -o "' + self.target_file + '" 2>&1 > /dev/null'
			print 'Encoding "' + self.source_file + '" to "' + self.target_file + '"...'
			outputfd = os.popen(execstring)
			output = outputfd.readlines()
			exitcode = outputfd.close()
