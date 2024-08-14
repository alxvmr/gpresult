import gpr_system
import ast

import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("gpr_show", "locales")
gettext.textdomain("gpr_show")
t = gettext.translation("gpr_show", localedir="../locales", languages=[loc])
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


def get_verbose_output(data):
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


def rsop_gen(type, name):
    header = _("The resulting set of policies for the ")

    sys_info = gpr_system.os_conf()

    if type == 'user':
        header += _("user {}:").format(name)
        sys_info.append(gpr_system.get_user_home_dir())

    elif type == 'machine':
        header += _("machine {}:").format(name)

    return {"header": header,
            "body": [{"body": sys_info,
                     "type": "format"
                     }],
            "type": "section"
            }


def policies_gen(policies, type):
    header = _("Applied Group Policy Objects")
    body = []

    if type == 'standard':
        policies_name = list(policies.keys())
        body.append({"body": policies_name,
                     "type": 'list'
                    })
        
    elif type == "with_keys":
        for policy_name, value in policies.items():
            body.append({"header": policy_name,
                         "body":[{"body": value,
                                  "type": 'format'
                                }],
                         "type": 'subsection'})
            
    elif type == "verbose":
        body = []
        for value in policies.values():
            for e in value:
                body.append(e)

        body.sort(key = lambda x: x[0])

        return {"body": body, "type": 'verbose'}
            
    return {"header": header,
        "body": body,
        "type": 'section'
        }


def user_settings_gen(policies, output_type='standard'):
    if output_type == 'verbose':
        return policies_gen(policies, output_type)
    
    header = _("USER SETTINGS")
    policies = policies_gen(policies, output_type)

    return {"header": header,
            "body": [policies],
            "type": "section"
            }


def gen(policies, obj_type, name, output_type):
    data = []

    if output_type == "standard" or output_type == "with_keys":
        data.extend([
            header_gen(),
            rsop_gen(obj_type, name),
            user_settings_gen(policies, output_type)
        ])

    elif output_type == "verbose":
        data.extend([
            header_gen(),
            user_settings_gen(policies, output_type)
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

        if elem["type"] == 'verbose':
            print(get_verbose_output(elem["body"]))

        if elem["type"] == "str":
            print(elem["body"] + "\n")

        if elem["type"] == "list":
            print(get_list_output(elem["body"], offset))


def show(policies, obj_type, name, output_type="standard"):
    data = gen(policies, obj_type, name, output_type)
    offset = 0

    show_helper(data, offset)
