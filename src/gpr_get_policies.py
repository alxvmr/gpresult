import gi

gi.require_version("Gvdb", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gvdb
from gi.repository import GLib

import gpr_system
import ast


def get_policies(name=None, type='standart'):
    uid = None
    policies = None

    if name:
        uid = gpr_system.get_uid_from_name(name)
    path = gpr_system.get_path_to_policy(uid)

    if type == 'standart' or type == "with_keys" or type == "verbose":
        policies = get_applied_policy_names(path)

    return policies


def get_applied_policy_names(path):
    policies = get_all_policies(path)
    applied_policy_with_keys = {}

    for k, v in zip(policies['keys'][:], policies['values'][:]):
        if (k[:7] == '/Source') and (v != None):
            if v.get_type().equal(GLib.VariantType.new("s")):
                meta = ast.literal_eval(v.get_string())
                
            software = k[7:]
            index_software = policies['keys'].index(software)
            value_of_key_policy = policies['values'][index_software]

            if value_of_key_policy.get_type().equal(GLib.VariantType.new("s")):
                value_of_key_policy = value_of_key_policy.get_string()

            if ('policy_name' in meta) and (meta['policy_name'] != ''):
                applied_policy_with_keys.setdefault(meta['policy_name'], []).append([k, value_of_key_policy, meta])

    return applied_policy_with_keys


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
    
    return {"keys": [],
            "values": []}
