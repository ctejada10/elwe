import subprocess

def run_applescript(path_to_script):
	result = subprocess.run(['osascript', path_to_script], stdout=subprocess.DEVNULL)
	return result.returncode