#! /usr/bin/env python3
import argparse
from gpr_get_policies import get_policies
from gpr_show import show
import os

import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("gpresult", "locales")
gettext.textdomain("gpresult")
t = gettext.translation("gpresult", localedir="/usr/lib/python3/site-packages/gpresult/locales", languages=[loc])
t.install()
_ = t.gettext


def parse_cli_arguments():
    argparser = argparse.ArgumentParser(description=_("Information about applied policies"), formatter_class=argparse.RawTextHelpFormatter)

    argparser.add_argument('-f', '--format',
                           choices=['raw', 'standard', 'verbose'],
                           help = _("Output format. Choose one of the following options:\n"\
                                    "* raw: display of policy keys and values\n"\
                                    "* standard: standard output including environment information; outputs only the names of applied policies\n"\
                                    "* verbose: is similar to the standard output, in addition, the applied keys and policy values are also output"))

    argparser.add_argument('-i', '--guid',
                           action='store_true',
                           help=_("Add policy guid output for policies\n"\
                                  "* For the <raw> output type the option does not apply"))

    argparser.add_argument("-p", "--policy_guid",
                           help=_("Information about policy keys and values by guid\n"\
                                  "* For the <verbose> output type the option does not apply"),
                           type=str)

    argparser.add_argument("-n", "--policy_name",
                           help=_("Information about policy keys and values by name\n"\
                                  "* For the <verbose> output type the option does not apply"),
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

    obj = None
    is_cmd = False
    policies = []

    user_name = os.getlogin()

    if args.user:
        obj = 'user'

    elif args.machine:
        obj = 'machine'

    if args.policy_guid or args.policy_name:

        if args.format in ['raw', 'standard']:
            is_cmd = True

            if args.policy_guid:
                policies.append(get_policies(name=user_name, type=args.format, with_guid=args.guid, cmd="guid", cmd_name=args.policy_guid))
                policies.append(get_policies(name=None, type=args.format, with_guid=args.guid, cmd="guid", cmd_name=args.policy_guid))

            elif args.policy_name:
                policies.append(get_policies(name=user_name, type=args.format, with_guid=args.guid, cmd="name", cmd_name=args.policy_name))
                policies.append(get_policies(name=None, type=args.format, with_guid=args.guid, cmd="name", cmd_name=args.policy_name))

        else:
            exit() # TODO: To infer an invalid output format for this option

    else:

        if args.guid and args.format == 'raw':
            exit() # TODO: To infer an invalid output format for this option

        else:
            policies.append(get_policies(name=user_name, type=args.format, with_guid=args.guid))
            policies.append(get_policies(name=None, type=args.format, with_guid=args.guid))

    show(policies, obj, args.format, is_cmd)


if __name__ == "__main__":
    main()