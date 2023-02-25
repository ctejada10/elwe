from clize import run
from tqdm import tqdm
from metacritic import Metacritic
from apple_music import AppleMusic
import logging

def main(config_folder_path):
  m  = Metacritic(config_folder_path)
  am = AppleMusic(config_folder_path)

  unfiltered_releases = m.get_entries()
  filtered_releases   = filter_releases(unfiltered_releases, m.config)

  for release in (pbar:= tqdm(filtered_releases)):
    pbar.set_description(f'Adding {release.album} by {release.artist} to library.')

    album_id = am.search_album(release.album, release.artist)
    if album_id is not None:
      am.add_album_to_library(album_id)
  
  print(f'Added {len(filtered_releases)} albums to the library.')


def filter_releases(entries, config):
  filtered_entries = []
  for entry in entries:
    if entry.genre not in config['ignored_genres'] and entry.score >= config['score_threshold']:
      filtered_entries.append(entry)
  
  return filtered_entries



if __name__ == "__main__":
  logging.basicConfig(level=logging.WARN)
  run(main)