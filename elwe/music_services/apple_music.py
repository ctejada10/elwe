import logging
from os.path import join, dirname
from urllib.parse import quote_plus as encode
from notifications.pushcut import send_error_notification

import requests
from utils.config_utils import ConfigUtils


class AppleMusic():
	"""
    A class for interacting with the Apple Music API to search for albums and add them to the user's library.

    Args:
        config_file_path (str): Path to the configuration file for Apple Music API credentials.

    Attributes:
        config_file_path (str): Path to the configuration file.
        config (ConfigUtils): An instance of ConfigUtils for handling configuration.
        headers (dict): HTTP headers for API requests.

    Methods:
        search_album(artist: str, album: str) -> str:
            Retrieve the album ID from the Apple Music API for a given artist and album name.
        
        add_album_to_library(album_id: str) -> None:
            Add an album to the user's Apple Music library using the provided album ID.
    """
	def __init__(self, config_file_path: str) -> None:
		self.config_file_path = join(config_file_path, 'apple_music.json')
		self._load_config()


	def _load_config(self):
		self.config = ConfigUtils(self.config_file_path)
		self._build_headers()


	def _build_headers(self):
			self.headers = {
				'Authorization': 'Bearer ' + self.config.developer_token,
				'Music-User-Token': self.config.music_user_token
			}
	

	def search_album(self, artist: str, album: str) -> str:
		"""
    Retrieve the album ID from the Apple Music API for a given artist and album
    name.

    Args:
        artist (str): The name of the artist.
        album (str): The name of the album.

    Returns:
        str: The ID of the requested album, or None if not found.

    Raises:
        SystemExit: If an HTTP error occurs during the API request.
    """
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
			send_error_notification(join(dirname(self.config_file_path), 'pushcut.json'), 'searching albums')
			raise SystemExit(e)


	def add_album_to_library(self, album_id: str) -> None:
		"""
    Add an album to the user's Apple Music library using the provided album ID.

    Args:
        album_id (str): The ID of the album to be added to the library.

    Raises:
        SystemExit: If an HTTP error occurs during the API request.
    """
		url = 'https://api.music.apple.com/v1/me/library?ids[albums]='
		url = url + encode(album_id)
		try:
			r = requests.post(url, headers=self.headers)
			r.raise_for_status()
		except requests.exceptions.HTTPError as e:
			logging.error(e.strerror)
			send_error_notification(join(dirname(self.config_file_path), 'pushcut.json'), 'adding albums')
			raise SystemExit(e)
	




if __name__ == '__main__':
	am = AppleMusic('config/apple_music.json')
	print(am.search_album('22, A Million', 'Bon Iver'))