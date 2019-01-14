#!/usr/bin/env python
'''
Requires https://pypi.org/project/qrcode/
'''

import re
import qrcode
import io

from lib.core.data import kb
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Encode the payload in QR-Code
    """

    if payload:
        output = io.BytesIO()
        qrc = qrcode.make(payload)
        qrc.save(output)
        
    return output.getvalue()