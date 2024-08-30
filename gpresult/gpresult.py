import argparse
from . import gpr_get_policies, gpr_show

import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("gpresult", "locales")
gettext.textdomain("gpresult")
t = gettext.translation("gpresult", 
                        localedir="/usr/lib/python3/site-packages/gpresult/locales", 
                        languages=[loc])
t.install()
_ = t.gettext


class CustomAction(argparse._StoreTrueAction):
    def __call__(self, parser, namespace, values=True, option_string=None):
        self.values = values

        if not 'ordered_args' in namespace:
            setattr(namespace, 'ordered_args', [])

        previous = namespace.ordered_args
        previous.append((self.dest, values))
        setattr(namespace, 'ordered_args', previous)


def get_last_selected_option(parser):
    last_opt = None

    try:
        selected_opts = parser.ordered_args
    except AttributeError:
        return last_opt

    if len(selected_opts):
        last_opt = selected_opts[-1][0]

    return last_opt


def parse_cli_arguments():
    argparser = argparse.ArgumentParser(description=_("Information about applied policies"), 
                                        formatter_class=argparse.RawTextHelpFormatter)

    argparser.add_argument('-r', '--raw',
                           action=CustomAction,
                           help=_('Output format: display of policy keys and values'))

    argparser.add_argument('-s', '--standard',
                           action=CustomAction,
                           help=_('Output format: standard output including environment information; outputs only the names of applied policies'))

    argparser.add_argument('-v', '--verbose',
                           action=CustomAction,
                           help=_('Output format: is similar to the standard output, in addition, the applied keys and policy values are also output'))

    argparser.add_argument("-i", "--policy_guid",
                           help=_("Information about policy keys and values by guid"),
                           type=str)

    argparser.add_argument("-n", "--policy_name",
                           help=_("Information about policy keys and values by name"),
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
    output_format = get_last_selected_option(args)

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

        if output_format in ['raw', 'standard', 'verbose']:
            is_cmd = True

            if args.policy_guid:
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

    gpr_show.show(gpos, obj, output_format, is_cmd)


if __name__ == "__main__":
    main()