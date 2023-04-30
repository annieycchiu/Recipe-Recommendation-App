import torch
from PIL import Image
import requests
import os
import shutil
import subprocess

import streamlit as st
from streamlit_lottie import st_lottie
from deta import Deta


# Data to be written to Deta Base
with st.form("form"):
    name = st.text_input("Your name")
    age = st.number_input("Your age")
    submitted = st.form_submit_button("Store in database")


# Connect to Deta Base with your Data Key
deta = Deta(st.secrets['DETA_KEY'])

# Create a new database "example-db"
# If you need a new database, just use another name.
db = deta.Base("example-db")

# If the user clicked the submit button,
# write the data from the form to the database.
# You can store any data you want here. Just modify that dictionary below (the entries between the {}).
if submitted:
    db.put({"name": name, "age": age})

"---"
"Here's everything stored in the database:"
# This reads all items from the database and displays them to your app.
# db_content is a list of dictionaries. You can do everything you want with it.
db_content = db.fetch().items
st.write(db_content)

# # Connect to Deta Base with your Data Key
# deta = Deta(st.secrets['DETA_KEY'])

# image_file = st.file_uploader("Upload a food image", type=['png','jpeg','jpg'])

# if image_file is not None:
#     file_details = {"FileName": image_file.name,"FileType": image_file.type}

#     # Save user uploaded image to Deta database
#     db.put(image_file.name, image_file)
#     st.success('Image saved successfully')

#     # Retrieve image from Deta database
#     db.get(image_file.name)
#     st.success('Image retrieved successfully')
