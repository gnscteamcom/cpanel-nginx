import os
import sys
def get_vhost_data_from_file():
    userdata_file="/etc/userdatadomains"
    if os.path.exists(userdata_file):
        userdata={}
        with open(userdata_file, 'r') as ufile:
            lines=ufile.read().splitlines()
        for line in lines:
            domd=line.split(' ')
            doms=domd[0].split(':')
            domain=doms[0]
            ds=domd[1].split('=')
            domainuser=ds[0]
            domaintype=ds[4]
            domainreal=ds[6]
            domaindocroot=ds[8]
            domainip=ds[10].split(':')[0].strip()
            userdata[domain]=[domain,domainuser,domaintype,domainreal,domaindocroot,domainip]
    else:
        userdata={}
    return userdata
