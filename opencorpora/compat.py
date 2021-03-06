# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import functools
import itertools

PY3 = sys.version_info[0] == 3

if PY3:
    imap = map
else:
    imap = itertools.imap

try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

try:
    import cPickle as pickle
except ImportError:
    import pickle

def utf8_for_PY2(func):
    if PY3:
        return func

    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs).encode('utf8')

    return inner