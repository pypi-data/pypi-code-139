from skyway import *

nmap = NodeMap()
print("\n" + tabulate([node.values() for node in nmap.nodes.values()], headers=nmap.cols) + "\n")

import sys

if "--update" in sys.argv:
  nmap.dump_hosts()
