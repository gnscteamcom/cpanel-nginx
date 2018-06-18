#!/usr/bin/python -B
"""
copyright(c) cpnginx.com
Hook for rebuilding domain vhosts
"""
import os
import sys
import json
import subprocess
def main():
    cpuser=sys.argv[1]
    cmd="/usr/local/cpanel/scripts/nginxctl rebuilduservhost "+cpuser
    subprocess.call(cmd,shell=True)
if __name__ == "__main__":
    main()

