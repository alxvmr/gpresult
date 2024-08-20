class KeyValue:
    keys_values = []

    def __init__(self, key, value, obj, **kwargs):
        self.key = key
        self.value = value
        self.obj = obj
        self.policy_name = kwargs.get("policy_name", None)
        self.type = kwargs.get("type", None)
        self.reloaded = kwargs.get("reloaded_with_policy_key", None)
        self.is_list = kwargs.get("is_list", None)

        KeyValue.keys_values.append(self)


    def get_info_list(self):
        return [self.key, self.value, {"type": self.type, "is_list": self.is_list}]

    
    @classmethod
    def set_meta_to_key_value(cls, key, obj, **kwargs):
        for kv in cls.keys_values:
            if kv.key == key and kv.obj == obj:
                kv.policy_name = kwargs.get("policy_name", None)
                kv.type = kwargs.get("type", None)
                kv.reloaded = kwargs.get("reloaded_with_policy_key", None)
                kv.is_list = kwargs.get("is_list", None)
                return
            
        return False


    @classmethod
    def get_all_keys_values(cls, obj=None):
        if not obj:
            return cls.keys_values
        else:
            kvs = []
            for kv in cls.keys_values:
                if kv.obj == obj:
                    kvs.append(kv)
            return kvs
