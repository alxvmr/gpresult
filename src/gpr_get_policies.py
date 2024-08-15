import gi

gi.require_version("Gvdb", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gvdb
from gi.repository import GLib

import gpr_system
import ast


def get_policies(name=None, type='standard', with_id=False):
    uid = None
    policies = None
    policies_id = None

    if name:
        uid = gpr_system.get_uid_from_name(name)
    path = gpr_system.get_path_to_policy(uid)

    if type == 'standard' or type == "with_keys" or type == "verbose":
        policies = get_applied_policy_names(path)
    if with_id:
        policies_id = get_policy_name_with_id(path)

    return (policies, policies_id)


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


def get_policy_name_with_id(path):
    policies = get_all_policies(path)
    policy_path_name_id = {}
    policy_name_id = {}

    for k, v in zip(policies['keys'][:], policies['values'][:]):
        if (k.find('GpoPriority') != -1) and (v != None):
            if k[-12:] == 'display_name' and v.get_type().equal(GLib.VariantType.new("s")):
                policy_path_name_id.setdefault(k[:-12], {}).update({k[-12:]: v.get_string()})
            elif k[-4:] == 'name' and v.get_type().equal(GLib.VariantType.new("s")):
                policy_path_name_id.setdefault(k[:-4], {}).update({k[-4:]: v.get_string()})
    
    for path, d in policy_path_name_id.items():
        name = None
        id = None

        for k, v in d.items():
            if k == 'display_name':
                name = v
            else:
                id = v
        
        policy_name_id[name] = id
    
    return policy_name_id


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
