import platform
from datetime import datetime
from shutil import move

import pandas as pd
import requests
from utils.apple_script_utils import run_applescript


def load_library_data(self, path_to_applescript='get_library_info.scpt'):
	time_since_last_import = datetime.now() - self.last_import_date
	if time_since_last_import.days > 30:
		if platform.system() == 'Darwin':
			c = run_applescript(path_to_applescript)
			if c == 0:
				move('/Users/ctejada/Desktop/data.csv', '../data/data.csv')
				self._update_config('last_import_date', datetime.now().strftime('%Y/%m/%d'))
		else:
			status = f'It has been {datetime.now() - self.last_import_date} days since the library was updated in Elwë.'
			r = requests.post(
				'https://api.pushcut.io/HwnjkzpA86ntxL6NxPnS6/notifications/Update%20library%20data%20file', 
				json={'text': status})

	return pd.read_csv('../data/data.csv', 
											header=None, 
											delimiter='|', 
											names=['song_name', 
														'artist_name', 
														'album_name', 
														'play_count', 
														'is_loved', 
														'is_disliked', 
														'album_genre', 
														'song_length'])