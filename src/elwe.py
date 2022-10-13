from clize import run
from metacritic import Metacritic

def main(config_path):
  m = Metacritic(config_path)
  filtered_releases = filter_releases(m.get_entries(), m.config)
  for release in filtered_releases:
    print(release.to_json())


def filter_releases(entries, config):
  filtered_entries = []
  for entry in entries:
    if entry.genre not in config['ignored_genres'] and entry.score >= config['score_threshold']:
      filtered_entries.append(entry)
  
  return filtered_entries



if __name__ == "__main__":
  run(main)