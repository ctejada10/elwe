class Entry (object):
	def __init__(self, artist, album, score, genre, release_date) -> None:
		self.artist       = artist
		self.album        = album
		self.score        = score
		self.genre        = genre
		self.release_date = release_date

	
	def __repr__(self) -> str:
		return f'{self.artist} - {self.album} - ({self.genre}): {self.score}'
	

	def to_json(self) -> str:
		return '{"artist": "%s", "album": "%s"}' % (self.artist, self.album)