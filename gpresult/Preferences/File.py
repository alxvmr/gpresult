class File():
    preference_type = "File"
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
            ["Type", File.preference_type],
            ["From path", self.fromPath],
            ["Source", self.source],
            ["Action", self.action],
            ["Target path", self.targetPath],
            ["Read only", self.readOnly],
            ["Archive", self.archive],
            ["Hidden", self.hidden],
            ["Suppress", self.suppress],
            ["Executable", self.executable],
        ]