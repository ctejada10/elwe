from datetime import datetime
import json
import requests 
from bs4 import BeautifulSoup
from entry import Entry

class Scrapper (object):
  def _get_contents(self, url):
    headers = {"User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) \
          Gecko/20100101 Firefox/105.0"}
    contents = requests.get(url, headers=headers, allow_redirects=False)

    if contents.status_code != 200:
      # Log here
      raise Exception

    return BeautifulSoup(contents.content, 'html.parser')
  

  def _load_config(self, config_file_path):
    with open (config_file_path, 'r') as config_file:
      config = json.load(config_file)
    
    self.base_url        = config['base_url']
    self.feed_url        = config['feed_url']
    self.last_import     = config['last_import_title']
    self.max_pages       = config['max_pages']
    self.ignored_genres  = config['ignored_genres']
    self.score_threshold = config['score_threshold']

    self.config = config


  def _update_config(self, config_file_path, new_config):
    self.config = new_config
    with open(config_file_path, 'w'):
      json.dump(new_config)