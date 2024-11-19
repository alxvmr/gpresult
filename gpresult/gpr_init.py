import gi

gi.require_version("Gvdb", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gvdb
from gi.repository import GLib

import ast
from .GPO import GPO
from .KeyValue import KeyValue
from .Preferences.Preference import Preference

import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("gpr_show", "locales")
gettext.textdomain("gpr_show")
t = gettext.translation("gpr_show",
                        localedir="/usr/lib/python3/site-packages/gpresult/locales",
                        languages=[loc])
t.install()
_ = t.gettext

policy_fields = [
    "correct_path",
    "display_name",
    "name",
    "version",
]

preference_fields = [
    "Drives",
    "Environmentvariables",
    "Files",
    "Folders",
    "Inifiles",
    "Networkshares",
    "Shortcuts",
]


def init_gpos(path, obj):
    try:
        is_not_empty, bytes = GLib.file_get_contents(path)
    except GLib.Error as e:
        if e.matches(GLib.file_error_quark(), GLib.FileError.ACCES):
            print(_("Permission denied: {}").format(path))
        elif e.matches(GLib.file_error_quark(), GLib.FileError.NOENT):
            print(_("No such file: {}").format(path))
        else:
            print(e.message)
        exit()

    bytes = GLib.Bytes.new(bytes)

    if (is_not_empty):
        table = Gvdb.Table.new_from_bytes(bytes, True)

        key_list = Gvdb.Table.get_names(table)

        for k in key_list:
            v = Gvdb.Table.get_value(table, k)

            if v != None:
                # Computing policy data
                if (k.find('GpoPriority') != -1):
                    key_split = k.split("/")
                    field = key_split[-1]

                    if field in policy_fields:
                        keys_gpo = {}
                        keys_gpo[field] = (v.get_string() 
                                           if v.get_type().equal(GLib.VariantType.new("s"))
                                           else None)

                        prefix = "/".join(key_split[:-1])

                        for f in policy_fields:
                            if f == field:
                                continue
                            cur_key = prefix + "/" + f
                            cur_value = Gvdb.Table.get_value(table, cur_key)
                            
                            if cur_value.get_type().equal(GLib.VariantType.new("s")):
                                keys_gpo[f] = cur_value.get_string()
                            elif cur_value.get_type().equal(GLib.VariantType.new("i")):
                                keys_gpo[f] = cur_value.get_int32()

                        # TODO: Add deletion of viewed records

                        GPO(obj, **keys_gpo)


def init_keys_values(path, obj):
    try:
        is_not_empty, bytes = GLib.file_get_contents(path)
    except GLib.Error as e:
        if e.matches(GLib.file_error_quark(), GLib.FileError.ACCES):
            print(_("Permission denied: {}").format(path))
        elif e.matches(GLib.file_error_quark(), GLib.FileError.NOENT):
            print(_("No such file: {}").format(path))
        else:
            print(e.message)
        exit()

    bytes = GLib.Bytes.new(bytes)

    if (is_not_empty):
        table = Gvdb.Table.new_from_bytes(bytes, True)

        key_list = Gvdb.Table.get_names(table)

        for k in key_list:
            v = Gvdb.Table.get_value(table, k)

            if (v != None and k[:9].lower() == "/software" 
                and k.find('GpoPriority') == -1):
                # Computing key and value data

                if v.get_type().equal(GLib.VariantType.new("s")):
                    KeyValue(k, v.get_string(), obj)
                elif v.get_type().equal(GLib.VariantType.new("i")):
                    KeyValue(k, v.get_int32(), obj)

                # TODO: Add deletion of viewed records


def init_keys_values_meta(path, obj):
    try:
        is_not_empty, bytes = GLib.file_get_contents(path)
    except GLib.Error as e:
        if e.matches(GLib.file_error_quark(), GLib.FileError.ACCES):
            print(_("Permission denied: {}").format(path))
        elif e.matches(GLib.file_error_quark(), GLib.FileError.NOENT):
            print(_("No such file: {}").format(path))
        else:
            print(e.message)
        exit()

    bytes = GLib.Bytes.new(bytes)

    if (is_not_empty):
        table = Gvdb.Table.new_from_bytes(bytes, True)

        key_list = Gvdb.Table.get_names(table)

        for k in key_list:
            v = Gvdb.Table.get_value(table, k)

            if v != None and k[:7] == "/Source":
                # Computing key and value data

                if v.get_type().equal(GLib.VariantType.new("s")):
                    KeyValue.set_meta_to_key_value(
                        k[7:], obj, **ast.literal_eval(v.get_string())
                        )

                    # TODO: Add deletion of viewed records


def init_preferences(path, obj):
    try:
        is_not_empty, bytes = GLib.file_get_contents(path)
    except GLib.Error as e:
        if e.matches(GLib.file_error_quark(), GLib.FileError.ACCES):
            print(_("Permission denied: {}").format(path))
        elif e.matches(GLib.file_error_quark(), GLib.FileError.NOENT):
            print(_("No such file: {}").format(path))
        else:
            print(e.message)
        exit()

    bytes = GLib.Bytes.new(bytes)

    if (is_not_empty):
        table = Gvdb.Table.new_from_bytes(bytes, True)

        key_list = Gvdb.Table.get_names(table)

        for k in key_list:
            v = Gvdb.Table.get_value(table, k)
            preference_type = k.split("/")[-1]

            if (v != None and preference_type in preference_fields
                and k.find('Preferences') != -1
                and k.find('Previous') == -1):
                # Computing preference data

                if v.get_type().equal(GLib.VariantType.new("s")):
                    preference_list = ast.literal_eval(v.get_string())

                    for pref in preference_list:
                        Preference(obj, preference_type, **pref)


def init_data(path, obj):
    init_gpos(path, obj)
    init_keys_values(path, obj)
    init_keys_values_meta(path, obj)
    init_preferences(path, obj)

    for kv in KeyValue.get_all_keys_values(obj):
        GPO.set_keys_values(kv)

    for gpo_name, prefs in Preference.preferences.items():
        GPO.set_preferences(gpo_name, prefs)

    Preference.clear_preferences()
