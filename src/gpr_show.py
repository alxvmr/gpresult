##
# @file   gpr_show.py
# @author Maria Alexeeva <alxvmr@altlinux.com>
# @brief  Output format of applied policies.
# 
# Module for displaying the result of
# a readout (from the prt_get_policies.py module)
#/
import gettext

#  @todo    Add a definition of the system language.
gettext.bindtextdomain("gpr_show", "../locales")
gettext.textdomain("gpr_show")
t = gettext.translation("gpr_show", localedir="../locales", languages=['ru_RU'])
t.install()
_ = t.gettext


## @brief   Composing an output header.
#  @param   type Object type is machine or user.
#  @param   name Object Name.
#  @todo    Add an output type to the header (no empty keys, etc.)
#  @return  Header for displaying the list of applied policies.
def header_gen(type, name):
    s = _("\nA list of applied policies for the ")
    if type == 'user':
        s += _("user {}:\n\n").format(name)
    elif type == 'machine':
        s += _("machine {}:\n\n").format(name)
    return s

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
    output = header_gen(type, name)

    max_n = -1
    max_v = -1
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

    for n, v in zip(keys, values):
        output += "{:{max_n}s} {:{max_v}s}\n".format(str(n), str(v), max_n=max_n, max_v=max_v)
    
    print(output)