import os
import sys
import choice
if  os.geteuid()==0:
    choice.options()
else:
    print  "Cpnginx Extended"
    sys.exit()
