from mako.template import Template
import os,sys
import dataparse
import udatafile
import subprocess
from shellcolor import shellcolor
import conf
import phpfpm
import udatafile
import re
import cpanel
import json

def is_wildcard_domains(domain):
    if re.match('\*\.',domain):
        return True
    else:
        return False
def get_apache_port_http():
    dfile="/etc/cpnginx/data/settings.json"
    http_port=dataparse.readjsonval(dfile,"APACHE_HTTP_PORT")[0]
    return http_port
def get_apache_port_https():
    dfile="/etc/cpnginx/data/settings.json"
    https_port=dataparse.readjsonval(dfile,"APACHE_HTTPS_PORT")[0]
    return https_port
def get_default_settings():
    sfile="/etc/cpnginx/data/settings.json"
    settings=dataparse.readjson(sfile)
    return settings
def get_firewall():
    ffile="/etc/cpnginx/data/firewall.json"
    fdata=dataparse.readjson(ffile)
    return fdata
def get_template_path(template):
    tdata_file="/etc/cpnginx/data/templates.json"
    tdata=dataparse.readjson(tdata_file)
    if tdata.get(template) != None:
        tfiledata=tdata[template]
        path=tfiledata[2]
        conf=tfiledata[0]
    else:
        path="vhost"
        conf="proxy"
    t_file_path="/etc/cpnginx/templates/"+path+"/"+conf+".conf"
    t_file_custom="/etc/cpnginx/templates/custom/"+conf+".conf"
    if os.path.exists(t_file_custom):
        tpath=t_file_custom
    elif os.path.exists(t_file_path):
        tpath=t_file_path
    else:
        tpath="/etc/cpnginx/templates/vhost/proxy.conf"
    return tpath

def add_fpm_user(user,fpm):
    fpmdb=dataparse.readjson("/etc/cpnginx/data/fpm.json")
    path="/opt/cpanel/ea-php56/root/etc/php-fpm.d"
    if not  len(fpmdb.keys()) == 0:
        if fpm in fpmdb:
            path=fpmdb[fpm][5]
    else:
        path="/opt/cpanel/ea-php56/root/etc/php-fpm.d"
    conf=path+"/"+user+".conf"
    custom="/etc/cpnginx/templates/custom/fpm/fpm.conf"
    real="/etc/cpnginx/templates/fpm/fpm.conf"
    if os.path.exists(custom):
        template=custom
    else:
        template=real
    if not os.path.exists(conf):
        fpmtemplate  = Template(filename=template)
        data={}
        data['USER']=user
        fpmconf=fpmtemplate.render(**data)
        with open(conf,'w') as cfw:
            cfw.write(fpmconf)
        phpfpm.reloadfpm(fpm)
    socpath={}
    socpath['FPM_SOCK']="/opt/cpanel/ea-"+fpm+"/root/usr/var/run/php-fpm/"+user+".sock"
    return socpath

def have_valid_ssl(domain):
    cmd='/usr/sbin/whmapi1 fetchsslinfo domain='+domain+' --outpu=json'
    datas=os.popen(cmd).read()
    result={}
    try:
        result=json.loads(datas)
    except Exception as e:
        print((str(e)))
        pass
    if not bool(result['data']):
        return False
    else:
        keydata=str(result['data']['key'])
        certdata=str(result['data']['crt'])
        if len(keydata) < 100 or len(certdata) < 100:
            # Either key file or certificate is missing
            return False
        else:
            # both key file and certificate are present
            return True

def get_ssl_domains():
    alluserdata=dataparse.get_vhost_data()
    alluserdata.update(udatafile.get_vhost_data_from_file())
    ssldom={}
    for domain in alluserdata:
        if alluserdata[domain][2] == "sub":
            domconf='/var/cpanel/userdata/'+alluserdata[domain][1]+'/'+alluserdata[domain][0]+'_SSL'
            if os.path.exists(domconf):
                ssldom[domain]=[alluserdata[domain][0],alluserdata[domain][5]]
        else:
            domconf='/var/cpanel/userdata/'+alluserdata[domain][1]+'/'+alluserdata[domain][3]+'_SSL'
            if os.path.exists(domconf):
                ssldom[domain]=[alluserdata[domain][3],alluserdata[domain][5]]
    return ssldom



def get_user_domains(cpuser):
    alluserdata=dataparse.get_vhost_data()
    alluserdata.update(udatafile.get_vhost_data_from_file())
    cpuserdata={}
    for domain in alluserdata:
        if alluserdata[domain][1]==cpuser:
            cpuserdata[domain]=alluserdata[domain]
    return cpuserdata
def get_dedicated_ip_domains():
    with open('/etc/domainips','r') as dom:
        linesa=dom.read().splitlines()
    lines=filter(None, linesa)
    data={}
    for line in lines:
        if not line.startswith('#'):
            linesplit=line.split(':')
            domain=linesplit[1].strip()
            ip=linesplit[0].strip()
            data[domain]=[domain,ip]
    return data

                                                                                                                                                                                                                                        
def build_ssl_cert(domain,ssldata):                                                                                                                                                                                                  
    userdata=dataparse.get_vhost_data()                                                                                                                                                                                                 
    cert="/usr/local/nginx/conf/ssl.cert.d/"+domain+"_cert"                                                                                                                                                                             
    key="/usr/local/nginx/conf/ssl.key.d/"+domain+"_key"                                                                                                                                                                                
    cab="/usr/local/nginx/conf/ssl.ca.d/"+domain+"_ca-bundle"                                                                                                                                                                           
    if os.path.exists(cert):                                                                                                                                                                                                            
        if os.path.islink(cert):                                                                                                                                                                                                        
            os.unlink(cert)                                                                                                                                                                                                             
        else:                                                                                                                                                                                                                           
            os.remove(cert)                                                                                                                                                                                                             
    if os.path.exists(key):                                                                                                                                                                                                             
        if os.path.islink(key):                                                                                                                                                                                                         
            os.unlink(key)                                                                                                                                                                                                              
        else:                                                                                                                                                                                                                           
            os.remove(key)                                                                                                                                                                                                              
    if os.path.exists(cab):                                                                                                                                                                                                             
        if os.path.islink(cab):                                                                                                                                                                                                         
            os.unlink(cab)                                                                                                                                                                                                              
        else:                                                                                                                                                                                                                           
            os.remove(cab)                                                                                                                                                                                                              
    cabdata=''
    keydata=str(ssldata[domain]['key'])
    certdata=str(ssldata[domain]['certificate'])
    cabdata=str(ssldata[domain]['cabundle'])
    if not bool(cabdata.strip()) or len(cabdata.strip()) < 175:
        chain=certdata
    else:
        chain=certdata+'\n'+cabdata
    if bool(cabdata.strip()) and len(cabdata.strip()) > 175:
        print "Creating CA-Bundle For "+domain+" .. "+shellcolor.pink+"/usr/local/nginx/conf/ssl.ca.d/"+domain+"_ca-bundle"+shellcolor.end
        with open(cab,'w') as writecab:
            writecab.write(cabdata)
    print "Creating CERT File  For "+domain+" .. "+shellcolor.pink+"/usr/local/nginx/conf/ssl.cert.d/"+domain+"_cert"+shellcolor.end
    with open(cert,'w') as writecert:
        writecert.write(chain)
    print "Creating KEY File  For "+domain+" .. "+shellcolor.pink+"/usr/local/nginx/conf/ssl.key.d/"+domain+"_key"+shellcolor.end
    with open(key,'w') as writekey:
        writekey.write(keydata)


def build_all_ssl_certs():
    userdata=dataparse.get_vhost_data()
    userdata.update(udatafile.get_vhost_data_from_file())
    ssldata=cpanel.get_all_ssl_certificates()
    for dom in userdata:
        if userdata[dom][2] == "addon" or userdata[dom][2] == "parked":
            sdomain=userdata[dom][3]
            if sdomain in ssldata:
                keycrt=ssldata[sdomain]['key']
                cert=ssldata[sdomain]['certificate']
                ca=ssldata[sdomain]['cabundle']
                ssldata[dom]={'key': keycrt,'certificate': cert,'cabundle': ca}
    for domain in ssldata:
        build_ssl_cert(domain,ssldata)
def get_user_home(cpuser):
    with open('/etc/passwd', 'r') as passwd:
        lines=passwd.read().splitlines()
    for line in lines:
        l=line.split(":")
        if l[0] == cpuser:
            home=l[5]
            return home

def get_web_server_app_templates():
    tmpdb="/etc/cpnginx/data/templates.json"
    tmpdata=dataparse.readjson(tmpdb)
    return tmpdata
def get_vhost_local_data(domain,user,settings,firewall):
    userhome=get_user_home(user)
    localfile=userhome+"/.cpnginx/"+domain+".json"
    finallocaldata={}
    if os.path.exists(localfile) and  os.path.islink(localfile) == False:
        localdata=dataparse.readjson(localfile)
        if not  len(localdata.keys()) == 0:
            try:   
                if localdata.get('HOT_LINK_PROTECTION') != None and settings['HOT_LINK_PROTECTION'][0] == "1":
                    if (localdata.get('HOT_LINK_PROTECTION')[0] == "0"  or localdata.get('HOT_LINK_PROTECTION')[0] == "1") and localdata.get('HOT_LINK_PROTECTION')[0] != None:
                        finallocaldata['HOT_LINK_PROTECTION'] = localdata.get('HOT_LINK_PROTECTION')
                if localdata.get('PROXY_CACHE') != None and settings['PROXY_CACHE'][0] == "1":
                    if (localdata.get('PROXY_CACHE')[0] == "0"  or localdata.get('PROXY_CACHE')[0] == "1") and localdata.get('PROXY_CACHE')[0] != None:
                        finallocaldata['PROXY_CACHE'] = localdata.get('PROXY_CACHE')
                if localdata.get('MOD_MP4') != None and settings['MOD_MP4'][0] == "1":
                    if (localdata.get('MOD_MP4')[0] == "0"  or localdata.get('MOD_MP4')[0] == "1") and localdata.get('MOD_MP4')[0] != None:
                        finallocaldata['MOD_MP4'] = localdata.get('MOD_MP4')
                if localdata.get('WWW_REDIRECTION') != None:
                    if (localdata.get('WWW_REDIRECTION')[0] == "wwwtonon"  or localdata.get('WWW_REDIRECTION')[0] == "nontowww" or localdata.get('WWW_REDIRECTION')[0] == "none") and localdata.get('WWW_REDIRECTION')[0] != None:
                        finallocaldata['WWW_REDIRECTION'] = localdata.get('WWW_REDIRECTION')
                if localdata.get('HTTPS_REDIRECTION') != None:
                    if (localdata.get('HTTPS_REDIRECTION')[0] == "0"  or localdata.get('HTTPS_REDIRECTION')[0] == "1") and localdata.get('HTTPS_REDIRECTION')[0] != None:
                        finallocaldata['HTTPS_REDIRECTION'] = localdata.get('HTTPS_REDIRECTION')
                if localdata.get('MOD_FLV') != None and settings['MOD_FLV'][0] == "1":
                    if (localdata.get('MOD_FLV')[0] == "0"  or localdata.get('MOD_FLV')[0] == "1") and localdata.get('MOD_FLV')[0] != None:
                        finallocaldata['MOD_FLV'] = localdata.get('MOD_FLV')
                if localdata.get('FASTCGI_CACHE') != None and settings['FASTCGI_CACHE'][0] == "1":
                    if (localdata.get('FASTCGI_CACHE')[0] == "0"  or localdata.get('FASTCGI_CACHE')[0] == "1") and localdata.get('FASTCGI_CACHE')[0] != None:
                        finallocaldata['FASTCGI_CACHE'] = localdata.get('FASTCGI_CACHE')
                if localdata.get('DIRECTORY_LIST') != None and settings['DIRECTORY_LIST'][0] == "1":
                    if (localdata.get('DIRECTORY_LIST')[0] == "0"  or localdata.get('DIRECTORY_LIST')[0] == "1") and localdata.get('DIRECTORY_LIST')[0] != None:
                        finallocaldata['DIRECTORY_LIST'] = localdata.get('DIRECTORY_LIST')
                if localdata.get('RANGE_PROTECTION') != None and firewall['RANGE_PROTECTION'][0] == "1":
                    if (localdata.get('RANGE_PROTECTION')[0] == "0"  or localdata.get('RANGE_PROTECTION')[0] == "1") and localdata.get('RANGE_PROTECTION')[0] != None:
                        finallocaldata['RANGE_PROTECTION'] = localdata.get('RANGE_PROTECTION')
                if localdata.get('HTTP_METHOD_ENABLE') != None and firewall['HTTP_METHOD_ENABLE'][0] == "1":
                    if (localdata.get('HTTP_METHOD_ENABLE')[0] == "0"  or localdata.get('HTTP_METHOD_ENABLE')[0] == "1") and localdata.get('HTTP_METHOD_ENABLE')[0] != None:
                        finallocaldata['HTTP_METHOD_ENABLE'] = localdata.get('HTTP_METHOD_ENABLE')
                if localdata.get('USER_AGENT_ATTACK_PROTECTION') != None and firewall['USER_AGENT_ATTACK_PROTECTION'][0] == "1":
                    if (localdata.get('USER_AGENT_ATTACK_PROTECTION')[0] == "0"  or localdata.get('USER_AGENT_ATTACK_PROTECTION')[0] == "1") and localdata.get('USER_AGENT_ATTACK_PROTECTION')[0] != None:
                        finallocaldata['USER_AGENT_ATTACK_PROTECTION'] = localdata.get('USER_AGENT_ATTACK_PROTECTION')
                if localdata.get('REFERRER_SPAM_PROTECHTION') != None and firewall['REFERRER_SPAM_PROTECHTION'][0] == "1":
                    if (localdata.get('REFERRER_SPAM_PROTECHTION')[0] == "0"  or localdata.get('REFERRER_SPAM_PROTECHTION')[0] == "1") and localdata.get('REFERRER_SPAM_PROTECHTION')[0] != None:
                        finallocaldata['REFERRER_SPAM_PROTECHTION'] = localdata.get('REFERRER_SPAM_PROTECHTION')
                if localdata.get('SCANNER_ATTACK_PROTECTION') != None and firewall['SCANNER_ATTACK_PROTECTION'][0] == "1":
                    if (localdata.get('SCANNER_ATTACK_PROTECTION')[0] == "0"  or localdata.get('SCANNER_ATTACK_PROTECTION')[0] == "1") and localdata.get('SCANNER_ATTACK_PROTECTION')[0] != None:
                        finallocaldata['SCANNER_ATTACK_PROTECTION'] = localdata.get('SCANNER_ATTACK_PROTECTION')
                if localdata.get('XSS_PROTECTION') != None and firewall['XSS_PROTECTION'][0] == "1":
                    if (localdata.get('XSS_PROTECTION')[0] == "0"  or localdata.get('XSS_PROTECTION')[0] == "1") and localdata.get('XSS_PROTECTION')[0] != None:
                        finallocaldata['XSS_PROTECTION'] = localdata.get('XSS_PROTECTION')
                if localdata.get('XFRAME_ATTACK_PROTECTION') != None and firewall['XFRAME_ATTACK_PROTECTION'][0] == "1":
                    if (localdata.get('XFRAME_ATTACK_PROTECTION')[0] == "0"  or localdata.get('XFRAME_ATTACK_PROTECTION')[0] == "1") and localdata.get('XFRAME_ATTACK_PROTECTION')[0] != None:
                        finallocaldata['XFRAME_ATTACK_PROTECTION'] = localdata.get('XFRAME_ATTACK_PROTECTION')
                if localdata.get('PROTECT_SQL_INJECTION') != None and firewall['PROTECT_SQL_INJECTION'][0] == "1":
                    if (localdata.get('PROTECT_SQL_INJECTION')[0] == "0"  or localdata.get('PROTECT_SQL_INJECTION')[0] == "1") and localdata.get('PROTECT_SQL_INJECTION')[0] != None:
                        finallocaldata['PROTECT_SQL_INJECTION'] = localdata.get('PROTECT_SQL_INJECTION')
                if localdata.get('PROTECT_FILE_INJECT') != None and firewall['PROTECT_FILE_INJECT'][0] == "1":
                    if (localdata.get('PROTECT_FILE_INJECT')[0] == "0"  or localdata.get('PROTECT_FILE_INJECT')[0] == "1") and localdata.get('PROTECT_FILE_INJECT')[0] != None:
                        finallocaldata['PROTECT_FILE_INJECT'] = localdata.get('PROTECT_FILE_INJECT')
                if localdata.get('PROTECT_COMMON_EXPLOITS') != None and firewall['PROTECT_COMMON_EXPLOITS'][0] == "1":
                    if (localdata.get('PROTECT_COMMON_EXPLOITS')[0] == "0"  or localdata.get('PROTECT_COMMON_EXPLOITS')[0] == "1") and localdata.get('PROTECT_COMMON_EXPLOITS')[0] != None:
                        finallocaldata['PROTECT_COMMON_EXPLOITS'] = localdata.get('PROTECT_COMMON_EXPLOITS')
                if localdata.get('SYMLINK_ATTACK') != None and firewall['SYMLINK_ATTACK'][0] == "on":
                    if (localdata.get('SYMLINK_ATTACK')[0] == "on"  or localdata.get('SYMLINK_ATTACK')[0] == "off") and localdata.get('SYMLINK_ATTACK')[0] != None:
                        finallocaldata['SYMLINK_ATTACK'] = localdata.get('SYMLINK_ATTACK')
                if localdata.get('GOOGLE_PAGE_SPEED') != None and settings['GOOGLE_PAGE_SPEED'][0] == "1":
                    if (localdata.get('GOOGLE_PAGE_SPEED')[0] == "0"  or localdata.get('GOOGLE_PAGE_SPEED')[0] == "1") and localdata.get('GOOGLE_PAGE_SPEED')[0] != None:
                        finallocaldata['GOOGLE_PAGE_SPEED'] = localdata.get('GOOGLE_PAGE_SPEED')
                if localdata.get('PHP_FPM') != None:
                    if  (localdata.get('PHP_FPM')[0] in conf.cpphpfpm_rpms) and localdata.get('PHP_FPM')[0] != None:
                        finallocaldata['PHP_FPM'] = localdata.get('PHP_FPM')
                if localdata.get('WEB_SERVER') != None:
                    tname=localdata.get('WEB_SERVER')[0]
                    allwebtemp=get_web_server_app_templates()
                    if allwebtemp.get(tname) != None:
                        finallocaldata['WEB_SERVER'] = localdata.get('WEB_SERVER')
            except (IndexError,ValueError, NameError) as e:
                pass
        else:
            finallocaldata={}
    return finallocaldata

def get_vhost_global_data(domain,user):
    globalfile="/etc/cpnginx/domains/"+domain+".json"
    if os.path.exists(globalfile):
        globaldata=dataparse.readjson(globalfile)
    else:
        globaldata={}
    return globaldata

# Remove this function after test
def test_data(domain,user):
    default_settings=get_default_settings()
    default_firewall=get_firewall()
    globaldata=get_vhost_global_data(domain,user)
    localdata=get_vhost_local_data(domain,user)
    print "-----defaultt "
    print default_settings
    print "------firewall "
    print default_firewall
    print "---------globaldata---"
    print globaldata
    print "--localdata--"
    print localdata
    com=default_settings.copy()
    com.update(default_firewall)
    com.update(globaldata)
    com.update(localdata)
    print "---final--"
    print com

def build_defaul_vhost():
    domain_data={}
    domain_data['APACHE_HTTP_PORT']=get_apache_port_http()
    domain_data['APACHE_HTTPS_PORT']=get_apache_port_https()
    domain_data['MAIN_IP']=cpanel.get_main_ip()
    template="/etc/cpnginx/templates/vhost/default.conf"
    if os.path.exists("/var/cpanel/ssl/cpanel/mycpanel.pem"):
        shared_ssl="mycpanel.pem"
    else:
        shared_ssl="cpanel.pem"
    domain_data['CPSSL']=shared_ssl
    httptemplate = Template(filename=template)
    confpath_ssl="/usr/local/nginx/conf/conf.d/000_default.conf"
    vhostdata_ssl=httptemplate.render(**domain_data)
    fo=open(confpath_ssl,"wb")
    fo.write(vhostdata_ssl)
    fo.close()
    print "Generating CPANEL DEFAULT  configuration file .. "+shellcolor.green+confpath_ssl+shellcolor.end


def build_vhost(userdata,havessl,havedip,firewall,settings,ssldata):
    domain=userdata[0]
    user=userdata[1]
    default_settings=settings
    #default_settings=get_default_settings()
    #default_firewall=get_firewall()
    default_firewall=firewall
    globaldata=get_vhost_global_data(domain,user)
    localdata=get_vhost_local_data(domain,user,default_settings,default_firewall)
    final=default_settings.copy()
    final.update(default_firewall)
    final.update(globaldata)
    final.update(localdata)
    if os.path.exists("/var/cpanel/suspended/"+userdata[1]):
        template="/etc/cpnginx/templates/vhost/suspended.conf"
    elif  is_wildcard_domains(domain):
        template="/etc/cpnginx/templates/vhost/wildcard.conf"      
    else:
        template=get_template_path(final['WEB_SERVER'][0].strip())
    httptemplate = Template(filename=template)
    domain_data={}
    for ver in final:
        domain_data[ver]=final[ver][0]
    domain_data['DOMAIN']=userdata[0]
    domain_data['USER']=userdata[1]
    domain_data['TYPE']=userdata[2]
    domain_data['PARENT_DOMAIN']=userdata[3]
    domain_data['DOCROOT']=userdata[4]
    domain_data['IP']=userdata[5]
    domain_data['HAVESSL']=havessl
    domain_data['APACHE_HTTP_PORT']=get_apache_port_http()
    domain_data['APACHE_HTTPS_PORT']=get_apache_port_https()
    domain_data['HAVE_DEDICATED_IP']=havedip
    if havessl== "1":
	if userdata[2] == "sub":
            domconf='/var/cpanel/userdata/'+userdata[1]+'/'+userdata[0]+'_SSL'
	elif userdata[2] == "addon" or userdata[2] == "parked":
            domconf='/var/cpanel/userdata/'+userdata[1]+'/'+userdata[3]+'_SSL'
	else:
            domconf='/var/cpanel/userdata/'+userdata[1]+'/'+userdata[0]+'_SSL'
        if os.path.exists(domconf):
            build_ssl_cert(userdata[0],ssldata)
            if os.path.exists("/usr/local/nginx/conf/ssl.ca.d/"+userdata[0]+"_ca-bundle"):
                domain_data['OSCP']="1"
            else:
                domain_data['OSCP']="0"
            include="/usr/local/nginx/conf/vhost.ssl.d/"+userdata[0]+".include"
            if os.path.exists(include):
                domain_data['HAVE_SSL_INCLUE']="1"
            rewrite="/usr/local/nginx/conf/vhost.ssl.d/"+userdata[0]+".rewrite"
            if os.path.exists(rewrite):
                domain_data['HAVE_SSL_REWRITE']="1"
        else:
            print "Generating  nginx "+shellcolor.green+"HTTPS"+shellcolor.end+"  configuration file for "+shellcolor.green+userdata[0]+shellcolor.end+"  ..  "+shellcolor.fail+"failed"+shellcolor.end
            return "#Cpanel ssl vhost data file missing"
    else:
        include="/usr/local/nginx/conf/vhost.d/"+userdata[0]+".include"
        if os.path.exists(include):
            domain_data['HAVE_INCLUE']="1"
        rewrite="/usr/local/nginx/conf/vhost.d/"+userdata[0]+".rewrite"
        if os.path.exists(rewrite):
            domain_data['HAVE_REWRITE']="1"
    fpmsock=add_fpm_user(domain_data['USER'],domain_data['PHP_FPM'])
    domain_data['FPM_SOCK']=fpmsock['FPM_SOCK']
    return httptemplate.render(**domain_data)

