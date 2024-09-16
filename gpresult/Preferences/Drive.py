class Drive:
    preference_type = "Drive map"
    drives = {}

    def __init__(self, **kwargs):
        self.login = kwargs.get("login", None)
        self.password = kwargs.get("password", None)
        self.dir = kwargs.get("dir", None)
        self.path = kwargs.get("path", None)
        self.action = kwargs.get("action", None)
        self.thisDrive = kwargs.get("thisDrive", None)
        self.allDrives = kwargs.get("allDrives", None)
        self.label = kwargs.get("label", None)
        self.persistent = kwargs.get("persistent", None)
        self.useLetter = kwargs.get("useLetter", None)
        self.policy_name = kwargs.get("policy_name", None)

        Drive.set_drive(self)


    @classmethod
    def set_drive(cls, drive):
        cls.drives.setdefault(drive.policy_name, []).append(drive)


    def get_info_list(self):

        return [
            ["Type", Drive.preference_type],
            ["Password", self.password],
            ["Direction", self.dir],
            ["Path", self.path],
            ["Action", self.action],
            ["This drive", self.thisDrive],
            ["All drives", self.allDrives],
            ["Label", self.label],
            ["Persistent", self.persistent],
            ["Use letter", str(self.useLetter)],
        ]