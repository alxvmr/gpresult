class EnvVar:
    preference_type = "Environment variables"
    envvars = {}

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.value = kwargs.get("value", None)
        self.action = kwargs.get("action", None)
        self.policy_name = kwargs.get("policy_name", None)

        EnvVar.set_envvar(self)


    @classmethod
    def set_envvar(cls, envvar):
        cls.envvars.setdefault(envvar.policy_name, []).append(envvar)


    def get_info_list(self):

        return [
            ["Type", EnvVar.preference_type],
            ["Value", self.value],
            ["Action", self.action],
        ]