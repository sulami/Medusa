#!/usr/bin/env python

# Medusa Master Controller 

from daemon import Daemon
import os
import socket
import subprocess
import sys
import time

# read peerlist (peers.conf), returns the peer dictionary
def read_peers():
    try:
        peersconf = open('peers.conf', mode='r')
        peers = {}
        for peer in peersconf.readlines():
            peers[(peer.rstrip('\n').split())[0]] = (peer.rstrip('\n').split())[1]
        return peers
        peersconf.close()
    except:
        print "ERROR: could not open peers.conf, exiting"
        quit()

# read services from identity files (peers/<identity>.conf) and initiate the checks
def read_services(peers):
    for peer in peers:
        try:
            peerconf = open('peers/' + peer + '.conf', mode='r')
        except:
            print "ERROR: could not open peers/" + peer.rstrip('\n') + ".conf as specified in peers.conf"
            quit() 
        for service in peerconf.readlines():
            if os.path.isfile('modules/' + service.rstrip('\n') + '.py'):
                result = subprocess.check_output('modules/' + service.rstrip('\n') + '.py', peers[peer], shell=True)
                return result
            else:
                return send_query(peers[peer], service.rstrip('\n'))
        peerconf.close()

# send queries over the network, returns the reply
def send_query(IP, QUERY):
    print IP + ' -> ' + QUERY
    PORT = 5005
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((IP, PORT))
        s.send(QUERY)
        data = s.recv(BUFFER_SIZE)
        s.close()
    except:
        print "ERROR: could not establish connection to " + str(IP) + ":" + str(PORT)
        return
    return data
read_services(read_peers())
class maindaemon(Daemon):
    def run(self):
        while True:
            time.sleep(1)

if __name__ == "__main__":
    daemon = maindaemon('/tmp/medusa-master.pid')
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
