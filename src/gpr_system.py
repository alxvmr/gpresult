'''
Поолучение информации о системе (домен и т.д.)
'''
import distro
import datetime
import os
import logging
import pwd

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
file_handler = logging.FileHandler('../logs/gpr_get_policies.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y %H:%M")


def os_conf():
    os_id, os_version, os_name = distro.linux_distribution()
    return {"OS Configuration:": os_id,
            "OS Version:": f"{os_version} ({os_name})"}

def get_user_home_dir():
    home_dir = os.path.expanduser("~")
    return {"Local Profile:": home_dir}

## @brief   Defining uid by username.
#  @param   name User or machine name.
#  @todo    Replace getpwnam.
#  @return	User uid.
def get_uid_from_name(name):
    try:
        pw = pwd.getpwnam(name)
    except KeyError as e:
        logger.error(_("An entry for the name {} could not be found. The user or machine name may be incorrect.").format(name))
        exit()
    uid = pw.pw_uid
    return uid

if __name__ == "__main__":
    os_conf()
