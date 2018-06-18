#copyright(c)Syslint technologies
import os
from shellcolor import shellcolor
import datetime
import subprocess
import version
import deps
import sys
import pre

def clean_old():
    if os.path.exists("/etc/cpnginx/build/templates/conf.d/cpanel-http.conf"):
        subprocess.call(['rm -rf /etc/cpnginx/build/templates/conf.d/cpanel-http.conf'],shell=True)
        subprocess.call(['rm -rf /usr/local/nginx/conf/conf.d/cpanel-http.conf'],shell=True)

def rebuild_all_vhost():
    subprocess.call(['/usr/local/cpanel/scripts/nginxctl build vhosts'],shell=True)

def start():
    with open('/etc/cpnginx/version','r') as lo:
        old_version=lo.read().strip()
    pwd=os.getcwd()
    with open(pwd+"/setup/src/etc/cpnginx/version",'r') as nw:
        new_version=nw.read().strip()
    if old_version == new_version:
        print "This server is runing the same version of cpnignx software .. "+shellcolor.green+new_version+shellcolor.end
        print "If you are looking for reinstall, please remove the current installation."
        print "Upgrade "+shellcolor.fail+"failed"+shellcolor.end+" .. reason .. same versions"
        sys.exit(0)
    else:
        print "Upgrading cpnginx to the new  version .. "+shellcolor.green+new_version+shellcolor.end
        deps.install_deps()
        deps.upgrade_core()
        deps.install_cron()
        deps.install_whm_plugin()
        deps.install_cpanel_plugin()
        deps.install_hooks()
        deps.setup_templates()
        clean_old()
        rebuild_all_vhost()
        deps.restart_services()
        print "---------------------------------------------------------------------------------\n"
        print "\t\t Cpnginx upgrade has been completed "
        print "\tPlease refer the documentation from https://cpnginx.com to getting start\n "
        print "---------------------------------------------------------------------------------\n"
        sys.exit(0)
