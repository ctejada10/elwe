# from utils import run_applescript
import json
from urllib.parse import quote_plus as encode
import requests
from os.path import join
import logging
from datetime import datetime
from utils.config_utils import ConfigUtils

class AppleMusic():
	def __init__(self, config_folder_path) -> None:
		self.config_file_path = join(config_folder_path, 'apple_music.json')
		self._load_config()


	def _load_config(self):
		with open(self.config_file_path, 'r') as f:
			c = f.read()
			j = json.loads(c)
			self._build_headers(j)
			if j['last_import_date']:
				self.last_import_date = datetime.strptime(j['last_import_date'], '%Y/%m/%d')
			else:
				self.last_import_date = datetime(1970, 1, 1)
	

	def _build_headers(self, json):
			self.headers = {
				'Authorization': 'Bearer ' + json['developer_token'],
				'Music-User-Token': json['music_user_token']
			}
	

	def _update_config(self, field, value):
		with open(self.config_file_path, 'r') as f:
			c = f.read()
			j = json.loads(c)
		
		j[field] = value

		with open(self.config_file_path, 'w') as f:
			json.dump(j, f)
		


	def search_album(self, album, artist):
		url = 'https://api.music.apple.com/v1/catalog/us/search?types=albums&term='
		url = url + encode(artist + ' ' + album)
		try:
			r = requests.get(url, headers=self.headers)
			r.raise_for_status()
			r = r.json()['results']
			if 'albums' not in r.keys():
				logging.warn(f'Album "{album}" by {artist} was not found')
				return None
			album_id = r['albums']['data'][0]['id']
			return album_id
		except requests.exceptions.HTTPError as e:
			logging.error(e)
			raise SystemExit(e)


	def add_album_to_library(self, album_id):
		url = 'https://api.music.apple.com/v1/me/library?ids[albums]='
		url = url + encode(album_id)
		try:
			r = requests.post(url, headers=self.headers)
			r.raise_for_status()
		except requests.exceptions.HTTPError as e:
			logging.error(e.strerror)
			raise SystemExit(e)
	




if __name__ == '__main__':
	am = AppleMusic('../config')