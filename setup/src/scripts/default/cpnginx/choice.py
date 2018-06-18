import os
import sys
from shellcolor import shellcolor
import datetime
import subprocess
import core
import conf

def option_usage():
	now = datetime.datetime.now()
	print "Copyright (C) 2009-"+str(now.year)+", Syslint Technologies India(P) LTD."
        print "Visit : https://cpnginx.com "
	print "Usage: nginxctl [options] <command>  [parameters]\n"
	print "nginxctl build  <nginx> [--version VALUE ]  |   <vhosts>  | <sslcerts>  | remoteip"
        print "nginxctl setupphpfpm"
	print "nginxctl rebuildvhost  <domain name>"
	print "nginxctl rmvhost  <domain name>"
	print "nginxctl rebuilduservhost  <cpanel user  name>"
	print "nginxctl rmuservhost  <cpanel user  name>"
	print "nginxctl templaterebuild "
	print "nginxctl restart "
	print "nginxctl help "
	print "nginxctl enable" 
	print "nginxctl disable"
	print "nginxctl status"
	print "nginxctl version"

def invalid_option():
    print shellcolor.warning+"Invalid option(s). Please enter the complete options"+shellcolor.end
    option_usage()
    sys.exit()



def  incomplete_option():
    print shellcolor.warning+"Incomplete option(s). Please enter the complete options"+shellcolor.end
    option_usage()
    sys.exit()

def parse_arguments(argus):
    length= len(argus)
    options={}
    if argus[0] == "build":
        if length == 2:
            options['build']=[argus[0],argus[1]]
        elif length == 4:
            options['build']=[argus[0],argus[1],argus[2],argus[3]]
        else:
            incomplete_option()
    elif argus[0] == "rebuildvhost" or argus[0] == "rebuilduservhost" or argus[0] == "rmuservhost" or argus[0] =="rmvhost":
        if length == 2:
            options[argus[0]]=[argus[0],argus[1]]
        else:
            incomplete_option()
    elif argus[0] == "restart" or argus[0] == "help" or argus[0] == "enable" or argus[0] == "disable"  or argus[0] == "status"  or argus[0] == "version" or argus[0] == "setupphpfpm" or  argus[0] == "templaterebuild":
        if length == 1:
            options[argus[0]]=[argus[0]]
        else:
            invalid_option()
    else:
        invalid_option()
    return options
def options():
    argus = sys.argv[1:]
    if not sys.argv[1:]:
        option_usage()
	sys.exit()
    cmd=parse_arguments(argus)
    for command in cmd:
        if command == "build":
            argc=len(cmd[command])
            if argc == 2:
                if cmd[command][1]=="nginx":
                    nversion=conf.NGINXVERSION
                    core.install_nginx(nversion)
                elif cmd[command][1]=="vhosts":
                    core.rebuild_all_vhost()
                elif cmd[command][1]=="sslcerts":
                    core.buildsslcerts()
                elif cmd[command][1]=="remoteip":
                    core.buildremoteip()
                else:
                    invalid_option()
            elif argc == 4:
                if cmd[command][1]=="nginx" and  cmd[command][2]=="--version":
                    nversion=cmd[command][3].strip()
                    core.install_nginx(nversion)
                else:
                    invalid_option()
            else:
                invalid_option()
        elif command == "rebuildvhost":
            rvhdom=cmd[command][1]
            core.rebuildvhost(rvhdom)
        elif command == "rmvhost":
            rvhdom=cmd[command][1]
            core.rmvhost(rvhdom)
        elif command == "rebuilduservhost":
            cpuser=cmd[command][1]
            core.rebuilduservhost(cpuser)
        elif command == "rmuservhost":
            cpuser=cmd[command][1]
            core.rmuservhost(cpuser)
        elif command == "templaterebuild":
            core.templaterebuild()
        elif command == "restart":
            core.restart()
        elif command == "setupphpfpm":
            core.setupphpfpm()
        elif command == "help":
            option_usage()
        elif command == "enable":
            core.enable()
        elif command == "disable":
            core.disable()
        elif command == "status":
            core.status()
        elif command == "version":
            core.version()
        else:
            invalid_option()

