import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext


class File():
    preference_type = _("File")
    files = {}

    def __init__(self, **kwargs):
        self.fromPath = kwargs.get("fromPath", None)
        self.source = kwargs.get("source", None)
        self.action = kwargs.get("action", None)
        self.targetPath = kwargs.get("targetPath", None)
        self.readOnly = kwargs.get("readOnly", None)
        self.archive = kwargs.get("archive", None)
        self.hidden = kwargs.get("hidden", None)
        self.suppress = kwargs.get("suppress", None)
        self.executable = kwargs.get("executable", None)
        self.policy_name = kwargs.get("policy_name", None)
        self.disabled = kwargs.get("disabled", None)
        self.remove_policy = kwargs.get("remove_policy", None)
        self.uid = kwargs.get("uid", None)
        self.bypass_errors = kwargs.get("bypass_errors", None)
        self.apply_once = kwargs.get("apply_once", None)
        self.changed = kwargs.get("changed", None)
        self.filters = kwargs.get("filters", None)

        File.set_file(self)


    @classmethod
    def set_file(cls, file):
        cls.files.setdefault(file.policy_name, []).append(file)


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

        return[
            [_("Type"), File.preference_type],
            [_("From path"), self.fromPath],
            [_("Source"), self.source],
            [_("Action"), self.action],
            [_("Target path"), self.targetPath],
            [_("Read only"), self.readOnly],
            [_("Archive"), self.archive],
            [_("Hidden"), self.hidden],
            [_("Suppress"), self.suppress],
            [_("Executable"), self.executable],
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