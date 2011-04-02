import os
from threading import Thread
from codec import *

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

         execstring = 'lame -V 2 --add-id3v2 --tc "lame 3.98.4 -V 2" "' + self.source_file + '" "' + self.target_file + '" 2>&1 > /dev/null'
         print 'Encoding "' + self.source_file + '" to "' + self.target_file + '"...'
         outputfd = os.popen(execstring)
         output = outputfd.readlines()
         exitcode = outputfd.close()
