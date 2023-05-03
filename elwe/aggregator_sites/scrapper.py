from datetime import datetime
import json
import requests 
from bs4 import BeautifulSoup
from .entry import Entry

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
    
    self.config = config


  def _update_config(self, config_file_path, new_config):
    with open(config_file_path, 'w') as f:
      json.dump(new_config, f, indent=2)