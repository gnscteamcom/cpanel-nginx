#copyright(c)Syslint technologies
import os
from shellcolor import shellcolor
import datetime
import subprocess
import version
import deps

def start():
    print "Cpnginx has been removing from your server .. "
    deps.remove_disable()
    deps.remove_files()

