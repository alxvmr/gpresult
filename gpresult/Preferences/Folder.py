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

        Folder.set_folder(self)


    @classmethod
    def set_folder(cls, folder):
        cls.folders.setdefault(folder.policy_name, []).append(folder)


    def get_info_list(self):

        return [
            [_("Type"), Folder.preference_type],
            [_("Path"), self.path],
            [_("Action"), self.action],
            [_("Delete folder"), self.delete_folder],
            [_("Delete subfolder"), self.delete_sub_folder],
            [_("Delete files"), self.delete_files],
            [_("Hidden folder"), self.hidden_folder],
        ]