import logging
import string

import requests
from aggregator_sites.metacritic import Metacritic
from clize import run
from music_services.apple_music import AppleMusic
from tqdm import tqdm

from utils.utils import Config


def main(config_folder_path):
	m  = Metacritic(config_folder_path)
	am = AppleMusic(config_folder_path)
	c  = Config(config_folder_path)

	unfiltered_releases = m.get_entries()
	filtered_releases   = filter_releases(unfiltered_releases, m.config)

	number_of_albums = 0
	for release in filtered_releases:
		album_id = am.search_album(
			release.album.translate(str.maketrans('', '', string.punctuation)), 
			release.artist.translate(str.maketrans('', '', string.punctuation)))
		if album_id is not None:
			am.add_album_to_library(album_id)
			number_of_albums += 1
	
	if number_of_albums > 0:
		status = f'Added {number_of_albums} albums to the library'
		r = requests.post(
			'https://api.pushcut.io/HwnjkzpA86ntxL6NxPnS6/notifications/New%20albums%20added', 
			json={'text': status})

	m.set_new_config_values() 


def filter_releases(entries, config):
	filtered_entries = []
	for entry in entries:
		if (entry.genre not in config['ignored_genres'] 
				and entry.score >= config['score_threshold']):
			filtered_entries.append(entry)
	
	return filtered_entries



if __name__ == "__main__":
	logging.basicConfig(
		filename='/var/log/elwe.log', 
		format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		level=logging.WARN)
	run(main)