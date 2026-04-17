import gettext
from typing import ClassVar

from .BasePreference import BasePreference

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


class NetworkShare(BasePreference):
    preference_type = _("Network share")
    nshares: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = kwargs.get("name")
        self.action = kwargs.get("action")
        self.path = kwargs.get("path")
        self.allRegular = kwargs.get("allRegular")
        self.comment = kwargs.get("comment")
        self.limitUsers = kwargs.get("limitUsers")
        self.abe = kwargs.get("abe")

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
            [_("Disabled"), self.disabled],
            [_("Remove policy"), self.remove_policy],
        ]
