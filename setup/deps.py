import sys
import subprocess
import os
from shellcolor import shellcolor
import platform
import dataparse
def find_ea_version():
	command=['/usr/local/cpanel/scripts/easyapache --version']
	DEVNULL = open(os.devnull, 'wb')
	proc=subprocess.Popen(command,stdout=DEVNULL,stderr=DEVNULL,shell=True)
	(output, err) = proc.communicate()
	p_status = proc.wait()
	
	if p_status > 0 :
		ea=4	
	else:
		ea=3
	return ea

def get_this_version():
    vfile="setup/src/etc/cpnginx/version" 
    if os.path.exists(vfile):
        ver=open(vfile,'r')
        version=ver.read().strip()
        return version
    else:
        version="unknown"
        return version

def check_cpphp_ioncube():
    command=['/usr/local/cpanel/3rdparty/bin/php -v | grep ionCube']
    DEVNULL = open(os.devnull, 'wb')
    proc=subprocess.Popen(command,stdout=DEVNULL,stderr=DEVNULL,shell=True)
    (output, err) = proc.communicate()
    p_status = proc.wait()
    return p_status

def install_deps():
    print "Installing dependencies for cpnginx .."
    command="yum -y install python-devel  zlib-devel pcre-devel openssl-devel PyYAML python-mako "
    subprocess.call(command,shell=True)


def upgrade_core():
    print "copying core files"
    pwd=os.getcwd()
    pyver=platform.python_version().split(".")
    if pyver[0] == "2" and pyver[1] == "6":
        cmd_script="/bin/cp -arf "+pwd+"/setup/src/scripts/2.6/* /usr/local/cpanel/scripts/"
    else:
        cmd_script="/bin/cp -arf "+pwd+"/setup/src/scripts/default/* /usr/local/cpanel/scripts/"
    cmd_ctl="ln -sf /usr/local/cpanel/scripts/nginxctl /usr/bin/nginxctl"
    print "Copying   cpgninx files to /etc/ ..."
    etcs=['version','cpnginx-cron']
    for item in etcs:
        cmd_etc="/bin/cp -avrf "+pwd+"/setup/src/etc/cpnginx/"+item+" /etc/cpnginx/"
        subprocess.call(cmd_etc,shell=True)
    print shellcolor.green+"done"+shellcolor.end
    subprocess.call(cmd_script,shell=True)
    print "Copying cpnginx core to /scripts/ .."
    subprocess.call(cmd_ctl,shell=True)
    os.chmod('/usr/local/cpanel/scripts/nginxctl',0750)
    os.chmod('/usr/local/cpanel/scripts/cpnginx/hooks/suspendacct.py',0750)
    susp="ln -sf /usr/local/cpanel/scripts/cpnginx/hooks/suspendacct.py /usr/local/cpanel/scripts/postsuspendacct"
    unsup="ln -sf /usr/local/cpanel/scripts/cpnginx/hooks/suspendacct.py /usr/local/cpanel/scripts/postunsuspendacct"
    subprocess.call(susp,shell=True)
    subprocess.call(unsup,shell=True)
    print shellcolor.green+"done"+shellcolor.end

def copy_core():
    print "copying core files"
    pwd=os.getcwd()
    cmd_etc="/bin/cp -arf "+pwd+"/setup/src/etc/cpnginx /etc/"
    pyver=platform.python_version().split(".")
    if pyver[0] == "2" and pyver[1] == "6":
        cmd_script="/bin/cp -arf "+pwd+"/setup/src/scripts/2.6/* /usr/local/cpanel/scripts/"
    else:
        cmd_script="/bin/cp -arf "+pwd+"/setup/src/scripts/default/* /usr/local/cpanel/scripts/"
    cmd_ctl="ln -sf /usr/local/cpanel/scripts/nginxctl /usr/bin/nginxctl"
    print "Copying   cpgninx files to /etc/ ..."
    subprocess.call(cmd_etc,shell=True)
    print shellcolor.green+"done"+shellcolor.end
    subprocess.call(cmd_script,shell=True)
    print "Copying cpnginx core to /scripts/ .."
    subprocess.call(cmd_ctl,shell=True)
    os.chmod('/usr/local/cpanel/scripts/nginxctl',0750)
    os.chmod('/usr/local/cpanel/scripts/cpnginx/hooks/suspendacct.py',0750)
    susp="ln -sf /usr/local/cpanel/scripts/cpnginx/hooks/suspendacct.py /usr/local/cpanel/scripts/postsuspendacct"
    unsup="ln -sf /usr/local/cpanel/scripts/cpnginx/hooks/suspendacct.py /usr/local/cpanel/scripts/postunsuspendacct"
    subprocess.call(susp,shell=True)
    subprocess.call(unsup,shell=True)
    print shellcolor.green+"done"+shellcolor.end




def ea4_enable_mod_remoteip():
    subprocess.call(['/usr/local/cpanel/scripts/nginxctl  build remoteip'],shell=True)

def install_cron():
    print "Installing SSL Monitoring cron  .. "
    cmd='/bin/cp -af /etc/cpnginx/cpnginx-cron /etc/cron.d/'
    subprocess.call(cmd,shell=True)


def ea4_default_php_fpm():
    subprocess.call(['/usr/local/cpanel/scripts/nginxctl  setupphpfpm'],shell=True)



def change_apache_port():
    dfile="/etc/cpnginx/data/settings.json"
    http_port=dataparse.readjsonval(dfile,"APACHE_HTTP_PORT")[0]
    https_port=dataparse.readjsonval(dfile,"APACHE_HTTPS_PORT")[0]
    cmdhttp='sed -i s/apache_port.*/apache_port=0.0.0.0:'+http_port+'/g /var/cpanel/cpanel.config'
    cmdhttps='sed -i s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:'+https_port+'/g /var/cpanel/cpanel.config'
    subprocess.call(cmdhttp,shell=True)
    subprocess.call(cmdhttps,shell=True)
    subprocess.call(['/usr/local/cpanel/scripts/rebuildhttpdconf'],shell=True)
    subprocess.call(['/usr/local/cpanel/scripts/restartsrv_httpd'],shell=True)

def install_nginx():
    subprocess.call(['/usr/local/cpanel/scripts/nginxctl build nginx'],shell=True)


def install_whm_plugin():
    print "...............................................................................\n"
    print "\t \tInstalling WHM  Nginx Administration Panel   \n"
    print "...............................................................................\n"
    print "Starting installation of whm plugin files .. "+shellcolor.green+"start"+shellcolor.end
    if not os.path.exists("/var/cpanel/apps"):
        subprocess.call(['mkdir -pv /var/cpanel/apps && chmod 750 /var/cpanel/apps'],shell=True)
    pwd=os.getcwd()
    appcfg= pwd+"/setup/src/whm/cpnginx.conf"
    appinstall="/usr/local/cpanel/bin/register_appconfig "+appcfg
    subprocess.call(appinstall,shell=True)
    appfilecmd="/bin/cp -arf "+pwd+"/setup/src/whm/cpnginx /usr/local/cpanel/whostmgr/cgi/"
    subprocess.call(appfilecmd,shell=True)
    cpicon="/bin/cp -af /usr/local/cpanel/whostmgr/cgi/cpnginx/ico-cpnginx.png  /usr/local/cpanel/whostmgr/docroot/addon_plugins/"
    subprocess.call(cpicon,shell=True)
    print "Finishing installation of whm plugins files .. "+shellcolor.green+"done"+shellcolor.end

def install_cpanel_plugin():
    print "..............................................................................\n"
    print "\t \tInstalling cPanel Nginx Plugin   \n"
    print "...............................................................................\n"
    print "Starting installation of cpanel plugin files .. "+shellcolor.green+"start"+shellcolor.end
    pwd=os.getcwd()
    plug=pwd+"/setup/src/cpanel/cpnginx.tar.gz"
    installplug="/usr/local/cpanel/scripts/install_plugin "+plug
    subprocess.call(installplug,shell=True)
    plgcpy="/bin/cp -arf "+pwd+"/setup/src/cpanel/cpnginx /usr/local/cpanel/base/frontend/paper_lantern/"
    subprocess.call(plgcpy,shell=True)
    print "Finishing installation of cpanel plugins files .. "+shellcolor.green+"done"+shellcolor.end

def install_hooks():
    print "Installing cpnginx hooks .."
    subprocess.call(['/usr/local/cpanel/scripts/cpnginx/hooks/cpnginxhooks install'],shell=True)

def setup_templates():
    subprocess.call(['/usr/local/cpanel/scripts/nginxctl templaterebuild'],shell=True)

def setup_chkservd():
    if os.path.exists('/etc/chkserv.d/nginx'):
        print "Nginx Chkservd Configuration file  already exists .. " + shellcolor.green+"ok"+shellcolor.end
    else:
        copycmd='cp -f /etc/cpnginx/build/templates/nginx.chkservd /etc/chkserv.d/nginx'
        subprocess.call(copycmd,shell=True)
        rmng=['grep -v nginx /etc/chkserv.d/chkservd.conf > /tmp/chk.conf']
        subprocess.call(rmng,shell=True)
        enablechk=['echo "nginx:1" >> /tmp/chk.conf ']   # need to add as new line 
        subprocess.call(enablechk,shell=True)
        reng=['cat /tmp/chk.conf > /etc/chkserv.d/chkservd.conf']
        subprocess.call(reng,shell=True)
        changeapache=['sed -i s/80/9080/g /etc/chkserv.d/httpd']
        attr=['chattr +ia /etc/chkserv.d/httpd']
        subprocess.call(changeapache,shell=True)
        subprocess.call(attr,shell=True)
        subprocess.call(['/usr/local/cpanel/scripts/restartsrv_chkservd'],shell=True)
        print "nginx chkservd installed  .. /etc/chkserv.d/nginx .." + shellcolor.green+"ok"+shellcolor.end

def restart_services():
    if os.path.exists('/lib/systemd/system'):
        subprocess.call(['systemctl restart nginx'],shell=True)
        subprocess.call(['systemctl status nginx'],shell=True)
    else:
        subprocess.call(['/etc/init.d/nginx restart'],shell=True)
    subprocess.call(['/usr/local/cpanel/scripts/restartsrv_httpd'],shell=True)
    print shellcolor.pink+"Status of nginx and apache"+shellcolor.end
    print shellcolor.green
    subprocess.call(["netstat -pant | egrep -i 'nginx|httpd'"],shell=True)
    print shellcolor.end


def remove_disable():
    subprocess.call(['/usr/local/cpanel/scripts/nginxctl disable'],shell=True)

def remove_files():
    pwd=os.getcwd()
    cpnaelplugin=pwd+"/setup/src/cpanel/cpnginx.tar.gz"
    rm_cpanel="/usr/local/cpanel/scripts/uninstall_plugin "+cpnaelplugin
    appinstall="/usr/local/cpanel/bin/unregister_appconfig cpnginx"
    sys.stdout.write("Removing nginx chkservd file /etc/chkserv.d/nginx .. ")
    subprocess.call(['rm -f /etc/chkserv.d/nginx'],shell=True)
    print shellcolor.green+"done"+shellcolor.end
    sys.stdout.write("Removing nginx from  /usr/local/nginx  .. ")
    subprocess.call(['rm -rf /usr/local/nginx'],shell=True)
    print shellcolor.green+"done"+shellcolor.end
    sys.stdout.write("Removing cpnginx configurations   /etc/cpnginx  .. ")
    subprocess.call(['rm -rf /etc/cpnginx'],shell=True)
    print shellcolor.green+"done"+shellcolor.end
    sys.stdout.write("Removing cpnginx scripts   /usr/local/cpanel/scripts/cpnginx  .. ")
    subprocess.call(['rm -rf /usr/local/cpanel/scripts/cpnginx'],shell=True)
    print shellcolor.green+"done"+shellcolor.end
    sys.stdout.write("Removing nginxctl     .. ")
    subprocess.call(['rm -rf /usr/local/cpanel/scripts/nginxctl'],shell=True)
    subprocess.call(['unlink /usr/bin/nginxctl'],shell=True)
    print shellcolor.green+"done"+shellcolor.end
    sys.stdout.write("Removing cpnginx cpanel plugin files   .. ")
    subprocess.call(rm_cpanel,shell=True)
    subprocess.call(['rm -rf /usr/local/cpanel/base/frontend/paper_lantern/cpnginx'],shell=True)
    print shellcolor.green+"done"+shellcolor.end
    sys.stdout.write("Removing cpnginx whm plugin files   .. ")
    subprocess.call(appinstall,shell=True)
    subprocess.call(['rm -rf /usr/local/cpanel/whostmgr/cgi/cpnginx'],shell=True)
    print shellcolor.green+"done"+shellcolor.end
    print "......................................................................\n"
    print "\t Cpnginx uninstallation completed !! \n"
    print "......................................................................\n"

