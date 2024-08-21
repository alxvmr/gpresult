import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("gpresult", "locales")
gettext.textdomain("gpresult")
t = gettext.translation("gpresult", 
                        localedir="/usr/lib/python3/site-packages/gpresult/locales", 
                        languages=[loc])
t.install()
_ = t.gettext


class GPO:
    gpos = [] # List of all GPOs retrieved from /etc/dconf/db/policy<guid>

    def __init__(self, obj, **kwargs):
        self.path = kwargs.get("correct_path", None)  # Sysvol path
        self.name = kwargs.get("display_name", None)  # Displayed GPO name
        self.guid = kwargs.get("name", None)          # GUID
        self.version = kwargs.get("version", None)    # Version
        self.obj = obj                                # Whether the GPO refers to a machine or user object
        self.keys_values = []                         # List of keys and values related to GPOs

        GPO.set_gpo(self)


    def get_info_list(self):
        kvs = self.get_keys_values_lists()
        if not kvs:
            kvs = None

        return [
            ["GPO", self.name],
            [_("Path"), self.path],
            [_("Version"), self.version],
            ["GUID", self.guid],
            [_("Keys and values"), kvs]
        ]
    

    def get_keys_values_lists(self):
        kvs_list = []

        for kv in self.get_sorted_keys_values():
            kvs_list.append(kv.get_info_list())

        return kvs_list

    
    def get_sorted_keys_values(self):
        return sorted(self.keys_values, key=lambda x: x.key)
    

    @classmethod
    def get_all_sorted_keys_values(cls):
        kv_list = []
        for gpo in cls.gpos:
            kv_list.extend(gpo.keys_values)

        return sorted(kv_list, key=lambda x: x.key)


    @classmethod
    def get_gpo_by_guid(cls, guid, obj=None):
        for gpo in cls.gpos:
            if gpo.guid == guid:
                if obj and gpo.obj == obj:
                    return gpo
                elif not obj:
                    return gpo
                
        return None
    

    @classmethod
    def get_gpo_by_name(cls, name, obj=None):
        for gpo in cls.gpos:
            if gpo.name == name:
                if obj and gpo.obj == obj:
                    return gpo
                elif not obj:
                    return gpo
                
        return None


    @classmethod
    def set_keys_values(cls, kv):
        kv_policy_name = kv.policy_name
        
        for gpo in cls.gpos:
            if gpo.name == kv_policy_name and gpo.obj == kv.obj:
                gpo.keys_values.append(kv)
                return
            
        return False


    @classmethod
    def set_gpo(cls, gpo):
        guid = gpo.guid
        obj = gpo.obj

        for e in cls.gpos:
            if e.guid == guid and e.obj == obj:
                e.path = gpo.path if not e.path else e.path
                e.name = gpo.name if not e.name else e.name
                e.version = gpo.version if not e.version else e.version
                return
            
        cls.gpos.append(gpo)


    @classmethod
    def get_all_gpos(cls, obj=None):
        if not obj:
            return cls.gpos
        else:
            return [gpo for gpo in cls.gpos if gpo.obj == obj]