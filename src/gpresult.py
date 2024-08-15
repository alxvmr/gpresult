#! /usr/bin/env python3
import argparse
from gpr_get_policies import get_policies
from gpr_show import show
import socket
import os

import gettext, locale

loc = locale.getlocale()[0]
if loc not in ['ru_RU', 'en_US']:
    loc = 'en_US'

gettext.bindtextdomain("gpresult", "locales")
gettext.textdomain("gpresult")
t = gettext.translation("gpresult", localedir="locales", languages=[loc])
t.install()
_ = t.gettext


def parse_cli_arguments():
    argparser = argparse.ArgumentParser(description=_("Information about applied policies"), formatter_class=argparse.RawTextHelpFormatter)

    argparser.add_argument('-t', '--type',
                           choices=['verbose', 'standard', 'with_keys'],
                           help = _("Output format. Choose one of the following options:\n"\
                                    "* verbose: display of policy keys and values\n"\
                                    "* standard: standard output including environment information; outputs only the names of applied policies\n"\
                                    "* with_keys: is similar to the standard output, in addition, the applied keys and policy values are also output"))
    
    argparser.add_argument('-id', '--id',
                           action='store_true',
                           help=_("Add policy ID output for policies\n"\
                                  "* For the <verbose> output type the option does not apply"))
    
    argparser.add_argument("-polid", "--policy_id",
                           help=_("Information about policy keys and values by ID\n"\
                                  "* For the <with_keys> output type the option does not apply"),
                           type=str)
    
    argparser.add_argument("-poln", "--policy_name",
                           help=_("Information about policy keys and values by name\n"\
                                  "* For the <with_keys> output type the option does not apply"),
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
    name = None
    name_uid = None

    if args.user:
        obj = 'user'
        name = name_uid = os.getlogin()

    else:
        obj = 'machine'
        name = socket.gethostname()

    if args.policy_id or args.policy_name:
        if args.type in ['verbose', 'standard']:
            if args.policy_id:
                policies = get_policies(name=name_uid, type=args.type, with_id=args.id, cmd="id", cmd_name=args.policy_id)
                show(policies, obj, name, args.type, True)
            elif args.policy_name:
                policies = get_policies(name=name_uid, type=args.type, with_id=args.id, cmd="name", cmd_name=args.policy_name)
                show(policies, obj, name, args.type, True)
        else:
            pass # TODO: To infer an invalid output format for this option
    else:
        if args.id and args.type == 'verbose':
            pass # TODO: To infer an invalid output format for this option
        else:
            policies = get_policies(name=name_uid, type=args.type, with_id=args.id)
            show(policies, obj, name, args.type, False)


if __name__ == "__main__":
    main()