#Copyright(c) Syslint.com
import os
import sys
import json

def get_main_ip():
    ip='127.0.0.1'
    with open('/etc/wwwacct.conf') as sfile:
        lines=sfile.read().splitlines()
    for line in lines:
        data=line.split()
        if data[0] == 'ADDR' and len(data)==2:
            ip=data[1]
    return(ip)

def get_all_ssl_certificates():
    cmd='/usr/sbin/whmapi1 fetch_vhost_ssl_components --outpu=json'
    datas=os.popen(cmd).read()
    result={}
    ssldata={}
    try:
        result=json.loads(datas)
    except Exception as e:
        print((str(e)))
        pass
    if not bool(result['data']):
        print "SSL information unable to find"
    else:
        for item in result['data']['components']:
            ssldata[item['servername']]={'key': item['key'],'certificate': item['certificate'],'cabundle': item['cabundle']}
    return ssldata
