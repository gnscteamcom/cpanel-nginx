import os
import sys
from shellcolor import shellcolor
import datetime
import subprocess
import conf
import subprocess
import multiprocessing
import dataparse
import vhost
import phpfpm
import time
import templates
import udatafile
import cpanel



def install_deps():
    command="yum -y install python-devel  zlib-devel pcre-devel openssl-devel PyYAML python-mako python-virtualenv "
    subprocess.call(command,shell=True)
def cpnginx_version():
    vfile="/etc/cpnginx/version"
    if os.path.exists(vfile):
        ver=open(vfile,'r')
        version=ver.read().strip()
        return version
    else:
        version="unknown"
        return version

def setup_nginx_conf():
    nginx_conf="/etc/cpnginx/build/templates/nginx.conf"
    if os.path.exists("/etc/cpnginx/build/templates/custom/nginx.conf"):
        nginx_conf="/etc/cpnginx/build/templates/custom/nginx.conf"
    print "Installing nginx configuration file from .. " + nginx_conf
    subprocess.call(["rm -f /usr/local/nginx/conf/nginx.conf"],shell=True)
    copyconf='cp -vf '+nginx_conf + " /usr/local/nginx/conf/nginx.conf"
    subprocess.call(copyconf,shell=True)
    if not  os.path.exists("/usr/local/nginx/conf/conf.d/"):
        print "conf.d not exist "
        copyconfd='cp -vrf /etc/cpnginx/build/templates/conf.d /usr/local/nginx/conf/'
        subprocess.call(copyconfd,shell=True)
    if not os.path.exists('/usr/local/nginx/conf/vhost.d/'): 
       print "Creating Virtual Host Configuration Directory .. /usr/local/nginx/conf/vhost.d/"
       subprocess.call(['mkdir -pv /usr/local/nginx/conf/vhost.d/'],shell=True)
    if not os.path.exists('/usr/local/nginx/conf/vhost.ssl.d/'): 
       print "Creating Virtual Host SSL  Configuration Directory .. /usr/local/nginx/conf/vhost.ssl.d/"
       subprocess.call(['mkdir -pv /usr/local/nginx/conf/vhost.ssl.d/'],shell=True)
    if not os.path.exists('/usr/local/nginx/conf/ssl.cert.d/'): 
       print "Creating  SSL  Certificate  Directory .. /usr/local/nginx/conf/ssl.cert.d/"
       subprocess.call(['mkdir -pv /usr/local/nginx/conf/ssl.cert.d/'],shell=True)
    if not os.path.exists('/usr/local/nginx/conf/ssl.ca.d/'): 
       print "Creating  SSL  CA File  Directory .. /usr/local/nginx/conf/ssl.ca.d/"
       subprocess.call(['mkdir -pv /usr/local/nginx/conf/ssl.ca.d/'],shell=True)
    if not os.path.exists('/usr/local/nginx/conf/ssl.key.d/'): 
       print "Creating  SSL  Key  Directory .. /usr/local/nginx/conf/ssl.key.d/"
       subprocess.call(['mkdir -pv /usr/local/nginx/conf/ssl.key.d/'],shell=True)

def setup_nginx_startup():
    if os.path.exists('/lib/systemd/system'):
        print "Installing nginx systemd service "
        subprocess.call(['cp -f /etc/cpnginx/build/templates/nginx.service /lib/systemd/system/'],shell=True)
        subprocess.call(['systemctl enable nginx.service'],shell=True)
        subprocess.call(['systemctl daemon-reload'],shell=True)
    else:
        print "Installing nginx init script"
        subprocess.call(['cp -f /etc/cpnginx/build/templates/nginx.rc /etc/init.d/nginx'],shell=True)
        subprocess.call(['chmod 0755 /etc/init.d/nginx'],shell=True)
        subprocess.call(['chkconfig --add nginx'],shell=True)
        subprocess.call(['chkconfig nginx on'],shell=True)

def setup_nginx_chkservd():
    if os.path.exists('/etc/chkserv.d/nginx'):
        print "Nginx Chkservd Configuration file  already exists .. " + shellcolor.green+"ok"+shellcolor.end
    else:
        copycmd='cp -f /etc/cpnginx/build/templates/nginx.chkservd /etc/chkserv.d/nginx'
        subprocess.call(copycmd,shell=True)
        enablechk=['echo "nginx:1" >> /etc/chkserv.d/chkservd.conf ']   # need to add as new line 
        subprocess.call(enablechk,shell=True)
        changeapache=['sed -i s/80/9080/g /etc/chkserv.d/httpd']
        attr=['chattr +ia /etc/chkserv.d/httpd']
        subprocess.call(changeapache,shell=True)
        subprocess.call(attr,shell=True)
        subprocess.call(['/usr/local/cpanel/scripts/restartsrv_chkservd'],shell=True)
        print "nginx chkservd installed  .. /etc/chkserv.d/nginx .." + shellcolor.green+"ok"+shellcolor.end
        
def change_apache_port():
    dfile="/etc/cpnginx/data/settings.json"
    http_port=dataparse.readjsonval(dfile,"APACHE_HTTP_PORT")[0]
    https_port=dataparse.readjsonval(dfile,"APACHE_HTTPS_PORT")[0]
    cmdhttp='sed -i s/apache_port.*/apache_port=0.0.0.0:'+http_port+'/g /var/cpanel/cpanel.config'
    cmdhttps='sed -i s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:'+https_port+'/g /var/cpanel/cpanel.config'
 #   cmdhttp='sed -i s/apache_port.*/apache_port=0.0.0.0:9080/g /var/cpanel/cpanel.config'
 #   cmdhttps='sed -i s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:9443/g /var/cpanel/cpanel.config'
    subprocess.call(cmdhttp,shell=True)
    subprocess.call(cmdhttps,shell=True)
    subprocess.call(['/usr/local/cpanel/scripts/rebuildhttpdconf'],shell=True)
    subprocess.call(['/usr/local/cpanel/scripts/restartsrv_httpd'],shell=True)

def restart_nginx():
    if os.path.exists('/lib/systemd/system'):
        subprocess.call(['systemctl restart nginx'],shell=True)
        subprocess.call(['systemctl status nginx'],shell=True)
    else:
        subprocess.call(['/etc/init.d/nginx restart'],shell=True)
def reload_nginx():
    subprocess.call(['/usr/local/nginx/sbin/nginx -s reload'],shell=True)
#-----------------------------Start  of Nginx Build -----------------------------------------#

def install_nginx(version):
    print "-------------------------------------------------"
    print shellcolor.blue+"Installing Nginx Web Server version : "+shellcolor.end + shellcolor.green + version + shellcolor.end
    print "-------------------------------------------------"
    print "Installing nginx dependencies  ..." 
    print shellcolor.bold
    install_deps()
    print shellcolor.end
    source_nginx=conf.SRCDIR+"/nginx-"+version+".tar.gz"
    source_nginx_dir=conf.SRCDIR+"/nginx-"+version
    source_nginx_module=conf.SRCDIR+"/nginx_modules.tar.gz"
    source_nginx_modulr_dir=conf.SRCDIR+"/nginx_modules"
    print "Nginx Source File  : " + source_nginx
    print "Nginx build root   : " + source_nginx_dir
    print "Nginx module       : " + source_nginx_module
    print "Nginx module root  : " + source_nginx_modulr_dir
    cleanbuild="rm -rf " + source_nginx_dir
    cleadmods="rm -rf "+ source_nginx_modulr_dir
    subprocess.call(cleanbuild,shell=True)
    subprocess.call(cleadmods,shell=True)
    cachedir="mkdir /var/cache/nginx && chown nobody.nobody /var/cache/nginx"
    subprocess.call(cachedir,shell=True)
    if os.path.exists(source_nginx):
        print "Nginx Source file  found .. " + shellcolor.green + "ok" + shellcolor.end
    else:
        print "Nginx Source file  found .. " + shellcolor.fail + "none" + shellcolor.end
        download_nginx=conf.wget+" -c " + conf.NGINXDOWNLOAD+"/nginx-"+version+".tar.gz  -O  "+ source_nginx
        subprocess.call(download_nginx,shell=True)
    pagespeed=val=dataparse.readjsonval('/etc/cpnginx/data/settings.json','GOOGLE_PAGE_SPEED')
    configure = "/etc/cpnginx/build/configure.sh"
    if os.path.exists("/etc/cpnginx/build/custom/configure.sh"):
        configure="/etc/cpnginx/build/custom/configure.sh"
    if pagespeed[0] == "1":
        if not os.path.exists("/usr/local/nginx/conf/conf.d/pagespeed.conf"):
            subprocess.call(['cp -f /etc/cpnginx/build/templates/conf.d/pagespeed.conf /usr/local/nginx/conf/conf.d/'],shell=True)
        if os.path.exists(source_nginx_module):
            print "Nginx Module Source file  found .. " + shellcolor.green + "ok" + shellcolor.end
        else:
            print "Nginx Modules Source file  found .. " + shellcolor.fail + "none" + shellcolor.end
            download_nginx_mod=conf.wget+" -c http://files.syslint.com/src/nginx/nginx_modules.tar.gz   -O  "+ source_nginx_module
            subprocess.call(download_nginx_mod,shell=True)
        print "Extracting nginx module source files in  " + source_nginx_modulr_dir + " please wait ...."
        extract_nginx_mod=conf.tar+" -xzf "+source_nginx_module+ " -C "+conf.SRCDIR
        subprocess.call(extract_nginx_mod,shell=True)
        print shellcolor.green+"done"+shellcolor.end
        time.sleep(3)
        configure ="/etc/cpnginx/build/configure.pagespeed.sh"
        if os.path.exists("/etc/cpnginx/build/custom/configure.pagespeed.sh"):
            configure="/etc/cpnginx/build/custom/configure.pagespeed.sh"
    else:
        if os.path.exists("/usr/local/nginx/conf/conf.d/pagespeed.conf"):
            os.remove("/usr/local/nginx/conf/conf.d/pagespeed.conf")
    print "Extracting nginx source files in  " + source_nginx_dir  
    extract_nginx=conf.tar+" -xzf "+source_nginx+ " -C "+conf.SRCDIR
    subprocess.call(extract_nginx,shell=True)
    if os.path.exists(source_nginx_dir):
        print "Changing builddir to "+source_nginx_dir+ " .. " + shellcolor.green + "done"+shellcolor.end
        os.chdir(source_nginx_dir)
        subprocess.call("pwd",shell=True)
        print "Running nginx autoconfigure : "+ shellcolor.green + configure + shellcolor.end
        configure_perm="chmod 0755 "  + configure
        print configure_perm
        subprocess.call(configure_perm, shell=True)
        nginxbuild_cmd=configure+ " && make -j"+str(multiprocessing.cpu_count())+ " && make install"
        print "Executing Nginx Build command  .. " +shellcolor.bold+  nginxbuild_cmd+shellcolor.end
        subprocess.call(nginxbuild_cmd, shell=True)
    else:
        print "Nginx extraction failed .. unable to install "
        sys.exist()
    os.chdir("/usr/local/cpanel/scripts/cpnginx")
    if not os.path.exists("/usr/local/nginx/sbin/nginx"):
        print "Nginx installation  .. " + shellcolor.fail + "FAILD" + shellcolor.end
    else:
        print "Nginx installation  .. " + shellcolor.green + "SUCCESS" + shellcolor.end
        if not  os.path.exists("/usr/local/nginx/sbin/nginx"):
            print shellcolor.fail + " Nginx compile failed . Please contact support" + shellcolor.end
            sys.exit()
        setup_nginx_conf()
        if pagespeed[0] == "0":
            if os.path.exists("/usr/local/nginx/conf/conf.d/pagespeed.conf"):
                os.remove("/usr/local/nginx/conf/conf.d/pagespeed.conf")
        setup_nginx_startup()    
        setup_nginx_chkservd()
        change_apache_port()
        rebuild_all_vhost()
        print shellcolor.yellow
        subprocess.call(['/usr/local/nginx/sbin/nginx -V'],shell=True)
        print shellcolor.end
        restart_nginx()
#-----------------------------End of Nginx Build -----------------------------------------#

def status():
    if os.path.exists('/lib/systemd/system'):
        cmdstatus='systemctl status nginx.service'
    else:
        cmdstatus='/etc/init.d/nginx status'
    subprocess.call(cmdstatus,shell=True)

def restart():
    print shellcolor.yellow+"......... Restarting Nginx Web  Server ..... starting .."+shellcolor.end
    restart_nginx()
    print shellcolor.yellow+"......... Restarting Nginx Web  Server ..... finished .."+shellcolor.end

def version():
    print "Cpnginx  Version : " + cpnginx_version() 
    nginxversion=subprocess.check_output(['/usr/local/nginx/sbin/nginx -v'],shell=True)
    apacheversion=subprocess.check_output(["httpd -v | head -1  | awk '{ print $3 }'"],shell=True)
    print "Apache version : " + apacheversion.strip()

def buildsslcerts():
    print "Rebuilding all ssl certificate , key and ca-bulde files  "
    vhost.build_all_ssl_certs()
    reload_nginx
    print shellcolor.green+"DONE"+shellcolor.end

def rebuild_all_vhost():
    userdata=dataparse.get_vhost_data()
    userdata.update(udatafile.get_vhost_data_from_file())
    ssldata=cpanel.get_all_ssl_certificates()
    #ssldomain=vhost.get_ssl_domains()
    dedicate_ip=vhost.get_dedicated_ip_domains()
    firewall=vhost.get_firewall()
    settings=vhost.get_default_settings()
    for domain in userdata:
        #print userdata
        confpath='/usr/local/nginx/conf/vhost.d/'+domain+'.conf'
        havessl="0"
        if domain in dedicate_ip:
            havedip="1"
        else:
            havedip="0"
        vhostdata =  vhost.build_vhost(userdata[domain],havessl,havedip,firewall,settings,ssldata)
        fo=open(confpath,"wb")
        fo.write(vhostdata)
        fo.close()
        vhostdata=""
        print "Generating  nginx "+shellcolor.pink+"HTTP"+shellcolor.end+"  configuration file for " +shellcolor.green+ domain+shellcolor.end + " on ... " + shellcolor.yellow+confpath+shellcolor.end
        if userdata[domain][2] == "addon" or userdata[domain][2] == "parked":
            sdomain=userdata[domain][3]
            if sdomain in ssldata:
                keycrt=ssldata[sdomain]['key']
                cert=ssldata[sdomain]['certificate']
                ca=ssldata[sdomain]['cabundle']
                ssldata[domain]={'key': keycrt,'certificate': cert,'cabundle': ca}
        #if domain in ssldomain:
        #if vhost.have_valid_ssl(domain):
        if domain in ssldata:
            havessl="1"
            confpath_ssl='/usr/local/nginx/conf/vhost.ssl.d/'+domain+'.conf'
            vhostdata_ssl =  vhost.build_vhost(userdata[domain],havessl,havedip,firewall,settings,ssldata)
            fo=open(confpath_ssl,"wb")
            fo.write(vhostdata_ssl)
            fo.close()
            vhostdata_ssl=""
            print "Generating  nginx "+shellcolor.green+"HTTPS"+shellcolor.end+"  configuration file for " +shellcolor.green+ domain+shellcolor.end + " on ... " + shellcolor.yellow+confpath_ssl+shellcolor.end
    vhost.build_defaul_vhost()
    reload_nginx()

def rebuildvhost(domain):
    alluserdata=dataparse.get_vhost_data()
    firewall=vhost.get_firewall()
    settings=vhost.get_default_settings()
    userdata={}
    if domain in alluserdata:
        userdata[domain]=alluserdata[domain]
        domainvalid="1"
    else:
        domainvalid="0"
    if domainvalid == "0":
        alluserdata=udatafile.get_vhost_data_from_file()
        if domain in alluserdata:
            userdata[domain]=alluserdata[domain]
            domainvalid="1"
        else:
            domainvalid="0"
    if domainvalid == "1":
        #ssldomain=vhost.get_ssl_domains()
        ssldata=cpanel.get_all_ssl_certificates()
        dedicate_ip=vhost.get_dedicated_ip_domains()
        confpath='/usr/local/nginx/conf/vhost.d/'+domain+'.conf'
        havessl="0"
        if userdata[domain][2] == "addon" or userdata[domain][2] == "parked":
            sdomain=userdata[domain][3]
            if sdomain in ssldata:
                keycrt=ssldata[sdomain]['key']
                cert=ssldata[sdomain]['certificate']
                ca=ssldata[sdomain]['cabundle']
                ssldata[domain]={'key': keycrt,'certificate': cert,'cabundle': ca}
        if domain in dedicate_ip:
            havedip="1"
        else:
            havedip="0"
        vhostdata =  vhost.build_vhost(userdata[domain],havessl,havedip,firewall,settings,ssldata)
        fo=open(confpath,"wb")
        fo.write(vhostdata)
        fo.close()
        vhostdata=""
        print "Generating  nginx "+shellcolor.pink+"HTTP"+shellcolor.end+"  configuration file for " +shellcolor.green+ domain+shellcolor.end + " on ... " + shellcolor.yellow+confpath+shellcolor.end
        #if domain in ssldomain:
        #if vhost.have_valid_ssl(domain):
        if domain in ssldata:
            havessl="1"
            confpath_ssl='/usr/local/nginx/conf/vhost.ssl.d/'+domain+'.conf'
            vhostdata_ssl =  vhost.build_vhost(userdata[domain],havessl,havedip,firewall,settings,ssldata)
            fo=open(confpath_ssl,"wb")
            fo.write(vhostdata_ssl)
            fo.close()
            vhostdata_ssl=""
            print "Generating  nginx "+shellcolor.green+"HTTPS"+shellcolor.end+"  configuration file for " +shellcolor.green+ domain+shellcolor.end + " on ... " + shellcolor.yellow+confpath_ssl+shellcolor.end

    else:
        print "Rebuilding vhost ..  "+ domain + shellcolor.fail +" ..  failed  ..  No such domain !!!"+shellcolor.end
    reload_nginx()

def rebuilduservhost(cpuser):
    firewall=vhost.get_firewall()
    settings=vhost.get_default_settings()
    if os.path.exists("/var/cpanel/users/"+cpuser):
        print "Rebuilding all domains nginx vhost configuration files for  user ..." +shellcolor.pink+cpuser+shellcolor.end
        userdata=vhost.get_user_domains(cpuser)
        #ssldomain=vhost.get_ssl_domains()
        ssldata=cpanel.get_all_ssl_certificates()
        dedicate_ip=vhost.get_dedicated_ip_domains()
        for domain in userdata:
            #print userdata[domain]
            confpath='/usr/local/nginx/conf/vhost.d/'+domain+'.conf'
            havessl="0"
            if domain in dedicate_ip:
                havedip="1"
            else:
                havedip="0"
            vhostdata =  vhost.build_vhost(userdata[domain],havessl,havedip,firewall,settings,ssldata)
            fo=open(confpath,"wb")
            fo.write(vhostdata)
            fo.close()
            vhostdata=""
            print "Generating  nginx "+shellcolor.pink+"HTTP"+shellcolor.end+"  configuration file for " +shellcolor.green+ domain+shellcolor.end + " on ... " + shellcolor.yellow+confpath+shellcolor.end
            #if domain in ssldomain:
            #if vhost.have_valid_ssl(domain):
            if domain in ssldata:
                havessl="1"
                confpath_ssl='/usr/local/nginx/conf/vhost.ssl.d/'+domain+'.conf'
                vhostdata_ssl =  vhost.build_vhost(userdata[domain],havessl,havedip,firewall,settings,ssldata)
                fo=open(confpath_ssl,"wb")
                fo.write(vhostdata_ssl)
                fo.close()
                vhostdata_ssl=""
                print "Generating  nginx "+shellcolor.green+"HTTPS"+shellcolor.end+"  configuration file for " +shellcolor.green+ domain+shellcolor.end + " on ... " + shellcolor.yellow+confpath_ssl+shellcolor.end
    else:
        print "No such cpanel user .. "+shellcolor.fail+"NOT FOUND"+shellcolor.end
    reload_nginx()

def rmuservhost(cpuser):
    if not os.path.exists("/var/cpanel/users/"+cpuser):
        print "Unknown user "+ cpuser
        sys.exit()
    userdata=vhost.get_user_domains(cpuser)
    for domain  in userdata:
        vdom="/usr/local/nginx/conf/vhost.d/"+domain+".conf"
        vdomin="/usr/local/nginx/conf/vhost.d/"+domain+".include"
        vdomre="/usr/local/nginx/conf/vhost.d/"+domain+".rewrite"
        vdomssl="/usr/local/nginx/conf/vhost.ssl.d/"+domain+".conf"
        vdomsslin="/usr/local/nginx/conf/vhost.ssl.d/"+domain+".include"
        vdomsslre="/usr/local/nginx/conf/vhost.ssl.d/"+domain+".rewrite"
        ddata="/etc/cpnginx/domains/"+domain+".json"
        if os.path.exists(ddata):
            os.remove(ddata)
        if os.path.exists(vdom):
            os.remove(vdom)
            print "Removed Nginx vhost configuration "+shellcolor.green+vdom+shellcolor.end
        if os.path.exists(vdomin):
            os.remove(vdomin)
            print "Removed Nginx vhost include "+shellcolor.green+vdomin+shellcolor.end
        if os.path.exists(vdomre):
            os.remove(vdomre)
            print "Removed Nginx vhost rewrite "+shellcolor.green+vdomre+shellcolor.end
        if os.path.exists(vdomssl):
            sslcrt="/usr/local/nginx/conf/ssl.cert.d/"+domain+"_cert"
            sslkey="/usr/local/nginx/conf/ssl.key.d/"+domain+"_key"
            sslca="/usr/local/nginx/conf/ssl.ca.d/"+domain+"_ca-bundle"
            if os.path.exists(sslcrt):
                os.remove(sslcrt)
                print "Removed ssl certificate "+shellcolor.green+sslcrt+shellcolor.end
            if os.path.exists(sslkey):
                os.unlink(sslkey)
                print "Removed ssl keyfile "+shellcolor.green+sslkey+shellcolor.end
            if os.path.exists(sslca):
                os.unlink(sslca)
                print "Removed ssl ca-bundle "+shellcolor.green+sslca+shellcolor.end
            os.remove(vdomssl)
            print "Removed Nginx ssl vhost  "+shellcolor.green+vdomssl+shellcolor.end
        if os.path.exists(vdomsslin):
            os.remove(vdomsslin)
            print "Removed Nginx ssl vhost include "+shellcolor.green+vdomsslin+shellcolor.end
        if os.path.exists(vdomsslre):
            os.remove(vdomsslre)
            print "Removed Nginx ssl vhost rewrite "+shellcolor.green+vdomsslre+shellcolor.end
    phpfpm.clear_fpm_user(cpuser)
    subprocess.call(['/usr/local/nginx/sbin/nginx -s reload'],shell=True)
def rmvhost(domain):
    vdom="/usr/local/nginx/conf/vhost.d/"+domain+".conf"
    vdomin="/usr/local/nginx/conf/vhost.d/"+domain+".include"
    vdomre="/usr/local/nginx/conf/vhost.d/"+domain+".rewrite"
    vdomssl="/usr/local/nginx/conf/vhost.ssl.d/"+domain+".conf"
    vdomsslin="/usr/local/nginx/conf/vhost.ssl.d/"+domain+".include"
    vdomsslre="/usr/local/nginx/conf/vhost.ssl.d/"+domain+".rewrite"
    ddata="/etc/cpnginx/domains/"+domain+".json"
    if os.path.exists(ddata):
        os.remove(ddata)
    if os.path.exists(vdom):
        os.remove(vdom)
        print "Removed Nginx vhost configuration "+shellcolor.green+vdom+shellcolor.end
    if os.path.exists(vdomin):
        os.remove(vdomin)
        print "Removed Nginx vhost include "+shellcolor.green+vdomin+shellcolor.end
    if os.path.exists(vdomre):
        os.remove(vdomre)
        print "Removed Nginx vhost rewrite "+shellcolor.green+vdomre+shellcolor.end
    if os.path.exists(vdomssl):
        sslcrt="/usr/local/nginx/conf/ssl.cert.d/"+domain+"_cert"
        sslkey="/usr/local/nginx/conf/ssl.key.d/"+domain+"_key"
        sslca="/usr/local/nginx/conf/ssl.ca.d/"+domain+"_ca-bundle"
        if os.path.exists(sslcrt):
            os.remove(sslcrt)
            print "Removed ssl certificate "+shellcolor.green+sslcrt+shellcolor.end
        if os.path.exists(sslkey):
            os.unlink(sslkey)
            print "Removed ssl keyfile "+shellcolor.green+sslkey+shellcolor.end
        if os.path.exists(sslca):
            os.unlink(sslca)
            print "Removed ssl ca-bundle "+shellcolor.green+sslca+shellcolor.end
        os.remove(vdomssl)
        print "Removed Nginx ssl vhost  "+shellcolor.green+vdomssl+shellcolor.end
    if os.path.exists(vdomsslin):
        os.remove(vdomsslin)
        print "Removed Nginx ssl vhost include "+shellcolor.green+vdomsslin+shellcolor.end
    if os.path.exists(vdomsslre):
        os.remove(vdomsslre)
        print "Removed Nginx ssl vhost rewrite "+shellcolor.green+vdomsslre+shellcolor.end
    subprocess.call(['/usr/local/nginx/sbin/nginx -s reload'],shell=True)
def enable():
    if  os.path.exists("/etc/cpnginx/disablecpnginx"):
        changeapache=['sed -i s/80/9080/g /etc/chkserv.d/httpd']
        attr=['chattr +ia /etc/chkserv.d/httpd']
        subprocess.call(changeapache,shell=True)
        subprocess.call(attr,shell=True)
        subprocess.call(['/usr/local/cpanel/scripts/cpnginx/hooks/cpnginxhooks install'],shell=True)
        setup_nginx_chkservd()
        change_apache_port()
        restart_nginx()
        os.remove('/etc/cpnginx/disablecpnginx')
        print shellcolor.yellow+"See the default webserver status below"+shellcolor.end
        subprocess.call(['netstat -pant | egrep nginx'],shell=True)
        subprocess.call(['netstat -pant | egrep httpd'],shell=True)
        print "Cpginx has been enabled"
    else:
        print "Cpnginx is already enabled  .. " + shellcolor.green +"done"+shellcolor.end

def disable():
    if os.path.exists("/etc/cpnginx/disablecpnginx"):
        print "Cpnginx is already disabled  .. " + shellcolor.green +"done"+shellcolor.end
    else:
        cmdchk="grep -v nginx /etc/chkserv.d/chkservd.conf > /tmp/disable.nginx"
        cmdchkre="cat /tmp/disable.nginx > /etc/chkserv.d/chkservd.conf"
        attr=['chattr -ia /etc/chkserv.d/httpd']
        changeapache=['sed -i s/9080/80/g /etc/chkserv.d/httpd']
        cmdhttp='sed -i s/apache_port.*/apache_port=0.0.0.0:80/g /var/cpanel/cpanel.config'
        cmdhttps='sed -i s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:443/g /var/cpanel/cpanel.config'
        subprocess.call(cmdhttp,shell=True)
        subprocess.call(cmdhttps,shell=True)
        subprocess.call(['/usr/local/cpanel/scripts/rebuildhttpdconf'],shell=True)
        if os.path.exists('/lib/systemd/system'):
            subprocess.call(['systemctl stop nginx'],shell=True)
        else:
            subprocess.call(['/etc/init.d/nginx stop'],shell=True)
        subprocess.call(cmdchk,shell=True)
        subprocess.call(cmdchkre,shell=True)
        subprocess.call(attr,shell=True)
        subprocess.call(changeapache,shell=True)
        subprocess.call(['rm -f /etc/chkserv.d/nginx'],shell=True)
        subprocess.call(['/usr/local/cpanel/scripts/restartsrv_chkservd'],shell=True)
        subprocess.call(['/usr/local/cpanel/scripts/restartsrv_httpd'],shell=True)
        subprocess.call(['/usr/local/cpanel/scripts/cpnginx/hooks/cpnginxhooks remove'],shell=True)
        subprocess.call(['touch /etc/cpnginx/disablecpnginx'],shell=True)
        print shellcolor.yellow+"See the default webserver status below"+shellcolor.end
        subprocess.call(['netstat -pant | grep httpd'],shell=True)
        
def setupphpfpm():
    fpmdb=phpfpm.ea4_default_php_fpm()  
    filename="/etc/cpnginx/data/fpm.json"
    dataparse.writejson(fpmdb,filename)
def templaterebuild():
    templates.build_templates()

def buildremoteip():
    command=['httpd -M | grep remoteip_module']
    DEVNULL = open(os.devnull, 'wb')
    proc=subprocess.Popen(command,stdout=DEVNULL,stderr=DEVNULL,shell=True)
    (output, err) = proc.communicate()
    p_status = proc.wait()
    if p_status == 1:
        command1=['yum -y install ea-apache24-mod_remoteip']
        subprocess.call(command1,shell=True)
        print "Installing  mod-remoteip for Apache .. "+ shellcolor.green + "starting" + shellcolor.end  
        command2=['/usr/local/cpanel/scripts/ipusage| awk \'{print $1}\'']
        y=subprocess.check_output(command2,shell=True).split()
        remoteip="RemoteIPHeader X-Real-IP\nRemoteIPInternalProxy 127.0.0.1\n"
        for i in y:
            remoteip += "RemoteIPInternalProxy " + i +"\n"
        conf=open("/etc/apache2/conf.modules.d/361_mod_cpgninx.conf","w")
        conf.write(remoteip)
        conf.close()
        print "Installing  mod-remoteip for Apache .. "+ shellcolor.green + "done" + shellcolor.end  
        result ="ok"
    else:
        print "Installing  mod-remoteip configurations for  Apache .. "+ shellcolor.green + "starting" + shellcolor.end  
        command2=['/usr/local/cpanel/scripts/ipusage| awk \'{print $1}\'']
        y=subprocess.check_output(command2,shell=True).split()
        remoteip="RemoteIPHeader X-Real-IP\nRemoteIPInternalProxy 127.0.0.1\n"
        for i in y:
            remoteip += "RemoteIPInternalProxy " + i +"\n"
        conf=open("/etc/apache2/conf.modules.d/361_mod_cpgninx.conf","w")
        conf.write(remoteip)
        conf.close()
        print "Installing  mod-remoteip configurations for  Apache .. "+ shellcolor.green + "done" + shellcolor.end  
        result ="ok"
    sys.stdout.write( "Running Apache Domlog  Fix .. ")
    cmd="sed -i s/%h/%a/g /var/cpanel/templates/apache2_4/ea4_main.default"
    subprocess.call(cmd,shell=True)
    cmdap="/usr/local/cpanel/scripts/rebuildhttpdconf"
    result=subprocess.check_output(cmdap,shell=True)
    print shellcolor.green+"done"+shellcolor.end

    return  result






























