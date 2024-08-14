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
t = gettext.translation("gpresult", localedir="../locales", languages=[loc])
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
    
    argparser.add_argument('-u', '--user',
                           action='store_true',
                           help=_('Get information about applied policies for the current user'))
    
    argparser.add_argument('-m', '--machine',
                           action='store_true',
                           help=_('Get information about applied policies for the current machine'))
    
    return argparser.parse_args()

def main():
    args = parse_cli_arguments()

    if args.user:
        obj = 'user'
        name = os.getlogin()
        policies = get_policies(name=name, type=args.type)

    else:
        obj = 'machine'
        name = socket.gethostname()
        policies = get_policies(type=args.type)
    
    show(policies, obj, name, args.type)


if __name__ == "__main__":
    main()