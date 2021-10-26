import subprocess
import pkg_resources
from Famcy import FManager

def main(args):
	famcy_id = args[0]
	script_output = subprocess.check_output(["bash", FManager.main+"/scripts/bash/"+"upgrade.sh", FManager.main, famcy_id]) 
	print("[Famcy Upgrade] ", script_output.decode())
	print("Famcy version after upgrade: ", pkg_resources.require("Famcy")[0].version)