import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("Drive", "locales")
gettext.textdomain("Drive")
t = gettext.translation("Drive",
                        localedir="/usr/lib/python3/site-packages/gpresult/locales",
                        languages=[loc])
t.install()
_ = t.gettext


class Drive:
    preference_type = _("Drive map")
    drives = {}

    def __init__(self, **kwargs):
        self.login = kwargs.get("login", None)
        self.password = kwargs.get("password", None)
        self.dir = kwargs.get("dir", None)
        self.path = kwargs.get("path", None)
        self.action = kwargs.get("action", None)
        self.thisDrive = kwargs.get("thisDrive", None)
        self.allDrives = kwargs.get("allDrives", None)
        self.label = kwargs.get("label", None)
        self.persistent = kwargs.get("persistent", None)
        self.useLetter = kwargs.get("useLetter", None)
        self.policy_name = kwargs.get("policy_name", None)

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
        ]