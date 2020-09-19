from datetime import datetime
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