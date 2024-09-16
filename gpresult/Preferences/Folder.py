class Folder:
    preference_type = "Folder"
    folders = {}

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", None)
        self.action = kwargs.get("action", None)
        self.delete_folder = kwargs.get("delete_folder", None)
        self.delete_sub_folder = kwargs.get("delete_sub_folder", None)
        self.delete_files = kwargs.get("delete_files", None)
        self.hidden_folder = kwargs.get("action", None)
        self.policy_name = kwargs.get("policy_name", None)

        Folder.set_folder(self)


    @classmethod
    def set_folder(cls, folder):
        cls.folders.setdefault(folder.policy_name, []).append(folder)


    def get_info_list(self):

        return [
            ["Type", Folder.preference_type],
            ["Path", self.path],
            ["Action", self.action],
            ["Delete folder", self.delete_folder],
            ["Delete subfolder", self.delete_sub_folder],
            ["Delete files", self.delete_files],
            ["Hidden folder", self.hidden_folder],
        ]