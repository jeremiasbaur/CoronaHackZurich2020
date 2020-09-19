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

class ChartSong(db.Model):
    __tablename__ = "chart_song"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    position = db.Column(db.Integer)

    trackId = db.Column(db.String(30))
    countryCode = db.Column(db.String(5))

    spotifySongId = db.Column(db.Integer, ForeignKey('spotify_song.id'))
    spotifySong = db.relationship("SpotifySong", back_populates="chartSong")

class SpotifySong(db.Model):
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
    chartSong = db.relationship("ChartSong", back_populates="spotifySong")

class SwitzerlandPopulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Code = db.Column(db.String(10))
    KTNR = db.Column(db.String(20))
    pop_1971 = db.Column(db.Integer)
    pop_1972 = db.Column(db.Integer)
    pop_1973 = db.Column(db.Integer)
    pop_1974 = db.Column(db.Integer)
    pop_1975 = db.Column(db.Integer)
    pop_1976 = db.Column(db.Integer)
    pop_1977 = db.Column(db.Integer)
    pop_1978 = db.Column(db.Integer)
    pop_1979 = db.Column(db.Integer)
    pop_1980 = db.Column(db.Integer)
    pop_1981 = db.Column(db.Integer)
    pop_1982 = db.Column(db.Integer)
    pop_1983 = db.Column(db.Integer)
    pop_1984 = db.Column(db.Integer)
    pop_1985 = db.Column(db.Integer)
    pop_1986 = db.Column(db.Integer)
    pop_1987 = db.Column(db.Integer)
    pop_1988 = db.Column(db.Integer)
    pop_1989 = db.Column(db.Integer)
    pop_1990 = db.Column(db.Integer)
    pop_1991 = db.Column(db.Integer)
    pop_1992 = db.Column(db.Integer)
    pop_1993 = db.Column(db.Integer)
    pop_1994 = db.Column(db.Integer)
    pop_1995 = db.Column(db.Integer)
    pop_1996 = db.Column(db.Integer)
    pop_1997 = db.Column(db.Integer)
    pop_1998 = db.Column(db.Integer)
    pop_1999 = db.Column(db.Integer)
    pop_2000 = db.Column(db.Integer)
    pop_2001 = db.Column(db.Integer)
    pop_2002 = db.Column(db.Integer)
    pop_2003 = db.Column(db.Integer)
    pop_2004 = db.Column(db.Integer)
    pop_2005 = db.Column(db.Integer)
    pop_2006 = db.Column(db.Integer)
    pop_2007 = db.Column(db.Integer)
    pop_2008 = db.Column(db.Integer)
    pop_2009 = db.Column(db.Integer)
    pop_2010 = db.Column(db.Integer)
    male_1971 = db.Column(db.Integer)
    male_1972 = db.Column(db.Integer)
    male_1973 = db.Column(db.Integer)
    male_1974 = db.Column(db.Integer)
    male_1975 = db.Column(db.Integer)
    male_1976 = db.Column(db.Integer)
    male_1977 = db.Column(db.Integer)
    male_1978 = db.Column(db.Integer)
    male_1979 = db.Column(db.Integer)
    male_1980 = db.Column(db.Integer)
    male_1981 = db.Column(db.Integer)
    male_1982 = db.Column(db.Integer)
    male_1983 = db.Column(db.Integer)
    male_1984 = db.Column(db.Integer)
    male_1985 = db.Column(db.Integer)
    male_1986 = db.Column(db.Integer)
    male_1987 = db.Column(db.Integer)
    male_1988 = db.Column(db.Integer)
    male_1989 = db.Column(db.Integer)
    male_1990 = db.Column(db.Integer)
    male_1991 = db.Column(db.Integer)
    male_1992 = db.Column(db.Integer)
    male_1993 = db.Column(db.Integer)
    male_1994 = db.Column(db.Integer)
    male_1995 = db.Column(db.Integer)
    male_1996 = db.Column(db.Integer)
    male_1997 = db.Column(db.Integer)
    male_1998 = db.Column(db.Integer)
    male_1999 = db.Column(db.Integer)
    male_2000 = db.Column(db.Integer)
    male_2001 = db.Column(db.Integer)
    male_2002 = db.Column(db.Integer)
    male_2003 = db.Column(db.Integer)
    male_2004 = db.Column(db.Integer)
    male_2005 = db.Column(db.Integer)
    male_2006 = db.Column(db.Integer)
    male_2007 = db.Column(db.Integer)
    male_2008 = db.Column(db.Integer)
    male_2009 = db.Column(db.Integer)
    male_2010 = db.Column(db.Integer)
    female_1971 = db.Column(db.Integer)
    female_1972 = db.Column(db.Integer)
    female_1973 = db.Column(db.Integer)
    female_1974 = db.Column(db.Integer)
    female_1975 = db.Column(db.Integer)
    female_1976 = db.Column(db.Integer)
    female_1977 = db.Column(db.Integer)
    female_1978 = db.Column(db.Integer)
    female_1979 = db.Column(db.Integer)
    female_1980 = db.Column(db.Integer)
    female_1981 = db.Column(db.Integer)
    female_1982 = db.Column(db.Integer)
    female_1983 = db.Column(db.Integer)
    female_1984 = db.Column(db.Integer)
    female_1985 = db.Column(db.Integer)
    female_1986 = db.Column(db.Integer)
    female_1987 = db.Column(db.Integer)
    female_1988 = db.Column(db.Integer)
    female_1989 = db.Column(db.Integer)
    female_1990 = db.Column(db.Integer)
    female_1991 = db.Column(db.Integer)
    female_1992 = db.Column(db.Integer)
    female_1993 = db.Column(db.Integer)
    female_1994 = db.Column(db.Integer)
    female_1995 = db.Column(db.Integer)
    female_1996 = db.Column(db.Integer)
    female_1997 = db.Column(db.Integer)
    female_1998 = db.Column(db.Integer)
    female_1999 = db.Column(db.Integer)
    female_2000 = db.Column(db.Integer)
    female_2001 = db.Column(db.Integer)
    female_2002 = db.Column(db.Integer)
    female_2003 = db.Column(db.Integer)
    female_2004 = db.Column(db.Integer)
    female_2005 = db.Column(db.Integer)
    female_2006 = db.Column(db.Integer)
    female_2007 = db.Column(db.Integer)
    female_2008 = db.Column(db.Integer)
    female_2009 = db.Column(db.Integer)
    female_2010 = db.Column(db.Integer)
    ch_1971 = db.Column(db.Integer)
    ch_1972 = db.Column(db.Integer)
    ch_1973 = db.Column(db.Integer)
    ch_1974 = db.Column(db.Integer)
    ch_1975 = db.Column(db.Integer)
    ch_1976 = db.Column(db.Integer)
    ch_1977 = db.Column(db.Integer)
    ch_1978 = db.Column(db.Integer)
    ch_1979 = db.Column(db.Integer)
    ch_1980 = db.Column(db.Integer)
    ch_1981 = db.Column(db.Integer)
    ch_1982 = db.Column(db.Integer)
    ch_1983 = db.Column(db.Integer)
    ch_1984 = db.Column(db.Integer)
    ch_1985 = db.Column(db.Integer)
    ch_1986 = db.Column(db.Integer)
    ch_1987 = db.Column(db.Integer)
    ch_1988 = db.Column(db.Integer)
    ch_1989 = db.Column(db.Integer)
    ch_1990 = db.Column(db.Integer)
    ch_1991 = db.Column(db.Integer)
    ch_1992 = db.Column(db.Integer)
    ch_1993 = db.Column(db.Integer)
    ch_1994 = db.Column(db.Integer)
    ch_1995 = db.Column(db.Integer)
    ch_1996 = db.Column(db.Integer)
    ch_1997 = db.Column(db.Integer)
    ch_1998 = db.Column(db.Integer)
    ch_1999 = db.Column(db.Integer)
    ch_2000 = db.Column(db.Integer)
    ch_2001 = db.Column(db.Integer)
    ch_2002 = db.Column(db.Integer)
    ch_2003 = db.Column(db.Integer)
    ch_2004 = db.Column(db.Integer)
    ch_2005 = db.Column(db.Integer)
    ch_2006 = db.Column(db.Integer)
    ch_2007 = db.Column(db.Integer)
    ch_2008 = db.Column(db.Integer)
    ch_2009 = db.Column(db.Integer)
    ch_2010 = db.Column(db.Integer)
    foreign_1971 = db.Column(db.Integer)
    foreign_1972 = db.Column(db.Integer)
    foreign_1973 = db.Column(db.Integer)
    foreign_1974 = db.Column(db.Integer)
    foreign_1975 = db.Column(db.Integer)
    foreign_1976 = db.Column(db.Integer)
    foreign_1977 = db.Column(db.Integer)
    foreign_1978 = db.Column(db.Integer)
    foreign_1979 = db.Column(db.Integer)
    foreign_1980 = db.Column(db.Integer)
    foreign_1981 = db.Column(db.Integer)
    foreign_1982 = db.Column(db.Integer)
    foreign_1983 = db.Column(db.Integer)
    foreign_1984 = db.Column(db.Integer)
    foreign_1985 = db.Column(db.Integer)
    foreign_1986 = db.Column(db.Integer)
    foreign_1987 = db.Column(db.Integer)
    foreign_1988 = db.Column(db.Integer)
    foreign_1989 = db.Column(db.Integer)
    foreign_1990 = db.Column(db.Integer)
    foreign_1991 = db.Column(db.Integer)
    foreign_1992 = db.Column(db.Integer)
    foreign_1993 = db.Column(db.Integer)
    foreign_1994 = db.Column(db.Integer)
    foreign_1995 = db.Column(db.Integer)
    foreign_1996 = db.Column(db.Integer)
    foreign_1997 = db.Column(db.Integer)
    foreign_1998 = db.Column(db.Integer)
    foreign_1999 = db.Column(db.Integer)
    foreign_2000 = db.Column(db.Integer)
    foreign_2001 = db.Column(db.Integer)
    foreign_2002 = db.Column(db.Integer)
    foreign_2003 = db.Column(db.Integer)
    foreign_2004 = db.Column(db.Integer)
    foreign_2005 = db.Column(db.Integer)
    foreign_2006 = db.Column(db.Integer)
    foreign_2007 = db.Column(db.Integer)
    foreign_2008 = db.Column(db.Integer)
    foreign_2009 = db.Column(db.Integer)
    foreign_2010 = db.Column(db.Integer)