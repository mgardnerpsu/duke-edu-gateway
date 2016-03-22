'''
Patch for UUID serialization support in json
'''
from json import JSONEncoder
from uuid import UUID

JSONEncoder_old_default = JSONEncoder.default

def JSONEncoder_new_default(self, o):
    if isinstance(o, UUID): 
    	return str(o)
    return JSONEncoder_old_default(self, o)

JSONEncoder.default = JSONEncoder_new_default
