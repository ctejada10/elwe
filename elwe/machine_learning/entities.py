class Song(object):
	def __init__(self, song_tile, song_length, 
	      play_count, is_liked, is_disliked) -> None:
		self.song_title  = song_tile
		self.song_length = song_length
		self.play_count  = play_count
		self.is_liked    = is_liked
		self.is_disliked = is_disliked

	
	def __str__(self):
		return self.song_title


	def __repr__(self):
		return self.__str__()
	


class Artist(object):
	def __init__(self, artist_name) -> None:
		self.artist_name = artist_name
	

	def __str__(self):
		return self.artist_name



class Album(object):
	def __init__(self, album_name, artist, songs, genre) -> None:
		self.album_name = album_name
		self.artist     = artist
		self.songs      = songs
		self.score      = self._calculate_album_score()
		self.genre      = genre


	def _calculate_album_score(self):
		# Liked songs are a x2 bump. Disliked songs are a -x2.
		score = 0
		for song in self.songs:
			score += 1 if song.is_liked else -5 if song.is_disliked else 0
		
		score = score / float(len(self.songs))
		return score


	def __str__(self):
		return f'''Album name: {self.album_name}\n
						Album artist: {self.artist}\n
						Songs: {self.songs}
						Genre: {self.genre}
						Score: {self.score}'''


	def _get_album_genre(self):
		pass