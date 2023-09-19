import json
import ipdb
import os

class Policy():
    type_obj = "pref"

    def __init__(self, path, name):
        # while os.stat(path).st_size == 0:
        #     pass
        ipdb.set_trace()
        self._info = json.load(open(path))
        self._name = name

    @property
    def info(self):
        return self._info
    
    @property
    def name(self):
        return self._name
    
    def get_info_dict(self):
        return {
            "name" : self.name,
            "info" : self.info,
            "type" : "pol"
        }