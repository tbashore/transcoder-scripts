import os, re
from time import sleep
from transcoderthread import TranscoderThread

class Transcoder():
   def __init__(self, source_codec, target_codec, post_process=None):
      self.source_codec = source_codec
      self.target_codec = target_codec
      self.ext_source = source_codec.GetExtension() if source_codec else '.wav'
      self.post_process = post_process

   def CheckThreads(self, threadlist):
      numThreads = len(threadlist)
      numLiveThreads = 0
      deadThreadIndices = []
      for i in range(0, numThreads):
         if threadlist[i].isAlive():
            numLiveThreads += 1
         else:
            deadThreadIndices.append(i)

      return numLiveThreads, deadThreadIndices

   def Go(self):
      numcpus = len(filter(lambda x: re.match('^cpu\d+$', x), os.listdir('/sys/devices/system/cpu')))

      source_files = filter(lambda x: x.endswith(self.ext_source), os.listdir('.'))
      source_files.sort()

      threadlist = []
      while len(source_files) != 0:
         numLiveThreads, deadThreadIndices = self.CheckThreads(threadlist)

         # Delete the dead threads in reverse order so that the other deadThreadIndices are not invalidated by deleting one.
         deadThreadIndices.reverse()
         for i in deadThreadIndices:
            threadlist.pop(i)

         if numLiveThreads < numcpus:
            # Add more work
            transThread = TranscoderThread(self.source_codec, self.target_codec, source_files.pop(0))
            transThread.post_process = self.post_process
            transThread.start()
            threadlist.append(transThread)

         sleep(1)

      numLiveThreads, deadThreadIndices = self.CheckThreads(threadlist)
      while numLiveThreads > 0:
         sleep(1)
         numLiveThreads, deadThreadIndices = self.CheckThreads(threadlist)

      print 'Done.'
