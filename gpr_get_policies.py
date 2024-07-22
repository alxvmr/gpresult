'''
Модуль для чтения политик с фильтрацией
'''
import gi
import pwd

gi.require_version("Gvdb", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gvdb
from gi.repository import GLib


PATH_DB = "/etc/dconf/db/policy"

'''
TODO: убрать getpwnam
'''
def get_uid_from_name(name):
    pw = pwd.getpwnam(name)
    uid = pw.pw_uid
    return uid

def get_path_to_policy(uid=None):
    if uid:
        return PATH_DB + str(uid)
    return PATH_DB

def get_policies(name=None):
    uid = None
    if name:
        uid = get_uid_from_name(name)
    path = get_path_to_policy(uid)
    policies = get_non_empty_keys_policies(path)
    return policies

def get_non_empty_keys_policies(path):
    policies = get_all_policies(path)
    for k, v in zip(policies['keys'][:], policies['values'][:]):
        if not v:
            policies['keys'].remove(k)
            policies['values'].remove(v)
    return(policies)

def get_all_policies(path):
    is_not_empty, bytes = GLib.file_get_contents(path)
    bytes = GLib.Bytes.new(bytes)
    if (is_not_empty):
        table = Gvdb.Table.new_from_bytes(bytes, True)

        key_list = Gvdb.Table.get_names(table)
        value_list = []
        for key in key_list:
            value = Gvdb.Table.get_value(table, key)
            value_list.append(value)

        return {"keys": key_list,
                "values": value_list}
