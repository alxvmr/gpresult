##
# @file   gpr_show.py
# @author Maria Alexeeva <alxvmr@altlinux.com>
# @brief  Output format of applied policies.
# 
# Module for displaying the result of
# a readout (from the prt_get_policies.py module)
#/
import gettext
import gpr_system

#  @todo    Add a definition of the system language.
gettext.bindtextdomain("gpr_show", "../locales")
gettext.textdomain("gpr_show")
t = gettext.translation("gpr_show", localedir="../locales", languages=['ru_RU'])
t.install()
_ = t.gettext


def dict_to_formatted_output(data, offset):
    max_n = 0
    max_v = 0
    output = ""

    for n, v in data.items():
        if n:
          l = len(n)
          if l > max_n:
              max_n = l
        if v:
            l = len(str(v))
            if l > max_v:
                max_v = l
    max_n += 3

    if max_n > 0 and max_v > 0:
        for n, v in data.items():
            output += " " * offset + "{:{max_n}s} {:{max_v}s}\n".format(str(n), str(v), max_n=max_n, max_v=max_v)

    return output


def header_gen():
    timest = gpr_system.get_timestamp()
    s = _("\nCreated on {}").format(timest)
    return {"body": s,
            "type": "str"
            }


def rsop_gen(type, name):
    header = _("The resulting set of policies for the ")
    if type == 'user':
        header += _("user {}:").format(name)
    elif type == 'machine':
        header += _("machine {}:").format(name)

    sys_info = gpr_system.os_conf()
    sys_info.update(gpr_system.get_user_home_dir())

    return {"header": header,
            "body": [{"body": sys_info,
                     "type": "format"
                     }],
            "type": "section"
            }


def user_settings_gen():
    header = _("USER SETTINGS")

    return {"header": header,
            "body": [],
            "type": "section"
            }


def gen(obj_type, name, output_type):
    data = []
    if output_type == "standart":
        data.extend([
            header_gen(),
            rsop_gen(obj_type, name),
            user_settings_gen()
        ])
    return data


def show_helper(data, offset):
    for elem in data:
        if elem["type"] == "section":
            # отрисовка заголовка секции
            print("\n" + offset * " " + elem["header"])
            print(offset * " " + len(elem["header"]) * "-" + "\n")
            show_helper(elem["body"], offset + 4)
        if elem["type"] == "format":
            print(dict_to_formatted_output(elem["body"], offset))
        if elem["type"] == "str":
            print(elem["body"] + "\n")


def show(obj_type, name, output_type="standart"):
    data = gen(obj_type, name, output_type)
    offset = 0
    show_helper(data, offset)
    


## @brief   Formatted output as a table.
#  @note    The output contains 2 columns - 
#           the policy key and the value. 
#           The output width is the length of 
#           the longest line + 3 empty characters 
#           for each of the columns:
#  @include formatted_show.txt
#  @param   policies A dictionary of lists containing policy keys and values.
#  @param   type Object type is machine or user.
#  @param   name Object Name.
#  @return  Formatted printing of the policies.
def formatted_show(policies, type, name):
    keys = policies['keys']
    values = policies['values']
    output = header_gen()

    max_n = 0
    max_v = 0
    for n, v in zip(keys, values):
        if n:
          l = len(n)
          if l > max_n:
              max_n = l
        if v:
            l = len(str(v))
            if l > max_v:
                max_v = l
    max_n += 3
    
    if max_n > 0 and max_v > 0:
        output += "{:^{max_n}s} {:^{max_v}s}\n".format(_("Policy keys:"), _("Values of policy keys:"), max_n=max_n, max_v=max_v)
        for n, v in zip(keys, values):
            output += "{:{max_n}s} {:{max_v}s}\n".format(str(n), str(v), max_n=max_n, max_v=max_v)
    
    print(output)

## @brief   Output without formatting.
#  @note    The output format is space-separated elements. 
#           This solution is provided for comfortable use
#           of the grep command.
#           Example output:
#  @include verbose_show.txt
#  @param   policies A dictionary of lists containing policy keys and values.
#  @return  Printing of the policies.
def verbose_show(policies):
    keys = policies['keys']
    values = policies['values']
    output = ""

    for n, v in zip(keys, values):
        output += "{} {}\n".format(str(n), str(v))
    print(output)