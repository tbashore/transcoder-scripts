#!/usr/bin/env python

import sys

from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import TPOS

sys.path.append(sys.path[0] + '/base')
from transcoder import Transcoder
from codec import *

sys.path.append(sys.path[0] + '/codecs')
from flaccodec import FLACCodec
from mp3codec import MP3Codec

def CopyTags(source_file, target_file):
   f = FLAC(source_file)
   m = EasyID3(target_file)

   for key in ['artist', 'title', 'album', 'date', 'genre', 'tracknumber']:
      if f.has_key(key):
         m[key] = f[key]
   m.save()

   if f.has_key('discnumber'):
      m = MP3(target_file)
      m['TPOS'] = TPOS(encoding=3, text=f['discnumber'])
      m.save()

# Main
trans = Transcoder(FLACCodec, MP3Codec, CopyTags)
trans.Go()
