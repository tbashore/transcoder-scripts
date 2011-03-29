#!/usr/bin/env python

import os, re, sys
from threading import Thread
from time import sleep

from codec import *
sys.path.append(sys.path[0] + '/codecs')
from apecodec import APECodec
from flaccodec import FLACCodec

ext_source = '.ape'
ext_intermediate = '.wav'
ext_target = '.flac'

#available_codecs = []

class TranscoderThread(Thread):
	def __init__(self, source_file):
		Thread.__init__(self)
		self.source_file = source_file
		self.intermediate_file = (os.path.splitext(source_file))[0] + ext_intermediate
		#self.target_file = (os.path.splitext(source_file))[0] + ext_target
	def run(self):
		ape = APECodec
		apedecoder = ape.DecoderThread(self.source_file)
		apedecoder.start()
		
		while apedecoder.isAlive():
			sleep(1)

		flac = FLACCodec
		flacencoder = flac.EncoderThread(self.intermediate_file)
		flacencoder.start()
		
		while flacencoder.isAlive():
			sleep(1)

		os.unlink(self.intermediate_file)

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
numcpus = len(os.listdir('/sys/devices/system/cpu'))

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
