#!/usr/bin/env python

# ping module for use on the master

import subprocess
import sys

CRIT = 1.0
WARN = 0.5
NOOFPINGS = '3'

# TODO: timeouts

# Performing the ping and filtering everything but the last line
data = subprocess.check_output(['ping', '-c', NOOFPINGS, sys.argv[1]])
data2 = data.split('\n')
data3 = data2[len(data2) -2]

# splitting the numbers
numbers = data3.split(' ')[3]
number = numbers.split('/')

#check max ping for status
if float(number[2]) >= CRIT:
    STATUS = 'CRITICAL'
elif float(number[2]) >= WARN:
    STATUS = 'WARNING'
else:
    STATUS = 'OK'

# print results, exit
print STATUS + " " + data3

sys.exit(0)
