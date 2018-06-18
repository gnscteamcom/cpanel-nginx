#copyright(c)Syslint technologies
import os
from shellcolor import shellcolor
import datetime
import subprocess
import version
import deps
import sys
import pre
def start():
    print "Starting Cpnginx auto installer ... "
    eaver = deps.find_ea_version()
    pre.precheck()
    if eaver >= 4 :
        print "Checking for EasyApacheVersion .. " + shellcolor.green + "v 4 " + shellcolor.end
        deps.install_deps()
        deps.copy_core()
        deps.ea4_enable_mod_remoteip()
        deps.ea4_default_php_fpm()
        deps.change_apache_port()
        deps.install_nginx()
        deps.install_whm_plugin()
        deps.install_cpanel_plugin()
        deps.install_hooks()
        deps.install_cron()
        deps.setup_templates()
        deps.setup_chkservd()
        deps.restart_services()
        print "---------------------------------------------------------------------------------\n"
        print "\t\t Cpnginx installation has been completed "
        print "\tPlease refer the documentation from https://cpnginx.com to getting start\n "
        print "---------------------------------------------------------------------------------\n"
    else:
        print "Checking for EasyApacheVersion .. " + shellcolor.fail + "v 3" + shellcolor.end
        print "Cpnginx v10 or higher won't support  Easyapache 3 . Please consider upgrading Easyapche"
        sys.exit(0)
