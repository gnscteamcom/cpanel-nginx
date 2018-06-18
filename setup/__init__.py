import os
import sys
import shellcolor
import setup
import install
import upgrade
import remove
import datetime
if  os.geteuid()==0:
    if len(sys.argv) == 2:
        if 'install' == sys.argv[1]:
            if os.path.exists('/etc/cpnginx/version'):
                upgrade.start()
            else:
                install.start()
        elif 'remove' == sys.argv[1]:
            remove.start()
        else:
            print "Unknown command"
            sys.exit(2)
            sys.exit(0)
    else:
        now = datetime.datetime.now()
        print "Copyright (C) 2009-"+str(now.year)+", Syslint Technologies India(P) LTD."
        print "Cpnginx auto installer and uninstall script"
        print "Visit : https://cpnginx.com "
        print "Usage: %s install | remove" % sys.argv[0]
        sys.exit(2)
else:
    print "Cpnginx auto installer"
    sys.exit(2)

