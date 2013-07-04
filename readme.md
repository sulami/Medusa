### WARNING: As of right now, Medusa is not ready for productional use. It is close to feature complete, but barely tested and not at all fool-proof. Also, there is no fluff yet, meaning init-scripts, systemd-services and proper settings.

# Medusa

Medusa is a distributed network monitoring tool with focus on easy configuration and management. It is entrirely written in Python, Plugins can be written in any language and it should also work with all common nagios/icinga-plugins. In the near future, there will be a status-website generator similar to munin.

## What do I need?

So far nothing besides a simple Python 2 installation. There are not that many plugins included, as I focus on the main program for now. Nagios plugins should work, but have to be copied to the "modules"-directory.

## What does it look like?

The repo contains three main folders, master, peer and mswo. In master are the files needed for the master which queries the peers and presents the results. The folder structure looks like this:

    master
    |-modules
    | \-<all local modules>
    |-peers
    | \-<all peer configs>
    |-master
    |-daemon.py
    \-peers.conf

    peer
    |-modules
    | \-<all remote modules>
    |-modules.enabled
    |-daemon.py
    \-peer
    
    mswo
    |-web
    | |-stylesheet.css
    | \-index.html
    |-daemon.py
    \-mswo

Depending on the type of check, Medusa will check from the master or send a query to the peer, sends back the results. When a local module for a check is present, the check from the master will be prefered. Mswo (the medusa simple website output) is separate and will act as a separate daemon to parse the text output to a html-file for remote (and local) viewing. If you want to, you can write your own output parser as well.

## Now what do I do?

You will edit peers.conf and enter a list of peers in the format "hostname ip", where hostname only serves as an identifier and does not have to match the actual hostname.
Then you need to write a ./peers/<hostname>.conf for every peer in peers.conf, in which you define the checks to make. The checknames are all capital and the same as the names of the corrosponding module, so PING.py would look for ./modules/PING.py and use it, or, if PING.py does not exist, send a query for PING.py to the peer (which would be pointless). The peer always uses it's own modules and sends back either a result or an error message.
At last, add the name of the check into modules.enabled on the peer-side, one per line. This prevents blackhats sending queries for potentially malicious executables by using a simple whitelist.Also, open port 5006.

## Expanding

The nature of Medusa is modular, so you can easily write your own modules. Right now, modules can be written in any language, but have to print the output to stdout and exit with sys.exit(0) (return zero to the shell). Using the prefixes OK, WARNING, CRITICAL and ERROR, followed by " - ", are recommended for a nicer output, interpreting results will be done by the respective plugins.
