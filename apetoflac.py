#!/usr/bin/env python

import sys

sys.path.append(sys.path[0] + '/base')
from transcoder import Transcoder
from codec import *

sys.path.append(sys.path[0] + '/codecs')
from apecodec import APECodec
from flaccodec import FLACCodec

# Main
trans = Transcoder(APECodec, FLACCodec)
trans.Go()
