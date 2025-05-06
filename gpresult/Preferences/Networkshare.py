import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext


class NetworkShare():
    preference_type = _("Network share")
    nshares = {}

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.action = kwargs.get("action", None)
        self.path = kwargs.get("path", None)
        self.allRegular = kwargs.get("allRegular", None)
        self.comment = kwargs.get("comment", None)
        self.limitUsers = kwargs.get("limitUsers", None)
        self.abe = kwargs.get("abe", None)
        self.policy_name = kwargs.get("policy_name", None)

        NetworkShare.set_nshare(self)


    @classmethod
    def set_nshare(cls, nshare):
        cls.nshares.setdefault(nshare.policy_name, []).append(nshare)


    def get_info_list(self):

        return [
            [_("Type"), NetworkShare.preference_type],
            [_("Name"), self.name],
            [_("Action"), self.action],
            [_("Path"), self.path],
            [_("All regular"), self.allRegular],
            [_("Abe"), self.abe],
            [_("Limit users"), self.limitUsers],
            [_("Comment"), self.comment],
        ]