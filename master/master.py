#!/usr/bin/env python

# Medusa Master Controller 

from daemon import Daemon
import os
import socket
import subprocess
import sys
import time

INST_PATH = "/home/sulami/medusa/master/"
CHECK_INTERVAL = 300
LOG_PATH = "/var/log/medusa-master.log"
OUT_PATH = "/home/sulami/medusa.out"

#
# TODO: Proper output to somewhere, analyzing prefixes
#

# writes events to the log
def write_log(data):
    with open(LOG_PATH, mode='a+') as logfile:
        logfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + " - " + data + "\n")
    logfile.close()

# read peerlist (peers.conf), returns the peer dictionary
def read_peers():
    try:
        peersconf = open(INST_PATH + 'peers.conf', mode='r')
        peers = {}
        for peer in peersconf.readlines():
            peers[(peer.rstrip('\n').split())[0]] = (peer.rstrip('\n').split())[1]
        peersconf.close()
        return peers
    except:
        write_log("ERROR: could not open peers.conf, exiting")
        sys.exit(1)

# interprets the results coming from plugins, returns int values
def interpret(result):
    resultstatus = (result.split(" - "))[0]
    if 'OK' in resultstatus:
        return 0
    elif 'WARNING' in resultstatus:
        return 1
    elif 'CRITICAL' in resultstatus:
        return 2
    elif 'ERROR' in resultstatus:
        return 3
    else:
        return 0

# send queries over the network, returns the reply
def send_query(IP, QUERY):
    PORT = 5006
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((IP, PORT))
        s.send(QUERY)
        data = s.recv(BUFFER_SIZE)
    except:
        write_log("ERROR: could not establish connection to " + str(IP) + ":" + str(PORT))
        return "NETWORK ERROR, CHECK LOG"
    s.close()
    return data

# write output into a log-like file
def write_out(host, query, data):
    try:
        with open(OUT_PATH, mode='a+') as output_file:
            output_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + " - " + host + " - " + query + " - " + data)
        output_file.close()
    except:
        write_log("ERROR: could not output data to " + OUT_PATH)

# read services from identity files (peers/<identity>.conf) and initiate the checks
def read_services(peers):
    for peer in peers:
        try:
            peerconf = open(INST_PATH + 'peers/' + peer + '.conf', mode='r')
        except:
            write_log("ERROR: could not open peers/" + peer.rstrip('\n') + ".conf as specified in peers.conf")
            quit() 
        for service in peerconf.readlines():
            nservice = service.rstrip()
            if os.path.isfile(INST_PATH + 'modules/' + nservice):
                try:
                    result = subprocess.check_output([INST_PATH + 'modules/' + nservice, peers[peer]])
                    write_out(peer, nservice, result)
                except:
                    write_log("ERROR: failed to run local module " + nservice)
            else:
                write_out(peer, nservice, send_query(peers[peer], nservice))
        peerconf.close()
"""   
print interpret("DISK OK - free space...")
read_services(read_peers())
"""

# Generic Unix daemon code, courtesy of Sander Marechal, http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class MyDaemon(Daemon):
    def run(self):
        while True:
            read_services(read_peers())
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/medusa-master.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            write_log("Daemon started")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            write_log("Daemon stopped")
        elif 'restart' == sys.argv[1]:
            daemon.restart()
            write_log("Daemon restarted")
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
"""
