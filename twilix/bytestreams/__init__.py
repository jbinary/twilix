from __future__ import unicode_literals
from builtins import str
import time
import hashlib
import random

def genSID():
    sid = str(time.time())
    sid += str(random.random())
    return hashlib.sha1(sid).hexdigest()
