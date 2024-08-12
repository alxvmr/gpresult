'''
Поолучение информации о системе (домен и т.д.)
'''
import distro
import datetime
import os

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



if __name__ == "__main__":
    os_conf()
