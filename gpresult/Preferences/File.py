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

        File.set_file(self)


    @classmethod
    def set_file(cls, file):
        cls.files.setdefault(file.policy_name, []).append(file)


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
        ]