import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext


class Shortcut:
    preference_type = _("Shortcut")
    shortcuts = {}

    def __init__(self, **kwargs):
        self.dest = kwargs.get("dest", None)
        self.path = kwargs.get("path", None)
        self.expanded_path = kwargs.get("expanded_path", None)
        self.arguments = kwargs.get("arguments", None)
        self.name = kwargs.get("name", None)
        self.action = kwargs.get("action", None)
        self.changed = kwargs.get("changed", None)
        self.icon = kwargs.get("icon", None)
        self.comment = kwargs.get("comment", None)
        self.is_in_user_context = kwargs.get("is_in_user_context", None)
        self.type = kwargs.get("type", None)
        self.desktop_file_template = kwargs.get("desktop_file_template", None)
        self.policy_name = kwargs.get("policy_name", None)
        self.disabled = kwargs.get("disabled", None)
        self.remove_policy = kwargs.get("remove_policy", None)
        self.uid = kwargs.get("uid", None)
        self.bypass_errors = kwargs.get("bypass_errors", None)
        self.apply_once = kwargs.get("apply_once", None)
        self.filters = kwargs.get("filters", None)

        Shortcut.set_shortcut(self)


    @classmethod
    def set_shortcut(cls, shortcut):
        cls.shortcuts.setdefault(shortcut.policy_name, []).append(shortcut)


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
            [_("Type"), Shortcut.preference_type],
            [_("Destination"), self.dest],
            [_("Path"), self.path],
            [_("Expanded path"), self.expanded_path],
            [_("Arguments"), self.arguments],
            [_("Name"), self.name],
            [_("Action"), self.action],
            [_("Changed"), self.changed],
            [_("Icon"), self.icon],
            [_("Comment"), self.comment],
            [_("Perfom action in user context"), self.is_in_user_context],
            [_("Link type"), self.type],
            [_("Desktop file template"), self.desktop_file_template],
            [_("Disabled"), self.disabled],
            [_("Remove policy"), self.remove_policy],
        ]

    def get_lifecycle_info_list(self):
        return [
            [_("UID"), self.uid],
            [_("Bypass errors"), self.bypass_errors],
            [_("Apply once"), self.apply_once],
            [_("Filters"), self._format_filters()],
        ]
