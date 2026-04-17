import gettext
from typing import ClassVar

from .BasePreference import BasePreference

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


class Drive(BasePreference):
    preference_type = _("Drive map")
    drives: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.login = kwargs.get("login")
        self.password = kwargs.get("password")
        self.dir = kwargs.get("dir")
        self.path = kwargs.get("path")
        self.action = kwargs.get("action")
        self.thisDrive = kwargs.get("thisDrive")
        self.allDrives = kwargs.get("allDrives")
        self.label = kwargs.get("label")
        self.persistent = kwargs.get("persistent")
        self.useLetter = kwargs.get("useLetter")

        Drive.set_drive(self)

    @classmethod
    def set_drive(cls, drive):
        cls.drives.setdefault(drive.policy_name, []).append(drive)

    def get_info_list(self):

        return [
            [_("Type"), Drive.preference_type],
            [_("Password"), self.password],
            [_("Direction"), self.dir],
            [_("Path"), self.path],
            [_("Action"), self.action],
            [_("This drive"), self.thisDrive],
            [_("All drives"), self.allDrives],
            [_("Label"), self.label],
            [_("Persistent"), self.persistent],
            [_("Use letter"), str(self.useLetter)],
            [_("Disabled"), self.disabled],
            [_("Remove policy"), self.remove_policy],
        ]
