from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db

class Tiles(db.Model):
    tileId = db.Column(db.String(12), unique=True, primary_key=True)
    munId = db.Column(db.String(5))
    llx = db.Column(db.String(40))
    lly = db.Column(db.String(40))
    urx = db.Column(db.String(40))
    ury = db.Column(db.String(40))

    def __repr__(self):
        return '<Tile {}>'.format(self.tileId)

class Tile_density(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tileDate = db.Column(db.Date)
    tileId = db.Column(db.String(12))
    density = db.Column(db.String(40))
    maleProportion = db.Column(db.String(30))
    
    def __repr__(self):
        return '<Tile Density information {} on {}>'.format(self.tileId, self.tileDate)

class ChartSong(db.model):
    __tablename__ = "chart_song"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    position = db.Column(db.Integer)

    trackId = db.Column(db.String(30))
    countryCode = db.Column(db.String(5))

    spotifySongId = Column(Integer, ForeignKey('spotify_song.id'))
    spotifySong = relationship("SpotifySong", back_populates="chart_song")

class SpotifySong(db.model):
    __tablename__ = "spotify_song"
    id = db.Column(db.Integer, primary_key=True)
    #general info
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    trackId = db.Column(db.String(30))
    spotifyUrl = db.Column(db.String(100))

    # audio features
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    loudness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
    duration_ms = db.Column(db.Integer)

    #relationship
    chart_data = relationship("ChartSong", back_populates="chart_song")