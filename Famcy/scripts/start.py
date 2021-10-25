import subprocess
from Famcy import FManager

def main(args):
	famcy_id = args[0]
	if "--dev" in args:
		_ = subprocess.check_output(["export", "FLASK_ENV=development"]) 
	_ = subprocess.check_output(["bash", FManager.main+"/scripts/bash/"+"run.sh", FManager.main, famcy_id]) 