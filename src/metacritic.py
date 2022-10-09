from scrapper import Scrapper
from datetime import datetime
from entry import Entry


class Metacritic (Scrapper):
  def __init__(self, config_path) -> None:
    self._load_config(config_path)


  def get_entries(self):
    albums      = list()
    last_import = True
    i           = 0

    while(last_import and i <= self.max_pages):
      url  = self.base_url + self.feed_url + str(i)
      soup = self._get_contents(url)

      album_titles  = soup.find_all('a', class_='title')
      artist_names  = soup.find_all('div', class_= 'artist')
      album_scores  = soup.find_all('div', class_='clamp-metascore')
      release_dates = soup.find_all('div', class_='clamp-details')

      for album, artist, score, date in zip(album_titles, artist_names, album_scores, release_dates):
        t = album.find('h3').get_text()
        a = artist.get_text().strip()[3:]
        d = datetime.strptime(date.find('span').get_text(), '%B %d, %Y')
        s = int(score.find('div', class_='metascore_w').get_text())
        g = self._get_genre(album)

        if (t == self.last_import):
          last_import = False
          break

        albums.append(Entry(a, t, s, g, d))

      i += 1
      
    # if len(albums):
      # self._update_config('last_import_title', albums[-1].album)

    return albums


  def _get_genre(self, album_tag):
    href       = album_tag.attrs['href']
    url        = self.base_url + href
    album_page = self._get_contents(url)

    genre = album_page.find('li', class_='product_genre').find('span', class_='data').get_text()
    return genre