#!/usr/bin/env python

# Reads and prints out the loadavg triplet

CRIT = 6.00
WARN = 4.50

import sys

with open('/proc/loadavg', mode='r') as file:
    avg = file.read().split(' ')
if (float(avg[0]) or float(avg[1]) or float(avg[2])) >= CRIT:
    STATUS = "CRITICAL"
elif (float(avg[0]) or float(avg[1]) or float(avg[2])) >= WARN:
    STATUS = "WARNING"
else:
    STATUS = "OK"
print STATUS + " " + avg[0] + " " + avg[1] + " " + avg[2]
sys.exit(0)
