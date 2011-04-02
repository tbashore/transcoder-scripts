#!/usr/bin/env python

import sys

from transcoder import Transcoder

from codec import *
sys.path.append(sys.path[0] + '/codecs')
from wavcodec import WAVCodec 
from mp3codec import MP3Codec

# Main
trans = Transcoder(None, MP3Codec)
trans.Go()
