#!/usr/bin/env python

import sys

from transcoder import Transcoder

from codec import *
sys.path.append(sys.path[0] + '/codecs')
from flaccodec import FLACCodec

# Main
trans = Transcoder(None, FLACCodec)
trans.Go()
