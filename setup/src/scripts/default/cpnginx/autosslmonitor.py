#!/usr/bin/python -B
#Copyright(c) Syslint.com
# Autossl monitor for cpnginx as cpanel don't have a hook to do it.  Set it as cron to run every minute
# 0 * * * * /usr/local/cpanel/scripts/cpnginx/autosslmonitor.py  > /dev/null 2>&1 
import os
import sys
import subprocess
import dataparse
import udatafile
import json
from multiprocessing.pool import ThreadPool
import core
import cpanel

def monitor_ssl(domain,ssldata):
    cert="/usr/local/nginx/conf/ssl.cert.d/"+domain+"_cert"
    cmd='/usr/sbin/whmapi1 fetchsslinfo domain='+domain+' --outpu=json'
    cabdata=''
    keydata=str(ssldata[domain]['key'])
    certdata=str(ssldata[domain]['certificate'])
    cabdata=str(ssldata[domain]['cabundle'])
    if not bool(cabdata.strip()) or len(cabdata.strip()) < 175:
        chain=certdata
    else:
        chain=certdata+'\n'+cabdata
    if os.path.exists(cert):
        with open(cert,'r') as cfile:
            certificate=cfile.read()
        if chain == certificate:
            print "SSl Certificate Uptodate for domain .. " + domain
        else:
            print "Updating new ssl certificate for domain  .." + domain
            core.rebuildvhost(domain)
    else:
        print "Installing  new ssl vhost for domain  .." + domain
        core.rebuildvhost(domain)

def monitor():
    ssldata=cpanel.get_all_ssl_certificates()
    userdata=dataparse.get_vhost_data()
    userdata.update(udatafile.get_vhost_data_from_file())
    for dom in userdata:
        if userdata[dom][2] == "addon" or userdata[dom][2] == "parked":
            sdomain=userdata[dom][3]
            if sdomain in ssldata:
                keycrt=ssldata[sdomain]['key']
                cert=ssldata[sdomain]['certificate']
                ca=ssldata[sdomain]['cabundle']
                ssldata[dom]={'key': keycrt,'certificate': cert,'cabundle': ca}
    puser=None
    parallel=ThreadPool(puser)
    for domain in ssldata:
        if bool(domain.strip()):
            parallel.apply_async(monitor_ssl,(domain,ssldata))
    parallel.close()
    parallel.join()

if __name__ == "__main__":
    if  os.geteuid()==0:
        monitor()
    else:
        "Auto  ssl monitor setup as a cron"

