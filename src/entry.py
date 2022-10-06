class Entry (object):
  def __init__(self, artist, album, score, genre) -> None:
    self.artist = artist
    self.album  = album
    self.score  = score
    self.genre  = genre

  
  def __repr__(self) -> str:
    return f'{self.artist} - {self.album} - ({self.genre}): {self.score}'