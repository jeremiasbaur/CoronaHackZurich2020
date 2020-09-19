from app import app, db
from app.models import Tiles, Tile_density

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Tiles': Tiles, 'Tile_density': Tile_density}
