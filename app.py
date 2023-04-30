import torch
from PIL import Image
import requests
import os
import shutil
import subprocess

import streamlit as st
from streamlit_lottie import st_lottie
import database as db

st.write('Hello world!')
cwd = os.getcwd()
st.write(cwd)


image_file = st.file_uploader("Please upload a food image",type=['png','jpeg','jpg'])

if image_file is not None:
    file_details = {"FileName": image_file.name,"FileType": image_file.type}

    st.write(file_details)

    img = Image.open(image_file)
    st.write('Original image')
    st.image(img, use_column_width=False)

    with open(os.path.join('user_uploads', image_file.name), "wb") as f: 
        f.write(image_file.getbuffer())         
        st.success("Saved File")
