from clize import run
from metacritic import Metacritic
from apple_music import AppleMusic

def main(config_folder_path):
  m  = Metacritic(config_folder_path)
  am = AppleMusic(config_folder_path)
  filtered_releases = filter_releases(m.get_entries(), m.config)
  for release in filtered_releases:
    id = am.search_album(release.album, release.artist)
    am.add_album_to_library(id)



def filter_releases(entries, config):
  filtered_entries = []
  for entry in entries:
    if entry.genre not in config['ignored_genres'] and entry.score >= config['score_threshold']:
      filtered_entries.append(entry)
  
  return filtered_entries



if __name__ == "__main__":
  run(main)