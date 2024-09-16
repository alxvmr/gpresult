class NetworkShare():
    preference_type = "Network share"
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
            ["Type", NetworkShare.preference_type],
            ["Name", self.name],
            ["Action", self.action],
            ["Path", self.path],
            ["All regular", self.allRegular],
            ["Abe", self.abe],
            ["Limit users", self.limitUsers],
            ["Comment", self.comment],
        ]