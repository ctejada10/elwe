import subprocess
import json

def run_applescript(path_to_script):
    result = subprocess.run(['osascript', path_to_script], stdout=subprocess.DEVNULL)
    return result.returncode


class Config():
	def __init__(self) -> None:
		pass


	def _load_site_config(self, config_file_path):
		pass


	def _load_apple_music_config(self, config_file_path):
		pass