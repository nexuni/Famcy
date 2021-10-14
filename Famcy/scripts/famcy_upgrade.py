import subprocess
import pkg_resources
from Famcy import famcy_dir

def main(args):
	famcy_id = args[0]
	script_output = subprocess.check_output(["bash", famcy_dir+"/scripts/bash/"+"relink.sh", famcy_dir, famcy_id]) 
	print("[Famcy Relink] ", script_output.decode())
	print("Famcy version after upgrade: ", pkg_resources.require("Famcy")[0].version)