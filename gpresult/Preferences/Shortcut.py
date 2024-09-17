import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("Shortcut", "locales")
gettext.textdomain("Shortcut")
t = gettext.translation("Shortcut",
                        localedir="/usr/lib/python3/site-packages/gpresult/locales",
                        languages=[loc])
t.install()
_ = t.gettext


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
        ]
