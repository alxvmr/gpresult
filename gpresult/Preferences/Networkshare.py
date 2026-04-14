import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext


class NetworkShare():
    preference_type = _("Network share")
    nshares = {}

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.action = kwargs.get("action", None)
        self.path = kwargs.get("path", None)
        self.allRegular = kwargs.get("allRegular", None)
        self.comment = kwargs.get("comment", None)
        self.limitUsers = kwargs.get("limitUsers", None)
        self.abe = kwargs.get("abe", None)
        self.policy_name = kwargs.get("policy_name", None)
        self.disabled = kwargs.get("disabled", None)
        self.remove_policy = kwargs.get("remove_policy", None)
        self.uid = kwargs.get("uid", None)
        self.bypass_errors = kwargs.get("bypass_errors", None)
        self.apply_once = kwargs.get("apply_once", None)
        self.changed = kwargs.get("changed", None)
        self.filters = kwargs.get("filters", None)

        NetworkShare.set_nshare(self)


    @classmethod
    def set_nshare(cls, nshare):
        cls.nshares.setdefault(nshare.policy_name, []).append(nshare)


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
            [_("Type"), NetworkShare.preference_type],
            [_("Name"), self.name],
            [_("Action"), self.action],
            [_("Path"), self.path],
            [_("All regular"), self.allRegular],
            [_("Abe"), self.abe],
            [_("Limit users"), self.limitUsers],
            [_("Comment"), self.comment],
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