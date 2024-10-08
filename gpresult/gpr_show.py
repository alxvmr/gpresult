from . import gpr_system
import ast

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


def get_lists_formatted_output(data, offset, is_rec=False, set_offset_pref=False):
    max_n = 0
    output = ""

    for i in range(len(data)):
        l = len(data[i][0])

        if l > max_n:
              max_n = l

    max_n += 3

    for e in data:
        if type(e[-1]) == list:
            output += (
                    " " * offset 
                    + "{:{max_n}s}".format(str(e[0]), max_n=max_n)
                    + get_lists_formatted_output(e[1], offset+max_n+1, is_rec=True)
                    )

        elif ( type(e[-1]) == dict
               and (e[-1].get("is_list", None)
                    or e[-1].get("is_prefs", None)) ):
            if e[-1].get("is_list", None):
                values_list = ast.literal_eval(e[1])
                out = get_list_output(values_list, max_n+offset+1).lstrip()
                out = out if out != "None" else "-"

                if is_rec and data.index(e) == 0:
                    output += " {:{max_n}s} {:s}\n".format(str(e[0]),
                                                          out, max_n=max_n)

                else:
                    output += (
                        " " * offset 
                        + "{:{max_n}s} {:s}\n".format(str(e[0]),
                                                      out, max_n=max_n)
                        )

            elif e[-1].get("is_prefs", None):
                if data.index(e) > 0:
                    set_offset_pref=True
                output += get_lists_formatted_output(e[0],
                                                    offset,
                                                    is_rec=True,
                                                    set_offset_pref=set_offset_pref)
                if data.index(e) != len(data)-1:
                    output += "\n"
        else:
            out = str(e[1])
            if (is_rec and data.index(e) == 0) and not set_offset_pref:
                output += " {:{max_n}s} {:s}\n".format(str(e[0]),
                                                     out if out != "None" else "-",
                                                     max_n=max_n)
            else:
                output += (
                    " " * offset
                    + "{:{max_n}s} {:s}\n".format(str(e[0]),
                                                out if out != "None" else "-",
                                                max_n=max_n)
                    )
    
    return output


def get_raw_output(data):
    s = ""

    for i in range(len(data)):
        s += f"{data[i][0]} {data[i][1]}\n"

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


def policies_gen(gpos, type, is_cmd):
    header = _("Applied Group Policy Objects")
    body = []

    if type == "raw" or (is_cmd and type == "common"):
        render_type = "raw" if type == "raw" else "format"

        if any(gpos):
            kvs = []

            for gpo in gpos:
                kvs.extend(gpo.keys_values)

            kvs.sort(key = lambda x: x.key)

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
            info = gpo.get_info_list()
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


def settings_gen(gpos, obj_type, output_type='common', is_cmd=False):
    global filtering_gpo
    filtering_gpo = gpos

    if output_type == 'raw' or output_type == 'list' or output_type == 'list_raw' or (is_cmd and output_type=='common'):
        return policies_gen(gpos, output_type, is_cmd)
    
    if obj_type:
        filtering_gpo = []
        for gpo in gpos:
            if obj_type == gpo.obj:
                filtering_gpo.append(gpo)
    
    policies = policies_gen(filtering_gpo, output_type, is_cmd)

    if obj_type == "user":
        header = _("USER SETTINGS")
    elif obj_type == "machine":
        header = _("MACHINE SETTINGS")

    return {"header": header,
            "body": [policies],
            "type": "section"
            }


def gen(gpos, obj_type, output_type, is_cmd):
    data = []

    if output_type == "raw" or output_type == 'list' or output_type == 'list_raw' or (is_cmd and output_type=='common'):
        data.extend([
            settings_gen(gpos, obj_type, output_type, is_cmd)
        ])

    elif output_type == "verbose" or output_type == "common":
        if not is_cmd:
            data.extend([
                header_gen(),
                rsop_gen(obj_type),
            ])

        if obj_type:
            set_gen = settings_gen(gpos, obj_type, output_type, is_cmd)

            if is_cmd:
                if len(set_gen["body"]) == 1 and not len(set_gen["body"][0]["body"]):
                    return data

            data.append(set_gen)

        else:
            for t in ['user', 'machine']:
                set_gen = settings_gen(gpos, t, output_type, is_cmd)

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


def show(gpos, obj_type, output_type="common", is_cmd=False):
    data = gen(gpos, obj_type, output_type, is_cmd)
    offset = 0

    show_helper(data, offset)
