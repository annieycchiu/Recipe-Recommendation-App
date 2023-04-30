import os
from deta import Deta

deta = Deta(st.secrets['DETA_KEY'])

db = deta.drive('user-images')