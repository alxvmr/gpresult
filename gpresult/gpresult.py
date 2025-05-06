import argparse
from . import gpr_get_policies, gpr_show

import gettext
gettext.bindtextdomain("gpresult", None)
gettext.textdomain ("gpresult")
_ = gettext.gettext

import argparse

class CustomAction(argparse._StoreTrueAction):
    def __call__(self, parser, namespace, values=True, option_string=None):
        self.values = values

        if not 'ordered_args' in namespace:
            setattr(namespace, 'ordered_args', [])

        previous = namespace.ordered_args
        previous.append(self.dest)
        setattr(namespace, 'ordered_args', previous)


def get_selected_option(parser, is_cmd):
    last_opt = None

    try:
        selected_opts = parser.ordered_args
    except AttributeError:
        return last_opt

    if len(selected_opts):
        if not is_cmd and len(set(selected_opts) & {'list', 'raw'}) == 2:
            last_opt = "list_raw"
        else:
            last_opt = selected_opts[-1]

    return last_opt


def validate_width (w):
    if w  and w <= 0:
        return None
    return w


def parse_cli_arguments():
    argparser = argparse.ArgumentParser(description=_("Information about applied policies"), 
                                        formatter_class=argparse.RawTextHelpFormatter)

    argparser.add_argument('-r', '--raw',
                           action=CustomAction,
                           help=_('Output format: display of policy keys, values and previous values'))

    argparser.add_argument('-c', '--common',
                           action=CustomAction,
                           help=_('Output format: common output including environment information; outputs only the names of applied policies'))

    argparser.add_argument('-v', '--verbose',
                           action=CustomAction,
                           help=_('Output format (DEFAULT): is similar to the common output, in addition, the applied keys, policy values  and preferences are also output'))

    argparser.add_argument('-l', '--list',
                           action=CustomAction,
                           help=_('Output format: output of GPO names and their GUIDs\n'\
                                  '* Not applicable with <-i>/<--policy_guid> and <-n>/<--policy_name>'))
    
    argparser.add_argument('-p', '--previous',
                           action='store_true',
                           help=_("Enable information about the previous GPO key value"))

    argparser.add_argument('-w', '--width',
                           help=_('Set column widths for outputting internal tables (keys and values, preferences, ...)\n'\
                                  '* If the specified value is less than or equal to 0, the width of the columns\n'\
                                  '  will be equal to the maximum length of the row\n'\
                                  '* By default, the column width is equal to the length of the maximum row\n'\
                                  '* If the length of the maximum string is less than the specified value, the width will not change'),
                           default=None,
                           type=int)

    argparser.add_argument("-i", "--policy_guid",
                           help=_("Information about policy keys and values by guid\n"\
                                  "* Not applicable with <-l>/<--list>"),
                           type=str)

    argparser.add_argument("-n", "--policy_name",
                           help=_("Information about policy keys and values by name\n"\
                                  "* Not applicable with <-l>/<--list>"),
                           type=str)

    argparser.add_argument('-u', '--user',
                           action='store_true',
                           help=_('Get information about applied policies for the current user'))

    argparser.add_argument('-m', '--machine',
                           action='store_true',
                           help=_('Get information about applied policies for the current machine'))

    return argparser.parse_args()


def main():
    args = parse_cli_arguments()

    output_format = get_selected_option(args, any([args.policy_name, args.policy_guid]))

    if not output_format:
        output_format = "verbose"

    obj = None
    is_cmd = False
    gpos = None
    
    if args.user:
        obj = 'user'

    elif args.machine:
        obj = 'machine'

    if args.policy_guid or args.policy_name:

        if output_format in ['raw', 'common', 'verbose']:
            is_cmd = True

            if args.policy_guid:
                if args.policy_guid[0] != '{' and args.policy_guid[-1] != '}':
                    args.policy_guid = '{' + args.policy_guid + '}'

                gpos = gpr_get_policies.get_policies(obj, 
                                                     cmd="guid", 
                                                     cmd_arg=args.policy_guid)

            elif args.policy_name:
                gpos = gpr_get_policies.get_policies(obj, 
                                                     cmd="name", 
                                                     cmd_arg=args.policy_name)

        else:
            exit() # TODO: To infer an invalid output format for this option

    else:
        gpos = gpr_get_policies.get_policies(obj)

    gpr_show.show(gpos, obj, output_format, is_cmd, previous=args.previous, width=validate_width(args.width))


if __name__ == "__main__":
    main()