import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext


class Inifile:
    preference_type = _("Inifile")
    inifiles = {}

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", None)
        self.section = kwargs.get("section", None)
        self.property = kwargs.get("property", None)
        self.value = kwargs.get("value", None)
        self.action = kwargs.get("action", None)
        self.policy_name = kwargs.get("policy_name", None)
        self.disabled = kwargs.get("disabled", None)
        self.remove_policy = kwargs.get("remove_policy", None)
        self.uid = kwargs.get("uid", None)
        self.bypass_errors = kwargs.get("bypass_errors", None)
        self.apply_once = kwargs.get("apply_once", None)
        self.changed = kwargs.get("changed", None)
        self.filters = kwargs.get("filters", None)

        Inifile.set_inifile(self)


    @classmethod
    def set_inifile(cls, ini):
        cls.inifiles.setdefault(ini.policy_name, []).append(ini)


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
            [_("Type"), Inifile.preference_type],
            [_("Path"), self.path],
            [_("Section"), self.section],
            [_("Property"), self.property],
            [_("Value"), self.value],
            [_("Action"), self.action],
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