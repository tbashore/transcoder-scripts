#!/usr/bin/env python

import sys

from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis
from mutagen.mp3 import MP3
from mutagen.id3 import TPOS

sys.path.append(sys.path[0] + '/base')
from transcoder import Transcoder
from codec import *

sys.path.append(sys.path[0] + '/codecs')
from oggcodec import OggCodec
from mp3codec import MP3Codec

def CopyTags(source_file, target_file):
   o = OggVorbis(source_file)
   m = EasyID3(target_file)

   for key in ['artist', 'title', 'album', 'date', 'genre', 'tracknumber']:
      if o.has_key(key):
         m[key] = o[key]
   m.save()

   if o.has_key('discnumber'):
      m = MP3(target_file)
      m['TPOS'] = TPOS(encoding=3, text=o['discnumber'])
      m.save()

# Main
trans = Transcoder(OggCodec, MP3Codec, CopyTags)
trans.Go()
