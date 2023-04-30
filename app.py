import torch
from PIL import Image
import requests
import os
import shutil
import subprocess
# import detect

import streamlit as st
from streamlit_lottie import st_lottie
#from deta import Deta
import s3fs



# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")

content = read_file("streamlit-food-images/test.csv")

# Print results.
for line in content.strip().split("\n"):
    name, pet = line.split(",")
    st.write(f"{name} has a :{pet}:")


# # Connect to Deta Base with your Data Key
# deta = Deta(st.secrets["DETA_KEY"])

# db = deta.Drive("user-images")

# col1, col2 = st.columns(2)
# image_file = st.file_uploader("Please upload a food image",type=['png','jpeg','jpg'])

# if image_file is not None:
#     db.put(image_file.name, image_file)
#     st.success('Successfully saved image')

#     with col1:
#         st.write('Original image')
#         uploaded_img_path = db.get(image_file.name)
#         uploaded_img = Image.open(uploaded_img_path)
#         st.image(uploaded_img, use_column_width=True)

#     with col2:
#         st.write('Inferenced image')
#         # if device == 'cuda':
#         #     detect(weights="models/best.pt", source=uploaded_img_path, save_txt=True, device=0) 
#         # else: 
#         #     detect(weights="models/best.pt", source=uploaded_img_path, save_txt=True, device='cpu')

        
