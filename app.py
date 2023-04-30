import torch
from PIL import Image
import requests
import os
import shutil
import subprocess

import streamlit as st
from streamlit_lottie import st_lottie
from deta import Deta

# Connect to Deta Base with your Data Key
deta = Deta(st.secrets['DETA_KEY'])

image_file = st.file_uploader("Upload a food image", type=['png','jpeg','jpg'])

if image_file is not None:
    file_details = {"FileName": image_file.name,"FileType": image_file.type}

    # Save user uploaded image to Deta database
    db.put(image_file.name, image_file)
    st.success('Image saved successfully')

    # Retrieve image from Deta database
    db.get(image_file.name)
    st.success('Image retrieved successfully')
