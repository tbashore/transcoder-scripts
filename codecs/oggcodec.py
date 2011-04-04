import os
from threading import Thread
from codec import *

class OggCodec(Codec):
   def __init__(self):
      Codec.__init__(self)

   @staticmethod
   def GetExtension():
      return '.ogg'

   class DecoderThread(Thread):
      def __init__(self, source_file):
         Thread.__init__(self)
         self.capabilities = {}
         self.capabilities['input'] = '.ogg'
         self.capabilities['output'] = '.wav'

         self.source_file = source_file
         self.target_file = (os.path.splitext(source_file))[0] + self.capabilities['output']

      def GetCapabilities(self):
         self.capabilities
      
      def run(self):
         if self.source_file.endswith(self.capabilities['input']) == False:
            raise DecodingError('The source file\'s extension is incompatible with this decoder.')

         execstring = 'oggdec -o "' + self.target_file + '" "' + self.source_file + '"  2>&1 > /dev/null'
         print 'Decoding "' + self.source_file + '" to "' + self.target_file + '"...'
         outputfd = os.popen(execstring)
         output = outputfd.readlines()
         exitcode = outputfd.close()

   class EncoderThread(Thread):
      def __init__(self, source_file):
         Thread.__init__(self)
         self.capabilities = {}
         self.capabilities['input'] = '.wav'
         self.capabilities['output'] = '.ogg'

         self.source_file = source_file
         self.target_file = (os.path.splitext(source_file))[0] + self.capabilities['output']

      def GetCapabilities(self):
         self.capabilities
      
      def run(self):
         if self.source_file.endswith(self.capabilities['input']) == False:
            raise EncodingError('The source file\'s extension is incompatible with this encoder.')

         execstring = 'oggenc -q 10 -o "' + self.target_file + '" "' + self.source_file + '" 2>&1 > /dev/null'
         print 'Encoding "' + self.source_file + '" to "' + self.target_file + '"...'
         outputfd = os.popen(execstring)
         output = outputfd.readlines()
         exitcode = outputfd.close()
