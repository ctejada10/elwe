from clize import run
from metacritic import Metacritic

def main(config_path):
  m = Metacritic(config_path)
  filtered_releases = filter_releases(m.get_entries(), m.config)
  for release in filtered_releases:
    print(release.to_json())


def filter_releases(entries, config):
  return [x for x in entries if x.genre not in config['ignored_genres'] and x.score >= config['score_threshold']]


if __name__ == "__main__":
  run(main)