class Entry (object):
  def __init__(self, artist, album, score) -> None:
    self.artist = artist
    self.album  = album
    self.score  = score

  
  def __repr__(self) -> str:
    return f'{self.artist} - {self.album}: {self.score}'