import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext


class Folder:
    preference_type = _("Folder")
    folders = {}

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", None)
        self.action = kwargs.get("action", None)
        self.delete_folder = kwargs.get("delete_folder", None)
        self.delete_sub_folder = kwargs.get("delete_sub_folder", None)
        self.delete_files = kwargs.get("delete_files", None)
        self.hidden_folder = kwargs.get("hidden_folder", None)
        self.policy_name = kwargs.get("policy_name", None)
        self.disabled = kwargs.get("disabled", None)
        self.remove_policy = kwargs.get("remove_policy", None)
        self.uid = kwargs.get("uid", None)
        self.bypass_errors = kwargs.get("bypass_errors", None)
        self.apply_once = kwargs.get("apply_once", None)
        self.changed = kwargs.get("changed", None)
        self.filters = kwargs.get("filters", None)

        Folder.set_folder(self)


    @classmethod
    def set_folder(cls, folder):
        cls.folders.setdefault(folder.policy_name, []).append(folder)


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
            [_("Type"), Folder.preference_type],
            [_("Path"), self.path],
            [_("Action"), self.action],
            [_("Delete folder"), self.delete_folder],
            [_("Delete subfolder"), self.delete_sub_folder],
            [_("Delete files"), self.delete_files],
            [_("Hidden folder"), self.hidden_folder],
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