import json
from urllib.parse import quote_plus as encode
import requests
from os.path import join
import logging

class AppleMusic():
  def __init__(self, config_folder_path) -> None:
    self._build_headers(join(config_folder_path, 'apple_music.json'))
  

  def _build_headers(self, config_path):
    with open(config_path, 'r') as f:
      c = f.read()
      j = json.loads(c)
      self.headers = {
        'Authorization': 'Bearer ' + j['developer_token'],
        'Music-User-Token': j['music_user_token']
      }


  def search_album(self, album, artist):
    url = 'https://api.music.apple.com/v1/catalog/us/search?types=albums&term='
    url = url + encode(artist + ' ' + album) 
    r = requests.get(url, headers=self.headers).json()['results']
    if 'albums' not in r.keys():
      logging.warn(f'Album "{album}" by {artist} was not found')
      return None
    album_id = r['albums']['data'][0]['id']
    return album_id


  def add_album_to_library(self, album_id):
    url = 'https://api.music.apple.com/v1/me/library?ids[albums]='
    url = url + encode(album_id)
    r = requests.post(url, headers=self.headers)



if __name__ == '__main__':
  am = AppleMusic()
  id = am.search_album('Food for worms', 'Shame')
  am.add_album_to_library(id)