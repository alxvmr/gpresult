import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("EnvVar", "locales")
gettext.textdomain("EnvVar")
t = gettext.translation("EnvVar",
                        localedir="/usr/lib/python3/site-packages/gpresult/locales",
                        languages=[loc])
t.install()
_ = t.gettext


class EnvVar:
    preference_type = _("Environment variables")
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
            [_("Type"), EnvVar.preference_type],
            [_("Value"), self.value],
            [_("Action"), self.action],
        ]