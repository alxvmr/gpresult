class Shortcut:
    preference_type = "Shortcut"
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
        self.policy_name = kwargs.get("policy_name", None)

        Shortcut.set_shortcut(self)


    @classmethod
    def set_shortcut(cls, shortcut):
        cls.shortcuts.setdefault(shortcut.policy_name, []).append(shortcut)


    def get_info_list(self):

        return [
            ["Type", Shortcut.preference_type],
            ["Destination", self.dest],
            ["Path", self.path],
            ["Expanded path", self.expanded_path],
            ["Arguments", self.arguments],
            ["Name", self.name],
            ["Action", self.action],
            ["Changed", self.changed],
            ["Icon", self.icon],
            ["Comment", self.comment],
            ["Perfom action in user context", self.is_in_user_context],
        ]
