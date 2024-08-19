import gpr_system
import ast

import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("gpr_show", "locales")
gettext.textdomain("gpr_show")
t = gettext.translation("gpr_show", localedir="/usr/lib/python3/site-packages/gpresult/locales", languages=[loc])
t.install()
_ = t.gettext


def get_lists_formatted_output(data, offset):
    max_n = 0
    output = ""

    for i in range(len(data)):
        l = len(data[i][0])

        if l > max_n:
              max_n = l

    max_n += 3

    if max_n > 0:
        for i in range(len(data)):
            if len(data[i]) > 2 and type(data[i][2]) == dict and data[i][2]["is_list"]:
                data_list = ast.literal_eval(data[i][1])
                output += " " * offset + "{:{max_n}s} {:s}\n".format(str(data[i][0]), str(data_list[0]), max_n=max_n)

                for i in range (1, len(data_list)):
                    output += " " * offset + "{:{max_n}s} {:s}\n".format(" ", str(data_list[i]), max_n=max_n)

            else:
                output += " " * offset + "{:{max_n}s} {:s}\n".format(str(data[i][0]), str(data[i][1]), max_n=max_n)

    return output[:-1]


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


def policies_gen(policies, type, is_cmd):
    header = _("Applied Group Policy Objects")
    body = []

    if is_cmd:
        if policies[0]:
            for e in policies[0]:
                body.append([e[0], e[1]])

            body.sort(key = lambda x: x[0])

        if type == 'standard':
            return {"body": body, "type": 'format'}
        elif type == 'raw':
            return {"body": body, "type": 'raw'}

    else:
        if type == 'standard':
            if policies[1] and policies[0]:
                policies_name_with_guid = [[pol, policies[1][pol]] for pol in policies[0]]
                body.append({"body": policies_name_with_guid,
                             "type": 'format'
                             })

            else:
                if policies[0]:
                    policies_name = list(policies[0].keys())
                    body.append({"body": policies_name,
                                "type": 'list'
                                })

        elif type == "verbose":
            if policies[1]:
                for policy_name, value in policies[0].items():
                    if policy_name in policies[1].keys():
                        body.append({"header": f"{policy_name} {policies[1][policy_name]}\n",
                                    "body":[{"body": value,
                                            "type": 'format'
                                            }],
                                    "type": 'subsection'})
            elif policies[0]:
                for policy_name, value in policies[0].items():
                    body.append({"header": policy_name,
                                 "body":[{"body": value,
                                          "type": 'format'
                                        }],
                                 "type": 'subsection'})

        elif type == "raw":
            if policies[0]:
                for value in policies[0].values():
                    for e in value:
                        body.append(e)

                body.sort(key = lambda x: x[0])

            return {"body": body, "type": 'raw'}

    return {"header": header,
        "body": body,
        "type": 'section'
        }


def settings_gen(obj_type, policies, output_type='standard', is_cmd=False):
    if is_cmd:
        return policies_gen(policies, output_type, is_cmd)

    if output_type == 'raw':
        return policies_gen(policies, output_type, False)

    if obj_type == "user":
        header = _("USER SETTINGS")
    else:
        header = _("MACHINE SETTINGS")
        
    policies = policies_gen(policies, output_type, False)

    return {"header": header,
            "body": [policies],
            "type": "section"
            }


def gen(policies, obj_type, output_type, is_cmd):
    data = []

    policy_indx = 0 if obj_type == 'user' else 1

    if is_cmd:
        if obj_type:
            data.extend([
                header_gen(),
                settings_gen(obj_type, policies[policy_indx], output_type, is_cmd)
            ])
        else:
            data.extend([
                header_gen(),
                settings_gen('user', policies[0], output_type, is_cmd),
                settings_gen('machine', policies[1], output_type, is_cmd)
            ])

    elif output_type == "standard" or output_type == "verbose":
        if obj_type:
            data.extend([
                header_gen(),
                rsop_gen(obj_type),
                settings_gen(obj_type, policies[policy_indx], output_type, False)
            ])
        else:
            data.extend([
                header_gen(),
                rsop_gen(obj_type),
                settings_gen('user', policies[0], output_type, False),
                settings_gen('machine', policies[1], output_type, False)
            ])

    elif output_type == "raw":
        if obj_type:
            data.extend([
                header_gen(),
                settings_gen(obj_type, policies[policy_indx], output_type, False)
            ])
        else:
            data.extend([
                header_gen(),
                settings_gen('user', policies[0], output_type, False),
                settings_gen('machine', policies[1], output_type, False)
            ])

    return data


def show_helper(data, offset):
    for elem in data:
        if elem["type"] == "section" or elem["type"] == "subsection":
            print("\n" + offset * " " + elem["header"])

            if elem["type"] == "section":
                print(offset * " " + len(elem["header"]) * "-")

            show_helper(elem["body"], offset + 4)

        if elem["type"] == "format":
            print(get_lists_formatted_output(elem["body"], offset))

        if elem["type"] == 'raw':
            print(get_raw_output(elem["body"]))

        if elem["type"] == "str":
            print(elem["body"] + "\n")

        if elem["type"] == "list":
            print(get_list_output(elem["body"], offset))


def show(policies, obj_type, output_type="standard", is_cmd=False):
    data = gen(policies, obj_type, output_type, is_cmd)
    offset = 0

    show_helper(data, offset)
