from scrapper import Scrapper
from datetime import datetime
from entry import Entry
from os.path import join
import logging


class Metacritic (Scrapper):
  def __init__(self, config_folder_path) -> None:
    self.config_path = join(config_folder_path, 'metacritic.json')
    self._load_config(self.config_path)


  def get_entries(self):
    albums      = list()
    last_import = True
    i           = 0

    print('Scrubbing Metacritic for new releases.')
    while(last_import and i <= self.config['max_pages']):
      url  = self.config['base_url'] + self.config['feed_url'] + str(i)
      soup = self._get_contents(url)

      album_titles  = soup.find_all('a', class_='title')
      artist_names  = soup.find_all('div', class_= 'artist')
      album_scores  = soup.find_all('div', class_='clamp-metascore')
      release_dates = soup.find_all('div', class_='clamp-details')

      for album, artist, score, date in zip(album_titles, artist_names, album_scores, release_dates):
        try:
          t = album.find('h3').get_text()
          a = artist.get_text().strip()[3:]
          d = datetime.strptime(date.find('span').get_text(), '%B %d, %Y')
          s = int(score.find('div', class_='metascore_w').get_text())
          g = self._get_genre(album)
        except:
          continue

        if (t == self.config['last_import_title']):
          last_import = False
          break

        # logging.info(f'Added {t} by {a} to the queue.')
        albums.append(Entry(a, t, s, g, d))

      i += 1
      
    if len(albums):
      self.config['last_import_title'] = albums[0].album
      self._update_config(self.config_path, self.config)

    return albums


  def _get_genre(self, album_tag):
    href       = album_tag.attrs['href'][1:]
    url        = self.config['base_url'] + href
    album_page = self._get_contents(url)

    if len(album_page):
      genre = album_page.find('li', class_='product_genre').find('span', class_='data').get_text()
      return genre

if __name__ == '__main__':
  m = Metacritic('../config/metacritic.json')
  m.get_entries()