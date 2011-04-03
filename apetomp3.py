#!/usr/bin/env python

import sys

sys.path.append(sys.path[0] + '/base')
from transcoder import Transcoder
from codec import *

sys.path.append(sys.path[0] + '/codecs')
from apecodec import APECodec
from mp3codec import MP3Codec

# Main
trans = Transcoder(APECodec, MP3Codec)
trans.Go()
