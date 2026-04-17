import gettext
from typing import ClassVar

from .BasePreference import BasePreference

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


class Inifile(BasePreference):
    preference_type = _("Inifile")
    inifiles: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.path = kwargs.get("path")
        self.section = kwargs.get("section")
        self.property = kwargs.get("property")
        self.value = kwargs.get("value")
        self.action = kwargs.get("action")

        Inifile.set_inifile(self)

    @classmethod
    def set_inifile(cls, ini):
        cls.inifiles.setdefault(ini.policy_name, []).append(ini)

    def get_info_list(self):

        return [
            [_("Type"), Inifile.preference_type],
            [_("Path"), self.path],
            [_("Section"), self.section],
            [_("Property"), self.property],
            [_("Value"), self.value],
            [_("Action"), self.action],
            [_("Disabled"), self.disabled],
            [_("Remove policy"), self.remove_policy],
        ]
