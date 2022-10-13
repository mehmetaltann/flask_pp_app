from pydoc import cli
import click
from flask.cli import with_appcontext
from .extensions import db
from .models import Musteriler, MusteriSiparis, Siparisler, SiparisUrun, Urunler, UrunTarif, UrunMalzeme, Tarifler, TarifMalzeme, Hammaddeler
from .login.routes import User

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()