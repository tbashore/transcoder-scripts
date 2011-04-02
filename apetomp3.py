#!/usr/bin/env python

import sys

from transcoder import Transcoder

from codec import *
sys.path.append(sys.path[0] + '/codecs')
from apecodec import APECodec
from mp3codec import MP3Codec

ext_source = '.ape'
ext_intermediate = '.wav'
ext_target = '.mp3'

# Main
trans = Transcoder(APECodec, MP3Codec, ext_source)
trans.Go()
