#!/usr/bin/python -B                                                                                                                                                                                                                    
"""
copyright (c) syslint technologies 
Cpnginx Auto Upgrade Tool

"""
import os
import sys
import urllib
import subprocess
def main():
    remoteurl="http://files.syslint.com/version/cpnginx/version.txt"
    remote= urllib.urlopen(remoteurl)
    remote_version=remote.read().strip()
    with open('/etc/cpnginx/version','r') as lo:
        local_version=lo.read().strip()
    if remote_version == local_version:
        print "This server is running the latest version of cpnginx .. "+remote_version
    else:
        newcpnginx="cpnginx-"+remote_version+".tar.gz"
        downcmd="wget -c --no-check-certificate  https://syslintportal.com/downloads/"+newcpnginx+" -O /usr/src/"+newcpnginx
        print "A new version of cpnginx is availabe .. "+remote_version
        print "Downloading new cpnginx installer to ..  /usr/src/"+newcpnginx
        subprocess.call(downcmd,shell=True)
        extract="tar -xzf /usr/src/"+newcpnginx+" -C /usr/src"
        subprocess.call(extract,shell=True)
        autoinstaller="/usr/src/cpnginx-"+remote_version+"/install.py"
        os.chmod(autoinstaller,0750)
        print "Running autoinstaller .."
        udir="/usr/src/cpnginx-"+remote_version
        os.chdir(udir)
        subprocess.call(['./install.py install'],shell=True)
        
if __name__ == "__main__":
    main()
