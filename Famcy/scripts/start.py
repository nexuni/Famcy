import subprocess
from Famcy import famcy_dir

def main(args):
	famcy_id = args[0]
	if "--dev" in args:
		_ = subprocess.check_output(["export", "FLASK_ENV=development"]) 
	_ = subprocess.check_output(["bash", famcy_dir+"/scripts/bash/"+"run.sh", famcy_dir, famcy_id]) 