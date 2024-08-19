import gi

gi.require_version("Gvdb", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gvdb
from gi.repository import GLib

import gpr_system
import ast


def get_policies(name=None, type='standard', with_guid=False, cmd=None, cmd_name=None):
    uid = None
    policies = None
    policies_guid = None

    if name:
        uid = gpr_system.get_uid_from_name(name)
    path = gpr_system.get_path_to_policy(uid)

    if type == 'standard' or type == "verbose" or type == "raw":
        if cmd == "guid":
            policies = get_applied_policy_verbose_by_guid(path, cmd_name)
        elif cmd == "name":
            policies = get_applied_policy_verbose_by_name(path, cmd_name)
        else:
            policies = get_applied_policy_names_verbose(path)
    if with_guid:
        policies_guid = get_policy_name_with_guid(path)

    return (policies, policies_guid)


def get_applied_policy_verbose_by_guid(path, guid):
    applied_policy_with_names = get_applied_policy_names_verbose(path)
    name_with_guid = get_policy_name_with_guid(path)

    policy_name = [key for key, val in name_with_guid.items() if val == guid] # Is it possible to get multiple display_name for a policy guid ?...

    if policy_name and policy_name[0] in applied_policy_with_names.keys():
        return applied_policy_with_names[policy_name[0]]

    return None


def get_applied_policy_verbose_by_name(path, cmd_name):
    applied_policy_with_names = get_applied_policy_names_verbose(path)

    if cmd_name in applied_policy_with_names.keys():
        return applied_policy_with_names[cmd_name]

    return None


def get_applied_policy_names_verbose(path):
    policies = get_all_policies(path)
    applied_policy_verbose = {}

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
                applied_policy_verbose.setdefault(meta['policy_name'], []).append([k[7:], value_of_key_policy, meta])

    return applied_policy_verbose


def get_policy_name_with_guid(path):
    policies = get_all_policies(path)
    policy_path_name_guid = {}
    policy_name_guid = {}

    for k, v in zip(policies['keys'][:], policies['values'][:]):
        if (k.find('GpoPriority') != -1) and (v != None):
            if k[-12:] == 'display_name' and v.get_type().equal(GLib.VariantType.new("s")):
                policy_path_name_guid.setdefault(k[:-12], {}).update({k[-12:]: v.get_string()})
            elif k[-4:] == 'name' and v.get_type().equal(GLib.VariantType.new("s")):
                policy_path_name_guid.setdefault(k[:-4], {}).update({k[-4:]: v.get_string()})

    for path, d in policy_path_name_guid.items():
        name = None
        guid = None

        for k, v in d.items():
            if k == 'display_name':
                name = v
            else:
                guid = v

        policy_name_guid[name] = guid

    return policy_name_guid


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
