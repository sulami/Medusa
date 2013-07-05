#!/usr/bin/env python

# Medusa Peer Controller

from daemon import Daemon
import os
import socket
import subprocess
import sys

INST_PATH = "/home/sulami/medusa/peer/"

IP = '0.0.0.0'
PORT = 5006
BUFFER_SIZE = 1024
moden = []

# Check for enabled modules in modules.enabled
try:
    f_moden = open(INST_PATH + "modules.enabled", mode='r')
    for line in f_moden.readlines():
        moden.append(line.rstrip('\n'))
except:
    print "ERROR - CANNOT READ modules.enabled"
    # not quite optimal yet
    quit()

# Open socket and listen
def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(5)

    conn, addr = s.accept()
    while 1:
        query = conn.recv(BUFFER_SIZE)
        if not query: break
        nquery = query.rstrip('\n')
        try:
            nnquery = nquery.split(' ', 1)
        except:
            nnquery = [nquery]
        if os.path.isfile(INST_PATH + 'modules/' + nnquery[0]) and nnquery[0] in moden:
            try:
                result = subprocess.check_output([INST_PATH + 'modules/' + nnquery[0], nnquery[1]])
                conn.send(result)
            except subprocess.CalledProcessError, e:
                conn.send(e.output)
            except:
                try:
                    result = subprocess.check_output(INST_PATH + 'modules/' + nnquery[0])
                    conn.send(result)
                except:
                    conn.send("ERROR - MODULE " + nquery + " FAILED TO RUN (BROKEN/MISSING MODULE?)\n")
        else:
            conn.send("ERROR - MODULE " + nquery + " NOT FOUND OR DISABLED (modules.enabled?)\n")
    conn.close()
    s.close()
"""
while 1:
    listen()
"""
# Generic Unix daemon code, courtesy of Sander Marechal, http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class MyDaemon(Daemon):
    def run(self):
        while True:
            listen()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/medusa-peer.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

