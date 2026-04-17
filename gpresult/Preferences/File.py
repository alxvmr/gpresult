import gettext
from typing import ClassVar

from .BasePreference import BasePreference

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


class File(BasePreference):
    preference_type = _("File")
    files: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fromPath = kwargs.get("fromPath")
        self.source = kwargs.get("source")
        self.action = kwargs.get("action")
        self.targetPath = kwargs.get("targetPath")
        self.readOnly = kwargs.get("readOnly")
        self.archive = kwargs.get("archive")
        self.hidden = kwargs.get("hidden")
        self.suppress = kwargs.get("suppress")
        self.executable = kwargs.get("executable")

        File.set_file(self)

    @classmethod
    def set_file(cls, file):
        cls.files.setdefault(file.policy_name, []).append(file)

    def get_info_list(self):

        return [
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
