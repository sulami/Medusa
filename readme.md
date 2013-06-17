### WARNING: As of right now, Medusa is not ready for productional use. There is only one plugin and the output happens to a simple log.

# Medusa

Medusa is a distributed network monitoring tool with focus on easy configuration and management. It is entrirely written in Python.

## What do I need?

So far nothing besides a simple Python 2 installation.

## What does it look like?

The repo contains two main folders, master and peer. In master are the files needed for the master which queries the peers and presents the results. The folder structure looks like this:

    master
    |-modules
    | \-<all local modules>
    |-peers
    | \-<all peer configs>
    |-master.py
    \-peers.conf

    peer
    |-modules
    | \-<all remote modules>
    |-modules.enabled
    \-peer.py

Depending on the type of check, Medusa will check from the master or send a query to the peer, sends back the results. When a local module for a check is present, the check from the master will be prefered.

## Now what do I do?

You will edit peers.conf and enter a list of peers in the format "hostname ip", where hostname only serves as an identifier and does not have to match the actual hostname.
Then you need to write a ./peers/<hostname>.conf for every peer in peers.conf, in which you define the checks to make. The checknames are all capital and the same as the names of the corrosponding module, so PING would look for ./modules/PING.py and use it, or, if PING.py does not exist, send a query for PING to the peer (which would be pointless). The peer always uses it's own modules and sends back either a result or an error message.
At last, add the name of the check into modules.enabled on the peer-side, one per line. This prevents blackhats sending queries for potentially malicious executables by using a simple whitelist.Also, open port 5006.

## Expanding

The nature of Medusa is modular, so you can easily write your own modules. Right now, modules have to be written in Python 2, print the output to stdout and exit with sys.exit(0). Using the prefixes OK, WARNING, CRITICAL and ERROR are recommended for a nicer output, interpreting results will be done by the respective plugins.
