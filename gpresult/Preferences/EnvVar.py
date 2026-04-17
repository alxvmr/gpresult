import gettext
from typing import ClassVar

from .BasePreference import BasePreference

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


class EnvVar(BasePreference):
    preference_type = _("Environment variables")
    envvars: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = kwargs.get("name")
        self.value = kwargs.get("value")
        self.action = kwargs.get("action")
        EnvVar.set_envvar(self)

    @classmethod
    def set_envvar(cls, envvar):
        cls.envvars.setdefault(envvar.policy_name, []).append(envvar)

    def get_info_list(self):

        return [
            [_("Type"), EnvVar.preference_type],
            [_("Name"), self.name],
            [_("Value"), self.value],
            [_("Action"), self.action],
            [_("Disabled"), self.disabled],
            [_("Remove policy"), self.remove_policy],
        ]
