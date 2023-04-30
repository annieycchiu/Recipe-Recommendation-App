import os

from deta import Deta
from dotenv import load_dotenv

DETA_KEY = 'b0mwg57zwdt_cwbFheLqscgazkCnk9AcX6Kfn3eTNYBW'

deta = Deta(DETA_KEY)

db = deta.drive('user-images')