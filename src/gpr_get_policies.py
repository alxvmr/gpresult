##
# @file   gpr_get_policies.py
# @author Maria Alexeeva <alxvmr@altlinux.com>
# @brief  Reading policies (with filtering).
#
# This file provides functions to read policies 
# from the binary file /etc/dconf/db/<policy_name>
#
#/
import gi
import gettext

gi.require_version("Gvdb", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gvdb
from gi.repository import GLib

import gpr_system
import ast

#  @todo    Add a definition of the system language.
gettext.bindtextdomain("gpr_get_policies", "locales")
gettext.textdomain("gpr_get_policies")
t = gettext.translation("gpr_get_policies", localedir="../locales", languages=['ru_RU'])
t.install()
_ = t.gettext

## @brief   The path to concatenate with uid to 
#           retrieve a specific policy database
PATH_DB = "/etc/dconf/db/policy"

## @brief   Creating a path to user/machine policy.
#  @param   uid User uid.
#  @note	If no uid is specified, the default value 
#           of None will be used. That is, machine 
#           policies located in /etc/dconf/db/policy will be processed.
#  @return  Path to user/machine policies.
def get_path_to_policy(uid=None):
    if uid:
        return PATH_DB + str(uid)
    return PATH_DB

## @brief   Get all policies for a specific user/machine.
#  @param   name User or machine name.
#  @return  All policies for the specified object. 
#           Returned as a dictionary: { “keys”: [...], “values”: [...]}.
def get_policies(name=None, type='standart'):
    uid = None
    policies = None
    if name:
        uid = gpr_system.get_uid_from_name(name)
    path = get_path_to_policy(uid)

    if type == 'standart': # or output the policy name with keys and values ...
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
                applied_policy_with_keys.setdefault(meta['policy_name'], []).append([k, value_of_key_policy])

    return applied_policy_with_keys

## @brief   Get all policies with non-empty keys.
#  @param   path Path to the policy database.
#  @return  Policies for the specified object. 
#           Returned as a dictionary: { “keys”: [...], “values”: [...]}.
def get_non_empty_keys_policies(path):
    policies = get_all_policies(path)
    for k, v in zip(policies['keys'][:], policies['values'][:]):
        if not v:
            policies['keys'].remove(k)
            policies['values'].remove(v)
    return(policies)

## @brief   Get all policies for a specific user/machine.
#  @param   path Path to the policy database.
#  @return  Policies for the specified object. 
#           Returned as a dictionary: { “keys”: [...], “values”: [...]}.
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
