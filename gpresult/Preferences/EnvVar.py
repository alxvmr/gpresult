import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext


class EnvVar:
    preference_type = _("Environment variables")
    envvars = {}

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.value = kwargs.get("value", None)
        self.action = kwargs.get("action", None)
        self.policy_name = kwargs.get("policy_name", None)
        self.disabled = kwargs.get("disabled", None)
        self.remove_policy = kwargs.get("remove_policy", None)

        EnvVar.set_envvar(self)


    @classmethod
    def set_envvar(cls, envvar):
        cls.envvars.setdefault(envvar.policy_name, []).append(envvar)


    def get_info_list(self):

        return [
            [_("Type"), EnvVar.preference_type],
            [_("Name"), self.name],
            [_("Value"), self.value],
            [_("Action"), self.action],
            [_("Disabled"), self.disabled],
            [_("Remove policy"), self.remove_policy],
        ]