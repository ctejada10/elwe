import json
from urllib.parse import quote_plus as encode
import requests

class AppleMusic():
  def __init__(self, config_path="") -> None:
    self._build_headers(config_path)
  

  def _build_headers(self, auth_things):
    with open('../config/apple_music.json', 'r') as f:
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