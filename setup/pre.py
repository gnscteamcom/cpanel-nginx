#copyright(c)Syslint technologies 
import os
from shellcolor import shellcolor
import datetime
import subprocess
import version
import deps
import sys
import platform

def precheck():
    version=deps.get_this_version()
    now = datetime.datetime.now()
    subprocess.call('clear',shell=True)
    print shellcolor.green + "..................................................................\n" + shellcolor.end
    print "\t " + shellcolor.bold+" Cpnginx Extended Auto Installer V ( "+ version +" )"+ shellcolor.end
    print "\t  Copyright(c)"+ str(now.year) +" Syslint Technologies"
    print "Extra ordinary Server Management company, Proactive cPanel Server Management Solutions"
    print "email : " + shellcolor.pink +"sales@syslint.com"+ shellcolor.end +" visit  : "+ shellcolor.pink +"https://syslint.com"+ shellcolor.end +"  \n"
    print shellcolor.green + "..................................................................\n" + shellcolor.end
    if os.path.exists("/usr/local/cpanel/version"):
	print "Checking for cPanel .. " + shellcolor.green + "ok" + shellcolor.end 
    else:
	print "Checking for cPanel .. " + shellcolor.fail + "faild" + shellcolor.end 
	print "Installation Failed !!!"
	sys.exit()

    if os.path.exists("/etc/cpnginx/data.conf"):
	print "Checking for Very old version of Cpnginx .. " + shellcolor.fail + "found" + shellcolor.end
	print shellcolor.warning +"This server is running an unsupported old version of cpnginx \nPlease uninstall it using /etc/cpnginx/uninstall.sh before runing this installer !!" +shellcolor.end
	print "Installation Failed !!!"
	sys.exit()
    else:
	print "Checking for Very old version of Cpnginx .. " + shellcolor.green + " clean" + shellcolor.end
        ioncube = deps.check_cpphp_ioncube()
        if ioncube == 0:
	    print "Checking for Ioncube Loader in CPPHP  .. " + shellcolor.green + "ok" + shellcolor.end
        else:
	    print "Checking for Ioncube Loader in CPPHP  .. " + shellcolor.fail + "no" + shellcolor.end
	    print shellcolor.warning +"Please login to WHM as root user and enable Ioncube Loader from the following path\nWHM(root) => Server Configuration -> Tweak Settings -> PHP ->Select ioncube check box for cPanel PHP loader.\nAfter that run this installer again " +shellcolor.end
	    print "Installation Failed !!!"
	    sys.exit()
#        pyver=platform.python_version().split(".")
#        if pyver[0] == "2" and pyver[1] == "6":
#            print "Cpnginx 10 or  need python 2.7 . Your server is running an old version of python  with and old OS"
#            print "Please read the software requirements before installing cpnginx"
#            print shellcolor.fail+"Installation Failed"+shellcolor.end
#            sys.exit(0)
