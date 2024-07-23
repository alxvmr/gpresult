##
# @file   gpr_get_policies.py
# @author Maria Alexeeva <alxvmr@altlinux.com>
# @brief  Reading policies (with filtering).
#
# This file provides functions to read policies 
# from the binary file /etc/dconf/db/<policy_name>
#
# @bug     No know bugs.
#/
import gi
import pwd

gi.require_version("Gvdb", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gvdb
from gi.repository import GLib

## @brief   The path to concatenate with uid to 
#           retrieve a specific policy database
PATH_DB = "/etc/dconf/db/policy"

## @brief   Defining uid by username.
#  @param   name User or machine name.
#  @todo    Remove getpwnam from get_uid_from_name.
#  @return	User uid.
def get_uid_from_name(name):
    pw = pwd.getpwnam(name)
    uid = pw.pw_uid
    return uid

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
def get_policies(name=None):
    uid = None
    if name:
        uid = get_uid_from_name(name)
    path = get_path_to_policy(uid)
    policies = get_non_empty_keys_policies(path)
    return policies

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
