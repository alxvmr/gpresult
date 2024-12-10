class KeyValue:
    keys_values = [] # List of all GPO keys and values retrieved from /etc/dconf/db/policy<guid>

    def __init__(self, key, value, obj, **kwargs):
        self.key = key                                                   # GPO key
        self.value = value                                               # Key value
        self.obj = obj                                                   # Which object the pair refers to - the machine or the user
        self.policy_name = kwargs.get("policy_name", None)               # The name of the GPO to which the pair belongs
        self.type = kwargs.get("type", None)                             # Value data type
        self.reloaded = kwargs.get("reloaded_with_policy_key", None)     # Value data type
        self.is_list = kwargs.get("is_list", None)                       # Whether the value is a list
        self.mod_previous_value = kwargs.get("mod_previous_value", None) # Previous value

        KeyValue.keys_values.append(self)


    def get_info_list(self):

        return [self.key, self.value, self.mod_previous_value, {"type": self.type, "is_list": self.is_list}]

    
    @classmethod
    def set_meta_to_key_value(cls, key, obj, **kwargs):
        for kv in cls.keys_values:
            if kv.key == key and kv.obj == obj:
                kv.policy_name = kwargs.get("policy_name", None)
                kv.type = kwargs.get("type", None)
                kv.reloaded = kwargs.get("reloaded_with_policy_key", None)
                kv.is_list = kwargs.get("is_list", None)
                kv.mod_previous_value = kwargs.get("mod_previous_value", None)
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
