import json
import os
def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def readjson(datafile):
    with open(datafile,'r') as data_file:
        try:
            data = json.load(data_file,object_hook=_decode_dict)
        except ValueError, e:
            data={}
    return data

def readjsonval(datafile,field):
    with open(datafile,'r') as data_file:
        try:
            data = json.load(data_file,object_hook=_decode_dict)
        except ValueError, e:
            data={}
    return data.get(field)
"""
def readjson_example(file):
    with open(file,'r') as data_file:    
        data = json.load(data_file,object_hook=_decode_dict)
    default_apache_https_port = data.get('default_apache_https_port')
    print default_apache_https_port
    if "9443"  in default_apache_https_port:
        print "success"
"""
def get_ssl_domains_local():
    with open('/etc/ssldomains') as sfile:
        lines=sfile.read().splitlines()
    ssldom={}
    for line in lines:
        x=line.split(":")
        domain=x[0]
        ip=x[1].strip()
        ssldom[domain] =[domain,ip]
    return ssldom
def get_vhost_data():
    userdata_file="/etc/userdatadomains.json"
    if os.path.exists(userdata_file):
        userdata_json=readjson(userdata_file)
        ssldomains=get_ssl_domains_local()
        userdata={}
        for domain in userdata_json:
            domainuser=userdata_json[domain][0].strip()
            dopmaintype=userdata_json[domain][2].strip()
            domainreal=userdata_json[domain][3].strip()
            domaindocroot=userdata_json[domain][4].strip()
            domainip=userdata_json[domain][5].split(':')[0].strip()
            #print domain,domainuser,dopmaintype,domainreal,domaindocroot,domainip 
            userdata[domain]=[domain,domainuser,dopmaintype,domainreal,domaindocroot,domainip]
    else:
        userdata={}
    return userdata 
def writejson(db,filename):
    with open(filename, 'w') as fp:
        json.dump(db,fp)















