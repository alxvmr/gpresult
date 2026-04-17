import gettext

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


class BasePreference:
    def __init__(self, **kwargs):
        self.policy_name = kwargs.get("policy_name", None)
        self.disabled = kwargs.get("disabled", None)
        self.remove_policy = kwargs.get("remove_policy", None)

        self.uid = kwargs.get("uid", None)
        self.bypass_errors = kwargs.get("bypass_errors", None)
        self.apply_once = kwargs.get("apply_once", None)
        self.changed = kwargs.get("changed", None)
        self.filters = kwargs.get("filters", None)

    def _format_filters(self):
        if not self.filters:
            return None

        lines = []
        for f in self.filters:
            if isinstance(f, dict):
                for filter_type, attrs in f.items():
                    lines.append(_("Filter type") + ": " + filter_type)
                    if isinstance(attrs, dict):
                        for key, val in attrs.items():
                            lines.append("  " + _(key.capitalize()) + ": " + str(val))
        return "\n".join(lines) if lines else None

    def get_lifecycle_info_list(self):
        lifecycle = [
            [_("UID"), self.uid],
            [_("Bypass errors"), self.bypass_errors],
            [_("Apply once"), self.apply_once],
        ]

        if hasattr(self, "changed"):
            lifecycle.append([_("Changed"), self.changed])

        lifecycle.append([_("Filters"), self._format_filters()])
        return lifecycle

    def get_info_list(self):
        raise NotImplementedError("Subclasses must implement get_info_list()")
