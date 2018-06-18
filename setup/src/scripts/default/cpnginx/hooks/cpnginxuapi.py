#!/usr/bin/python -B
"""
copyright(c) cpnginx.com
Hook for rebuilding domain vhosts
"""
import os
import sys
import json
import subprocess

def _decode_list(data):
    pdata = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        pdata.append(item)
    return pdata

def _decode_dict(data):
    pdata = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        pdata[key] = value
    return pdata


def read_in():
    lines = sys.stdin.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
    return lines

def main():
    lines = read_in()
    data=lines[0]
    cpdata = json.loads(data,object_hook=_decode_dict)
    domain=cpdata['data']['args']['domain']
    cmd="/usr/local/cpanel/scripts/nginxctl rebuildvhost "+domain
    result=subprocess.check_output(cmd,shell=True)
    print 1
if __name__ == "__main__":
    main()
