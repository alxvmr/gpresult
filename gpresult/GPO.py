import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("GPO", "locales")
gettext.textdomain("GPO")
t = gettext.translation("GPO",
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
        self.preferences = []                         # Preferences list

        GPO.set_gpo(self)

    # This is needed to use set in the --list output
    # to remove repetition
    def __eq__(self, other):
        if isinstance(other, GPO):
            return (self.path == other.path and
                    self.name == other.name and
                    self.guid == other.guid and
                    self.version == other.version)
        return NotImplemented

    def get_info_list(self, with_previous=True):
        kvs = self.get_keys_values_lists(with_previous)
        prefs = self.get_preferences_lists()

        if not kvs:
            kvs = None

        if not prefs:
            prefs = None

        return [
            ["GPO", self.name],
            [_("Path"), self.path],
            [_("Version"), self.version],
            ["GUID", self.guid],
            [_("Keys"), kvs],
            [_("Preferences"), prefs],

        ]


    def get_keys_values_lists(self, with_previous=True):
        kvs_list = []

        for kv in self.get_sorted_keys_values():
            kvs_list.append(kv.get_info_list(with_previous))

        return kvs_list


    def get_preferences_lists(self):
        prefs_list = []

        for pref in self.preferences:
            prefs_list.append(pref.get_info_list())

        return prefs_list


    def get_sorted_keys_values(self):
        return sorted(self.keys_values, key=lambda x: x.key)


    @classmethod
    def get_all_sorted_keys_values(cls):
        kv_list = []
        for gpo in cls.gpos:
            kv_list.extend(gpo.keys_values)

        return sorted(kv_list, key=lambda x: x.key)


    @classmethod
    def get_gpos_by_guid(cls, guid, obj=None):
        gpos_res = []

        for gpo in cls.gpos:
            if gpo.guid == guid:
                if (obj and gpo.obj == obj) or not obj:
                    gpos_res.append(gpo)

        return gpos_res


    @classmethod
    def get_gpos_by_name(cls, name, obj=None):
        gpos_res = []

        for gpo in cls.gpos:
            if gpo.name == name:
                if (obj and gpo.obj == obj) or not obj:
                    gpos_res.append(gpo)

        return gpos_res


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


    @classmethod
    def set_preferences(cls, gpo_name, prefs):
        for gpo in cls.gpos:
            if gpo.name == gpo_name:
                for pref in prefs:
                    if pref.obj == gpo.obj:
                        gpo.preferences.append(pref)
