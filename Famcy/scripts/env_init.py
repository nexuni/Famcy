import subprocess
from Famcy import FManager

def main(args):
	famcy_id = args[0]
	init_script_output = subprocess.check_output(["bash", FManager.main+"/scripts/bash/"+"init.sh", famcy_id]) 
	print("[Famcy Init] ", init_script_output.decode())