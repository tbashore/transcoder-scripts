import os
from threading import Thread
from time import sleep

class TranscoderThread(Thread):
   def __init__(self, source_codec, target_codec, source_file):
      Thread.__init__(self)
      self.source_codec = source_codec
      self.target_codec = target_codec
      self.post_process = None
      self.source_file = source_file

   def run(self):
      if not self.source_file:
         return

      if self.source_codec:
         decoder = self.source_codec.DecoderThread(self.source_file)
         decoder.start()

         while decoder.isAlive():
            sleep(1)


      if self.target_codec:
         encode_source_file = decoder.target_file if self.source_codec else self.source_file

         encoder = self.target_codec.EncoderThread(encode_source_file)
         encoder.start()

         while encoder.isAlive():
            sleep(1)

      if self.source_codec:
         os.unlink(decoder.target_file)

      if self.post_process:
         self.post_process(self.source_file, encoder.target_file)
