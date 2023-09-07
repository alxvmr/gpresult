class GPO():
    type_obj = "gpo"

    def __init__(self, name, uuid, path=None):
        self._name = name
        self._uuid = uuid
        self._path = path

    @property
    def name(self):
        return self._name
    
    @property
    def uuid(self):
        return self._uuid
    
    @property
    def path(self):
        return self._path
    
    def get_info_dict(self):
        return {
            "name_gpo":self.name,
            "uuid":self.uuid,
            "path":self.path,
            "type":self.type_obj
        }