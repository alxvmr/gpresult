'''
Поолучение информации о системе (домен и т.д.)
'''
import distro
import datetime
import os
import pwd
import gettext

gettext.bindtextdomain("gpr_system", "locales")
gettext.textdomain("gpr_system")
t = gettext.translation("gpr_system", localedir="../locales", languages=['ru_RU'])
t.install()
_ = t.gettext

def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y %H:%M")


def os_conf():
    os_id, os_version, os_name = distro.linux_distribution()
    return [[_("OS Configuration:"), os_id],
            [_("OS Version:"), f"{os_version} ({os_name})"]]

def get_user_home_dir():
    home_dir = os.path.expanduser("~")
    return [_("Local Profile:"), home_dir]

## @brief   Defining uid by username.
#  @param   name User or machine name.
#  @todo    Replace getpwnam.
#  @return	User uid.
def get_uid_from_name(name):
    try:
        pw = pwd.getpwnam(name)
    except KeyError as e:
        exit()
    uid = pw.pw_uid
    return uid

if __name__ == "__main__":
    os_conf()
