#!/usr/bin/env python

# module for peers, checks disk space left on 'MOUNTPOINT'

# UNFINISHED

import subprocess
import sys

WARN = 90
CRIT = 95
MOUNTPOINT = "/"

data = subprocess.check_output(['df', MOUNTPOINT])
data2 = data.split('\n')
data3 = data2[len(data2) - 2]

data4 = data3.split(' ')[7]
print data3

sys.exit(0)
