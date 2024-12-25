from . import gpr_system
import ast
from prettytable import PrettyTable
from textwrap import fill

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

COLUMN_WIDTH = None

def add_offset(table_str, offset):
    table_split = table_str.split("\n")

    for i in range(len(table_split)):
        table_split[i] = " " * offset + table_split[i]

    return "\n".join(table_split)


def get_lists_formatted_output(data, offset, is_rec=False):
    mytable = PrettyTable()
    mytable.border = False
    mytable.header = False
    mytable.right_padding_width = 3
    if is_rec:
        mytable.left_padding_width = 0
    
    for j, row in enumerate(data):
        is_last_obj = j == len(data) - 1

        for i in range(len(row)):
            if type(row[i]) == dict:
                if row[i].get("is_list", None):
                    # list to join str output (for KeyValue)

                    #TODO: add to log
                    # This is a quick fix for a problem where 
                    # in the list a string is framed with u0230 
                    # instead of the normal quote character 
                    # (see gpupdate PR #207)
                    try:
                        ast.literal_eval(row[1])
                    except SyntaxError:
                        row[1] = row[1].replace("″", "\'")

                    values_list_cur = ast.literal_eval(row[1])
                    row[1] = "\n".join(values_list_cur)

                    if type(row[2]) is str and row[2] != "-":
                        #TODO: add to log
                        try:
                            ast.literal_eval(row[2])
                        except SyntaxError:
                            row[2] = row[2].replace("″", "\'")

                        values_list_prev = ast.literal_eval(row[2]) # what to be if send None??? - ok
                        row[2] = "\n".join(values_list_prev)


                del row[i]
                break

            elif type(row[i]) == list:
                row[i] = get_lists_formatted_output(row[i], 0, True)
                if not is_last_obj and is_rec:
                    row[i] += "\n"

            elif str(row[i]) == "None":
                row[i] = "-"

            elif type(row[i]) == str and COLUMN_WIDTH:
                row[i] = fill(str(row[i]), COLUMN_WIDTH)

        mytable.add_row(row)

    for field in mytable.field_names:
        mytable.align[field] = "l"

    output = add_offset(mytable.get_string(), offset)

    return output


def get_raw_output(data):
    s = ""

    for i in range(len(data)):
        row = []
        for j in range(len(data[i])):
            data[i][j] = str(data[i][j])
            if data[i][j] == "None":
                data[i][j] = "-"
            row.append(data[i][j])
        s += " ".join(row) + "\n"

    return s[:-1]


def get_list_output(l, offset):
    s = ""
    for e in l:
        s += " " * offset + e + "\n"

    return s[:-1]


def header_gen():
    timest = gpr_system.get_timestamp()
    s = _("\nCreated on {}").format(timest)

    return {"body": s,
            "type": "str"
            }


def rsop_gen(type):
    header = _("The resulting set of policies")

    sys_info = gpr_system.os_conf()

    if type == 'user':
        sys_info.append(gpr_system.get_user_home_dir())

    return {"header": header,
            "body": [{"body": sys_info,
                     "type": "format"
                     }],
            "type": "section"
            }


def policies_gen(gpos, type, is_cmd, previous):
    header = _("Applied Group Policy Objects")
    body = []

    if type == "raw" or (is_cmd and type == "common"):
        render_type = "raw" if type == "raw" else "format"

        if any(gpos):
            kvs = []

            for gpo in gpos:
                kvs.extend(gpo.keys_values)

            kvs.sort(key = lambda x: x.key)

            if previous:
                if type != "raw":
                    for kv in kvs:
                        body.append([
                            kv.key, 
                            kv.value,
                            kv.mod_previous_value,
                        ])
                else:
                    for kv in kvs:
                        body.append([
                            kv.key,
                            kv.mod_previous_value,
                        ])
            else:
                for kv in kvs:
                    body.append([
                        kv.key, 
                        kv.value,
                    ])

        return {
            "body": body,
            "type": render_type,
        }
    
    elif type == "list" or type == "list_raw":
        render_type = "format" if type == "list" else "raw"
        policy_guid = []
        for gpo in gpos:
            policy_guid.append([gpo.name, gpo.guid])

        return {
            "body": policy_guid,
            "type": render_type,
        }

    elif type == "verbose":
        for gpo in gpos:
            info = gpo.get_info_list(with_previous=previous)
            body.append({
                "body": info,
                "type": 'format'})
            
    elif type == "common":
        names_gpos = []
        for gpo in gpos:
            names_gpos.append(gpo.name)

        body.append({
            "body": names_gpos,
            "type": "list",
        })

    return {"header": header,
        "body": body,
        "type": 'subsection'
        }


def settings_gen(gpos, obj_type, output_type='common', is_cmd=False, previous=True):
    global filtering_gpo
    filtering_gpo = gpos

    if output_type == 'raw' or output_type == 'list' or output_type == 'list_raw' or (is_cmd and output_type=='common'):
        return policies_gen(gpos, output_type, is_cmd, previous)
    
    if obj_type:
        filtering_gpo = []
        for gpo in gpos:
            if obj_type == gpo.obj:
                filtering_gpo.append(gpo)
    
    policies = policies_gen(filtering_gpo, output_type, is_cmd, previous)

    if obj_type == "user":
        header = _("USER SETTINGS")
    elif obj_type == "machine":
        header = _("MACHINE SETTINGS")

    return {"header": header,
            "body": [policies],
            "type": "section"
            }


def gen(gpos, obj_type, output_type, is_cmd, previous):
    data = []

    if output_type == "raw" or output_type == 'list' or output_type == 'list_raw' or (is_cmd and output_type=='common'):
        data.extend([
            settings_gen(gpos, obj_type, output_type, is_cmd, previous)
        ])

    elif output_type == "verbose" or output_type == "common":
        if not is_cmd:
            data.extend([
                header_gen(),
                rsop_gen(obj_type),
            ])

        if obj_type:
            set_gen = settings_gen(gpos, obj_type, output_type, is_cmd, previous)

            if is_cmd:
                if len(set_gen["body"]) == 1 and not len(set_gen["body"][0]["body"]):
                    return data

            data.append(set_gen)

        else:
            for t in ['user', 'machine']:
                set_gen = settings_gen(gpos, t, output_type, is_cmd, previous)

                if is_cmd:
                    if len(set_gen["body"]) == 1 and not len(set_gen["body"][0]["body"]):
                        continue

                data.append(set_gen)

    return data


def show_helper(data, offset):
    for i, elem in enumerate(data):
        if elem["type"] == "section":
            print("\n" + offset * " " + elem["header"])
            print(offset * " " + len(elem["header"]) * "-")

            show_helper(elem["body"], offset + 4)
        
        if elem["type"] == 'subsection':
            print(offset * " " + elem["header"])
            print(offset * " " + len(elem["header"]) * "-")

            show_helper(elem["body"], offset + 4)

        if elem["type"] == "format":
            # To have an indentation between formatted lists,
            # but no top and bottom indentation
            if i:
                print("")
            print(get_lists_formatted_output(elem["body"], offset)[:-1])

        if elem["type"] == 'raw':
            print(get_raw_output(elem["body"]))

        if elem["type"] == "str":
            print(elem["body"])

        if elem["type"] == "list":
            print(get_list_output(elem["body"], offset))


def show(gpos, obj_type, output_type="common", is_cmd=False, previous=True, width=None):
    global COLUMN_WIDTH
    COLUMN_WIDTH = width

    data = gen(gpos, obj_type, output_type, is_cmd, previous)
    offset = 0

    show_helper(data, offset)
