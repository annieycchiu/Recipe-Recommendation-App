import torch
from PIL import Image
import requests
import os
import shutil
import subprocess
# import detect

import streamlit as st
from streamlit_lottie import st_lottie
from deta import Deta


# Connect to Deta Base with your Data Key
deta = Deta(st.secrets["DETA_KEY"])

db = deta.Drive("user-images")

col1, col2 = st.columns(2)
image_file = st.file_uploader("Please upload a food image",type=['png','jpeg','jpg'])

if image_file is not None:
    db.put(image_file.name, image_file)
    st.success('Successfully saved image')

    with col1:
        st.write('Original image')
        uploaded_img_path = db.get(image_file.name)
        uploaded_img = Image.open(uploaded_img_path)
        st.image(uploaded_img, use_column_width=True)

    with col2:
        st.write('Inferenced image')
        # if device == 'cuda':
        #     detect(weights="models/best.pt", source=uploaded_img_path, save_txt=True, device=0) 
        # else: 
        #     detect(weights="models/best.pt", source=uploaded_img_path, save_txt=True, device='cpu')

        
