from clize import run
from tqdm import tqdm
from metacritic import Metacritic
from apple_music import AppleMusic
import logging, string
import requests

def main(config_folder_path):
  m  = Metacritic(config_folder_path)
  am = AppleMusic(config_folder_path)

  unfiltered_releases = m.get_entries()
  filtered_releases   = filter_releases(unfiltered_releases, m.config)

  for release in filtered_releases:
    album_id = am.search_album(release.album.translate(str.maketrans('', '', string.punctuation)), 
                               release.artist.translate(str.maketrans('', '', string.punctuation)))
    if album_id is not None:
      am.add_album_to_library(album_id)
  
  status = f'Added {len(filtered_releases)} albums to the library.'
  r = requests.post('https://api.pushcut.io/HwnjkzpA86ntxL6NxPnS6/notifications/New%20albums%20added', 
                    json={'text': status})


def filter_releases(entries, config):
  filtered_entries = []
  for entry in entries:
    if entry.genre not in config['ignored_genres'] and entry.score >= config['score_threshold']:
      filtered_entries.append(entry)
  
  return filtered_entries



if __name__ == "__main__":
  logging.basicConfig(filename='/var/log/elwe.log', level=logging.WARN)
  run(main)