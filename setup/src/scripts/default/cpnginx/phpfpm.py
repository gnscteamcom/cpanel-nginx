import os
import subprocess
from shellcolor import shellcolor
import conf
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
def ea4_default_php_fpm():
        rpms=conf.cpphpfpm_rpms
        package =""
        for rpm in rpms:
            package +="ea-"+rpm+"-php-fpm ea-"+rpm+"-php-cli "
        command ='yum -y install '+package
        print "Installing  php-fpm(s)  .. "+ shellcolor.green + "starting" + shellcolor.end
        subprocess.call(command,shell=True)
        fpmfinal={}
        defaultphp=subprocess.check_output(["php","-r" ,"echo phpversion();"])
        for rpm in rpms:
            phpfpm="/opt/cpanel/ea-"+rpm+"/root/usr/sbin/php-fpm"
            if os.path.exists(phpfpm):
                print "PHP-FPM  found .. "+ shellcolor.green + phpfpm + shellcolor.end
                pversioncmd="/opt/cpanel/ea-"+rpm+"/root/usr/bin/php"
                pversion=subprocess.check_output([pversioncmd,"-r" ,"echo phpversion();"])
                if pversion == defaultphp:
                    print shellcolor.green+" ===== This is the server default php version "+pversion+"==========" +shellcolor.end
                    default="1"
                else:
                    default="0"
                version=pversion.split(".")
                conffile="/opt/cpanel/ea-"+rpm+"/root/etc/php-fpm.conf"
                confdir="/opt/cpanel/ea-"+rpm+"/root/etc/php-fpm.d"
                service="ea-"+rpm+"-php-fpm.service"
                serviceold="ea-"+rpm+"-php-fpm"
                fpmfinal[rpm]=[version[0],version[1],version[2],phpfpm,conffile,confdir,service,default]
                enable_service="systemctl enable ea-"+rpm+"-php-fpm.service"
                enable_service_old="chkconfig --add ea-"+rpm+"-php-fpm && chkconfig ea-"+rpm+"-php-fpm on"
                copypool = "cp -f /etc/cpnginx/build/templates/fpm/www.conf /opt/cpanel/ea-"+rpm+"/root/etc/php-fpm.d/"
                startfpm="systemctl restart  ea-"+rpm+"-php-fpm.service && systemctl status ea-"+rpm+"-php-fpm.service"
                startfpm_old="service ea-"+rpm+"-php-fpm restart"
                subprocess.call(copypool,shell=True)
                if os.path.exists('/lib/systemd/system'):
                    subprocess.call(enable_service,shell=True)
                    print shellcolor.pink+"Starting php fpm  service version .. "+shellcolor.end+shellcolor.yellow+pversion+shellcolor.end
                    subprocess.call(startfpm,shell=True)
                else:
                    subprocess.call(enable_service_old,shell=True)
                    print shellcolor.pink+"Starting php fpm  service version .. "+shellcolor.end+shellcolor.yellow+pversion+shellcolor.end
                    subprocess.call(startfpm_old,shell=True)

        print "Installing  php-fpm(s)  .. "+ shellcolor.green + "completed" + shellcolor.end
        return fpmfinal
def reloadfpm(rpm):
    service="ea-"+rpm+"-php-fpm.service"
    serviceold="ea-"+rpm+"-php-fpm"
    reloadfpm="systemctl reload  ea-"+rpm+"-php-fpm.service"
    reloadfpm_old="service ea-"+rpm+"-php-fpm reload"
    if os.path.exists('/lib/systemd/system'):
        subprocess.call(reloadfpm,shell=True)
    else:
        subprocess.call(reloadfpm_old,shell=True)

def clear_fpm_user(cpuser):
    for fpm in conf.cpphpfpm_rpms:
        fconf="/opt/cpanel/ea-"+fpm+"/root/etc/php-fpm.d/"+cpuser+".conf"
        if os.path.exists(fconf):
            os.remove(fconf)
            reloadfpm(fpm)
            print "PHP-FPM disabled  for fpm "+shellcolor.green+fpm+shellcolor.end


