#!/usr/bin/python -B
import sys
import os
import time
import atexit
import signal
from shellcolor import shellcolor
import logging
import logging.handlers
import subprocess
class Monitor:
    def __init__(self, pidfile): self.pidfile = pidfile
    
    def daemonize(self):
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError as err: 
            sys.stderr.write('Nginx Monitor Fork  failed: {0}\n'.format(err))
            sys.exit(1)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0) 
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1) 

        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile,'w+') as f:
            f.write(pid + '\n')
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:           
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        if pid:
            message = "Nginx Monitor already "+shellcolor.green+"running"+shellcolor.end+" with pidfile {0}  \n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)
        
        # Start the daemon
        print "Starting cpnginx monitor .. "+shellcolor.green+"done"+shellcolor.end
        self.daemonize()
        self.run()

    def stop(self):
        # Get the pid from the pidfile
        try:
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if not pid:
            message = "Nginx monitor is "+shellcolor.fail+"not running"+shellcolor.end+" pidfile {0} does not exist.\n"
            sys.stderr.write(message.format(self.pidfile))
            return # not an error in a restart

        # Try killing the  Monitor daemon process    
        try:
            print "Stopping cpnginx monitor .. "+shellcolor.green+"done"+shellcolor.end
            # Get the pid from the pidfile
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print (str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the  monitor daemon."""
        self.stop()
        self.start()

    def run(self):
        """
        Cpnginx monitor log override
        """
