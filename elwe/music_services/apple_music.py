import logging
from os.path import join
from urllib.parse import quote_plus as encode

import requests
from utils.config_utils import ConfigUtils


class AppleMusic():
	def __init__(self, config_file_path) -> None:
		self.config_file_path = join(config_file_path)
		self._load_config()


	def _load_config(self):
		self.config = ConfigUtils(self.config_file_path)
		self._build_headers()


	def _build_headers(self):
			self.headers = {
				'Authorization': 'Bearer ' + self.config.developer_token,
				'Music-User-Token': self.config.music_user_token
			}
	

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
	am = AppleMusic('config/apple_music.json')
	print(am.search_album('22, A Million', 'Bon Iver'))