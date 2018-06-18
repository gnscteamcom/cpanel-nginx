import os
import sys
import re
import glob
from shellcolor import shellcolor
import dataparse
def build_templates():
    apps= glob.glob("/etc/cpnginx/templates/apps/*.conf")
    vhost= glob.glob("/etc/cpnginx/templates/vhost/*.conf")
    custom= glob.glob("/etc/cpnginx/templates/custom/*.conf")
    all=apps + vhost + custom
    data={}
    count=0
    for ffile in all:
        with open(ffile,'r') as conf:
            fline=conf.readline().strip()
        if re.match('#:',fline):
            vline=fline.split(":")
            vfile=ffile.split("/")
            if data.get(vline[1]) == None:
                count += 1
                if vline[1] == "hybrid":
                    print "Adding the template "+shellcolor.green+vline[1]+shellcolor.end+ " as "+shellcolor.yellow+"default"+shellcolor.end+" to the database"
                    data[vline[1]]=[vline[1],vline[2],vfile[4],vline[3],"1"]
                else:
                    print "Adding the template "+shellcolor.green+vline[1]+shellcolor.end+ " to the database"
                    data[vline[1]]=[vline[1],vline[2],vfile[4],vline[3],"0"]
    dataparse.writejson(data,"/etc/cpnginx/data/templates.json")
    print "Auto rebuild of app templates and vhost templates completed . Tototal templates available : " +shellcolor.pink+str(count)+shellcolor.end
