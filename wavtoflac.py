#!/usr/bin/env python

import sys

from transcoder import Transcoder

from codec import *
sys.path.append(sys.path[0] + '/codecs')
from flaccodec import FLACCodec

ext_source = '.wav'
ext_intermediate = '.wav'
ext_target = '.flac'

# Main
trans = Transcoder(None, FLACCodec, ext_source)
trans.Go()
