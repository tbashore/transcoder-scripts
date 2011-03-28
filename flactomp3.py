#!/usr/bin/env python

import os, re
from threading import Thread
from time import sleep

from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import TPOS

ext_source = '.flac'
ext_intermediate = '.wav'
ext_target = '.mp3'

#available_codecs = []

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

# Parent codec class.
class Codec:
	def __init__(self):
		#available_codecs.append(self)
		pass
	
	def GetCapabilities(self):
		pass

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

class MP3Codec(Codec):
	def __init__(self):
		Codec.__init__(self)

	class DecoderThread(Thread):
		def __init__(self, source_file):
			Thread.__init__(self)
			self.capabilities = {}
			self.capabilities['input'] = '.mp3'
			self.capabilities['output'] = '.wav'

			self.source_file = source_file
			self.target_file = (os.path.splitext(source_file))[0] + self.capabilities['output']

		def GetCapabilities(self):
			self.capabilities
		
		def run(self):
			if self.source_file.endswith(self.capabilities['input']) == False:
				raise DecodingError('The source file\'s extension is incompatible with this decoder.')

			execstring = 'lame --decode "' + self.source_file + '" "' + self.target_file + '" 2>&1 > /dev/null'
			print 'Decoding "' + self.source_file + '" to "' + self.target_file + '"...'
			outputfd = os.popen(execstring)
			output = outputfd.readlines()
			exitcode = outputfd.close()

	class EncoderThread(Thread):
		def __init__(self, source_file):
			Thread.__init__(self)
			self.capabilities = {}
			self.capabilities['input'] = '.wav'
			self.capabilities['output'] = '.mp3'

			self.source_file = source_file
			self.target_file = (os.path.splitext(source_file))[0] + self.capabilities['output']

		def GetCapabilities(self):
			self.capabilities

		def run(self):
			if self.source_file.endswith(self.capabilities['input']) == False:
				raise DecodingError('The source file\'s extension is incompatible with this decoder.')

			execstring = 'lame -V 2 --vbr-new --add-id3v2 --tc "lame 3.93 --alt-preset standard" "' + self.source_file + '" "' + self.target_file + '" 2>&1 > /dev/null'
			print 'Encoding "' + self.source_file + '" to "' + self.target_file + '"...'
			outputfd = os.popen(execstring)
			output = outputfd.readlines()
			exitcode = outputfd.close()

class TranscoderThread(Thread):
	def __init__(self, source_file):
		Thread.__init__(self)
		self.source_file = source_file
		self.intermediate_file = (os.path.splitext(source_file))[0] + ext_intermediate
		#self.target_file = (os.path.splitext(source_file))[0] + ext_target
	def run(self):
		flac = FLACCodec
		flacdecoder = flac.DecoderThread(self.source_file)
		flacdecoder.start()
		
		while flacdecoder.isAlive():
			sleep(1)

		mp3 = MP3Codec
		mp3encoder = mp3.EncoderThread(self.intermediate_file)
		mp3encoder.start()

		while mp3encoder.isAlive():
			sleep(1)

		os.unlink(self.intermediate_file)

		# Copy tags
		f = FLAC(self.source_file)
		m = EasyID3(mp3encoder.target_file)

		for key in ['artist', 'title', 'album', 'date', 'genre', 'tracknumber']:
			if f.has_key(key):
				m[key] = f[key]
		m.save()

		if f.has_key('discnumber'):
			m = MP3(mp3encoder.target_file)
			m['TPOS'] = TPOS(encoding=3, text=f['discnumber'])
			m.save()

def CheckThreads(threadlist):
   numThreads = len(threadlist)
   numLiveThreads = 0
   deadThreadIndices = []
   for i in range(0, numThreads):
      if threadlist[i].isAlive():
         numLiveThreads += 1
      else:
         deadThreadIndices.append(i)

   return numLiveThreads, deadThreadIndices

# Main
numcpus = len(filter(lambda x: re.match('^cpu\d+$', x), os.listdir('/sys/devices/system/cpu')))

files = os.listdir('.')

source_files = []
for file in files:
   if file.endswith(ext_source):
      source_files.append(file)

source_files.sort()

threadlist = []
while len(source_files) != 0:
   numLiveThreads, deadThreadIndices = CheckThreads(threadlist)

   # Delete the dead threads in reverse order so that the other deadThreadIndices are not invalidated by deleting one.
   deadThreadIndices.reverse()
   for i in deadThreadIndices:
      threadlist.pop(i)

   if numLiveThreads < numcpus:
      # Add more work
      encThread = TranscoderThread(source_files.pop(0))
      encThread.start()
      threadlist.append(encThread)

   sleep(1)

numLiveThreads, deadThreadIndices = CheckThreads(threadlist)
while numLiveThreads > 0:
   sleep(1)
   numLiveThreads, deadThreadIndices = CheckThreads(threadlist)

print 'Done.'
