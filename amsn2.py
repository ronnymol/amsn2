#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import optparse
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
#FIXME
sys.path.insert(0, "./papyon")
import locale
locale.setlocale(locale.LC_ALL, '')

from amsn2.core import aMSNCore, aMSNUserInterfaceManager

if __name__ == '__main__':
    account = None
    passwd = None
    default_front_end = "qt4"

    parser = optparse.OptionParser(usage = "usage: %prog [options] [-- frontend_options]")
    parser.add_option("-a", "--account", dest="account",
                      default=None, help="The account's username to use")
    parser.add_option("-p", "--password", dest="password",
                      default=None, help="The account's password to use")
    parser.add_option("-f", "--front-end", dest="front_end",
                      default=default_front_end,
                      help="The frontend to use (default is %s)"%(default_front_end,))
    parser.add_option("-l", "--list", action="store_true",
                      dest="list_fe",
                      default=False, help="List Available front ends")
    parser.add_option("-d", "--debug-protocol", action="store_true",
                      dest="debug_protocol",
                      default=False, help="Show protocol debug")
    parser.add_option("-D", "--debug-amsn2", action="store_true", dest="debug_amsn2",
                      default=False, help="Show amsn2 debug")
    parser.add_option("-A", "--autologin", action="store_true", dest="auto_login",
                      default=False, help="Auto login with the credentials given")
    (options, args) = parser.parse_args()

    if options.list_fe:
        print "Available front ends are: %s" %(
            ', '.join(aMSNUserInterfaceManager.list_frontends()))
        sys.exit(0)

    amsn = aMSNCore(options, args)

    amsn.run()

