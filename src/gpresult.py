##
# @file   gpresult.py
# @author Maria Alexeeva <alxvmr@altlinux.com>
# The main module that performs argument 
# parsing with the string command. It calls the other modules.
#/

import argparse
from gpr_get_policies import get_policies
from gpr_show import formatted_show
import socket

import gettext

gettext.bindtextdomain("gpresult", "/locales")
gettext.textdomain("gpresult")
t = gettext.translation("gpresult", localedir="locales", languages=['ru_RU'])
t.install()
_ = t.gettext

def parse_cli_arguments():
    argparser = argparse.ArgumentParser(description=_("Information about applied policies"))
    argparser.add_argument('-t', '--type',
                           choices=['all'],
                           help = _("Output format"))
    argparser.add_argument('-u', '--user',
                           type=str,
                           help=_('Get information about applied policies for a user'))
    argparser.add_argument('-m', '--machine',
                           action='store_true',
                           help=_('Get information about applied machine policies'))
    
    return argparser.parse_args()

def main():
    args = parse_cli_arguments()
    if args.type == 'all':
        if args.user:
            policies = get_policies(args.user)
            formatted_show(policies, 'user', args.user)
        elif args.machine:
            policies = get_policies()
            formatted_show(policies, 'machine', socket.gethostname())
        

if __name__ == "__main__":
    main()