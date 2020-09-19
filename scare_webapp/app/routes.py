from app import app
from flask import render_template, flash, redirect, url_for, request
from app.models import Tiles, Tile_density
from app import db

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Corona Scare Application')

@app.route('/scaremap')
def scaremap():
    density = Tile_density.query.filter(and_(Tile_density.maleProportion>0, Tile_density.munId==261)).all()
    return render_template("scaremap.html", density_data=density)