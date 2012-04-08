# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import functools

PY3 = sys.version_info[0] == 3

try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


def utf8_for_PY2(func):
    if PY3:
        return func

    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs).encode('utf8')

    return inner