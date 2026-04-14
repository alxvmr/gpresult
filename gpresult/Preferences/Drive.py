import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext


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
        self.disabled = kwargs.get("disabled", None)
        self.remove_policy = kwargs.get("remove_policy", None)
        self.uid = kwargs.get("uid", None)
        self.bypass_errors = kwargs.get("bypass_errors", None)
        self.apply_once = kwargs.get("apply_once", None)
        self.changed = kwargs.get("changed", None)
        self.filters = kwargs.get("filters", None)

        Drive.set_drive(self)


    @classmethod
    def set_drive(cls, drive):
        cls.drives.setdefault(drive.policy_name, []).append(drive)


    def _format_filters(self):
        if not self.filters:
            return None
        lines = []
        for f in self.filters:
            if isinstance(f, dict):
                for filter_type, attrs in f.items():
                    lines.append(_("Filter type") + ': ' + filter_type)
                    if isinstance(attrs, dict):
                        for key, val in attrs.items():
                            lines.append('  ' + _(key.capitalize()) + ': ' + str(val))
        return '\n'.join(lines) if lines else None


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

    def get_lifecycle_info_list(self):
        return [
            [_("UID"), self.uid],
            [_("Bypass errors"), self.bypass_errors],
            [_("Apply once"), self.apply_once],
            [_("Changed"), self.changed],
            [_("Filters"), self._format_filters()],
        ]