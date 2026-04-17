import gettext
from typing import ClassVar

from .BasePreference import BasePreference

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


class Shortcut(BasePreference):
    preference_type = _("Shortcut")
    shortcuts: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dest = kwargs.get("dest")
        self.path = kwargs.get("path")
        self.expanded_path = kwargs.get("expanded_path")
        self.arguments = kwargs.get("arguments")
        self.name = kwargs.get("name")
        self.action = kwargs.get("action")
        self.changed = kwargs.get("changed")
        self.icon = kwargs.get("icon")
        self.comment = kwargs.get("comment")
        self.is_in_user_context = kwargs.get("is_in_user_context")
        self.type = kwargs.get("type")
        self.desktop_file_template = kwargs.get("desktop_file_template")

        Shortcut.set_shortcut(self)

    @classmethod
    def set_shortcut(cls, shortcut):
        cls.shortcuts.setdefault(shortcut.policy_name, []).append(shortcut)

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
