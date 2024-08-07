import logging
import string

from aggregator_sites.metacritic import Metacritic
from clize import run
from music_services.apple_music import AppleMusic
from tqdm import tqdm
from notifications.pushcut import send_new_album_notification
from os.path import join

from utils.config_utils import ConfigUtils


def main(config_folder_path):
	m  = Metacritic(config_folder_path)
	am = AppleMusic(config_folder_path)
	c  = ConfigUtils(join(config_folder_path, 'metacritic.json'))

	unfiltered_releases = m.get_entries()
	filtered_releases   = filter_releases(unfiltered_releases, m.config)

	result = '"'
	for release in filtered_releases:
		result += release.to_json() + "\n"
	
	result += '"'
	print(result)

	m.set_new_config_values() 


def filter_releases(entries, c):
	filtered_entries = []
	for entry in entries:
		if (entry.genre not in c.ignored_genres
				and entry.score >= c.score_threshold):
			filtered_entries.append(entry)
		else:
			logging.info(f'Album {entry.album} by {entry.artist} was skipped. (Score: {entry.score}; Genre: {entry.genre})')
	
	logging.info(f'Filtered away {len(entries) - len(filtered_entries)} albums.')
	return filtered_entries



if __name__ == "__main__":
	logging.basicConfig(
		filename='/var/log/elwe.log', 
		format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		level=logging.WARN)
	run(main)