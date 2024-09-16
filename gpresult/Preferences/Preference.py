from .Folder import Folder
from .Inifile import Inifile
from .Shortcut import Shortcut
from .EnvVar import EnvVar
from .Drive import Drive
from .File import File
from .Networkshare import NetworkShare


class Preference:
    preferences = {}

    def __init__(self, obj, pref_type, **kwargs):
        self.obj = obj
        self.type = pref_type
        self.policy_name = kwargs.get("policy_name", None)

        if pref_type == "Folders":
            self.preference_obj = Folder(**kwargs)
        elif pref_type == "Inifiles":
            self.preference_obj = Inifile(**kwargs)
        elif pref_type == "Shortcuts":
            self.preference_obj = Shortcut(**kwargs)
        elif pref_type == "Environmentvariables":
            self.preference_obj = EnvVar(**kwargs)
        elif pref_type == "Drives":
            self.preference_obj = Drive(**kwargs)
        elif pref_type == "Files":
            self.preference_obj = File(**kwargs)
        elif pref_type == "Networkshares":
            self.preference_obj = NetworkShare(**kwargs)

        Preference.set_preference(self)


    @classmethod
    def set_preference(cls, pref):
        cls.preferences.setdefault(pref.policy_name, []).append(pref)


    @classmethod
    def clear_preferences(cls):
        cls.preferences.clear()


    def get_info_list(self):
        if self.preference_obj:
            pref_info = [self.preference_obj.get_info_list(), {'lbr': True, 'is_list': True}]
            return pref_info
            
        return None