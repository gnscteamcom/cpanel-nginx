#!/usr/bin/python -B
"""
copyright(c) cpnginx.com
Hook for fixing apache domlog bug 
"""
import os
import sys
import json
import subprocess


def main():
    print "Running cpnginx  Apache Domlog  Fix Hook "
    cmd="sed -i s/%h/%a/g /var/cpanel/templates/apache2_4/ea4_main.default"
    subprocess.call(cmd,shell=True)
    cmdap="/usr/local/cpanel/scripts/rebuildhttpdconf"
    result=subprocess.check_output(cmdap,shell=True)
    print "Cpnginx post hook completed"

if __name__ == "__main__":
    main()
