import distro
import datetime
import os
import pwd

import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("gpr_system", "locales")
gettext.textdomain("gpr_system")
t = gettext.translation("gpr_system", localedir="/usr/lib/python3/site-packages/gpresult/locales", languages=[loc])
t.install()
_ = t.gettext

PATH_DB = "/etc/dconf/db/policy"


def get_timestamp():
    now = datetime.datetime.now()

    return now.strftime("%d-%m-%Y %H:%M")


def os_conf():
    os_id, os_version, os_name = distro.linux_distribution()

    return [[_("Operating system:"), os_id],
            [_("OS Version:"), f"{os_version} ({os_name})"]]


def get_user_home_dir():
    home_dir = os.path.expanduser("~")

    return [_("Local Profile:"), home_dir]


def get_uid_from_name(name):
    try:
        pw = pwd.getpwnam(name)
    except KeyError as e:
        exit()

    uid = pw.pw_uid

    return uid


def get_path_to_policy(uid=None):
    if uid:
        return PATH_DB + str(uid)

    return PATH_DB
