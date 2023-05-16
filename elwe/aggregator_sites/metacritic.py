import logging
from datetime import datetime
from os.path import join

from .entry import Entry
from .scrapper import Scrapper


class Metacritic (Scrapper):
	def __init__(self, config_folder_path) -> None:
		self.config_path = join(config_folder_path)
		self._load_config(join(self.config_path, 'metacritic.json'))


	def get_entries(self):
		self.albums = list()
		last_import = True
		i           = 0

		while(last_import and i <= self.config.max_pages):
			url  = self.config.base_url + self.config.feed_url + str(i)
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

				if (t == self.config.last_import_title):
					last_import = False
					break

				self.albums.append(Entry(a, t, s, g, d))

			i += 1
			
		return self.albums
	
	
	def set_new_config_values(self):
		if len(self.albums):
			self.config.update_config_value('last_import_title', self.albums[0].album)



	def _get_genre(self, album_tag):
		href       = album_tag.attrs['href'][1:]
		url        = self.config.base_url + href
		album_page = self._get_contents(url)

		if len(album_page):
			genre = album_page.find('li', class_='product_genre').find('span', class_='data').get_text()
			return genre

if __name__ == '__main__':
	m = Metacritic('config/metacritic.json')
	print(m.get_entries())