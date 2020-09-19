from app import app
from flask import render_template, flash, redirect, url_for, request
from app.models import Tiles, Tile_density
from app import db
from sqlalchemy import select

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Corona Scare Application')

@app.route('/scaremap')
def scaremap():
    # density = Tile_density.query \
    # .filter(Tile_density.maleProportion>0) \
    # .outerjoin(Tiles, Tiles.tileId == Tile_density.tileId) \
    # .all()

    density = db.session.query(Tiles, Tile_density).join(Tile_density, Tiles.tileId == Tile_density.tileId).all()

    density = [{
        "llx" : each[0].llx,
        "lly" : each[0].lly,
        "date" : each[1].tileId,
        "value" : each[1].density
    } for each in density]
    return render_template("scaremap.html", density_data=density)