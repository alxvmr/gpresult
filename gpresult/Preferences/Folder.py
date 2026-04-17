import gettext
from typing import ClassVar

from .BasePreference import BasePreference

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


class Folder(BasePreference):
    preference_type = _("Folder")
    folders: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.path = kwargs.get("path")
        self.action = kwargs.get("action")
        self.delete_folder = kwargs.get("delete_folder")
        self.delete_sub_folder = kwargs.get("delete_sub_folder")
        self.delete_files = kwargs.get("delete_files")
        self.hidden_folder = kwargs.get("hidden_folder")

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
            [_("Disabled"), self.disabled],
            [_("Remove policy"), self.remove_policy],
        ]
