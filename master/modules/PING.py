#!/usr/bin/env python

# ping module for use on the master

import subprocess
import sys

subprocess.check_output('/bin/ping ' + sys.argv[0])

sys.exit(0)
