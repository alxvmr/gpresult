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


def get_lists_formatted_output(data, offset, is_rec=False):
    max_n = 0
    output = ""

    for i in range(len(data)):
        l = len(data[i][0])

        if l > max_n:
              max_n = l

    max_n += 3

    # TODO: Remove or redo the check. max_n is always greater than 0
    if max_n > 0:
        for i in range(len(data)):
            if type(data[i][1]) == list:
                output += (
                    " " * offset 
                    + "{:{max_n}s}".format(str(data[i][0]), max_n=max_n) 
                    + get_lists_formatted_output(data[i][1], offset+max_n, is_rec=True)
                    )

            else:
                out = str(data[i][1])

                if (len(data[i]) == 3 
                    and type(data[i][2]) == dict 
                    and data[i][2]["is_list"]):

                    values_list = ast.literal_eval(data[i][1])
                    out = get_list_output(values_list, max_n+offset+1)[:-1].lstrip()
                
                if out == "None":
                    out = "-"

                if is_rec and i == 0:
                    output += "{:{max_n}s} {:s}\n".format(str(data[i][0]),
                                                          out, max_n=max_n)

                else:
                    output += (
                        " " * offset 
                        + "{:{max_n}s} {:s}\n".format(str(data[i][0]), 
                                                      out, max_n=max_n)
                        )
    
    return output


def get_raw_output(data):
    s = ""

    for i in range(len(data)):
        s += f"{data[i][0]} {data[i][1]}\n"

    return s


def get_list_output(l, offset):
    s = ""
    for e in l:
        s += " " * offset + e + "\n"

    return s


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

    if type == "raw" or (is_cmd and type == "standard"):
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
    
    elif type == "verbose":
        for gpo in gpos:
            info = gpo.get_info_list()
            body.append({
                "body": info,
                "type": 'format'})
            
    elif type == "standard":
        names_gpos = []
        for gpo in gpos:
            names_gpos.append(gpo.name)

        body.append({
            "body": names_gpos,
            "type": "list",
        })

    return {"header": header,
        "body": body,
        "type": 'section'
        }


def settings_gen(gpos, obj_type, output_type='standard', is_cmd=False):
    global filtering_gpo
    filtering_gpo = gpos

    if output_type == 'raw' or (is_cmd and output_type=='standard'):
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

    if output_type == "raw" or (is_cmd and output_type=='standard'):
        data.extend([
            settings_gen(gpos, obj_type, output_type, is_cmd)
        ])

    elif output_type == "verbose" or output_type == "standard":
        data.extend([
            header_gen(),
            rsop_gen(obj_type),
        ])
        
        if obj_type:
            data.append(settings_gen(gpos, obj_type, output_type, False))

        else:
            data.append(settings_gen(gpos, 'user', output_type, False))
            data.append(settings_gen(gpos, 'machine', output_type, False))

    return data


def show_helper(data, offset):
    for elem in data:
        if elem["type"] == "section":
            print("\n" + offset * " " + elem["header"])
            print(offset * " " + len(elem["header"]) * "-")

            show_helper(elem["body"], offset + 4)
        
        if elem["type"] == 'subsection':
            print(offset * " " + elem["header"])
            show_helper(elem["body"], offset + 4)
            print("\n")

        if elem["type"] == "format":
            print(get_lists_formatted_output(elem["body"], offset))

        if elem["type"] == 'raw':
            print(get_raw_output(elem["body"]))

        if elem["type"] == "str":
            print(elem["body"] + "\n")

        if elem["type"] == "list":
            print(get_list_output(elem["body"], offset))


def show(gpos, obj_type, output_type="standard", is_cmd=False):
    data = gen(gpos, obj_type, output_type, is_cmd)
    offset = 0

    show_helper(data, offset)
