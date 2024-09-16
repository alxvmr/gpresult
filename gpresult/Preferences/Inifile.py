class Inifile:
    preference_type = "Inifile"
    inifiles = {}

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", None)
        self.section = kwargs.get("section", None)
        self.property = kwargs.get("property", None)
        self.value = kwargs.get("value", None)
        self.action = kwargs.get("action", None)
        self.policy_name = kwargs.get("policy_name", None)

        Inifile.set_inifile(self)


    @classmethod
    def set_inifile(cls, ini):
        cls.inifiles.setdefault(ini.policy_name, []).append(ini)


    def get_info_list(self):

        return [
            ["Type", Inifile.preference_type],
            ["Path", self.path],
            ["Section", self.section],
            ["Property", self.property],
            ["Value", self.value],
            ["Action", self.action],
        ]