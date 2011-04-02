#!/usr/bin/env python

import sys

from transcoder import Transcoder

from codec import *
sys.path.append(sys.path[0] + '/codecs')
from apecodec import APECodec
from flaccodec import FLACCodec

ext_source = '.ape'
ext_intermediate = '.wav'
ext_target = '.flac'

# Main
trans = Transcoder(APECodec, FLACCodec, ext_source)
trans.Go()
