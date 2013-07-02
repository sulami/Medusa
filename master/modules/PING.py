#!/usr/bin/env python

# ping module for use on the master

import subprocess
import sys

CRIT = 5.0
WARN = 1.0
NOOFPINGS = '3'

# Performing the ping and filtering everything but the last line
data = subprocess.check_output(['ping', '-c', NOOFPINGS, sys.argv[1]])
data2 = data.split('\n')
data3 = data2[len(data2) - 2]

# splitting the numbers
numbers = data3.split(' ')[3]
number = numbers.split('/')

# checking package loss
ploss = data2[len(data2) - 3]
ploss2 = ploss.split(' ')[5]

#check max ping and package loss for status
if ploss2 == '0%':
    if float(number[2]) >= CRIT:
        STATUS = 'CRITICAL'
    elif float(number[2]) >= WARN:
        STATUS = 'WARNING'
    else:
        STATUS = 'OK'
elif ploss2 == '100%':
    STATUS = 'CRITICAL'
else:
    STATUS = 'WARNING'

# print results, exit
print STATUS + " - package loss: " + ploss2 + " " + data3

sys.exit(0)
