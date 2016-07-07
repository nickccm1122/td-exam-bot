"""
General purpose utility library..
"""

import json


def loadConfig(file):
    """Input: file; Output: json object"""
    file = file.read()
    Obj = json.loads(file)
    return Obj
