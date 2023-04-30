import torch
from PIL import Image
import requests
import os
import shutil
import subprocess

import streamlit as st
from streamlit_lottie import st_lottie
from deta import Deta

deta = Deta(st.secrets["DETA_KEY"])
db = deta.Drive("user-images")

image_file = st.file_uploader("Please upload a food image",type=['png','jpeg','jpg'])
col1, col2 = st.columns(2)

if image_file is not None:
    img = Image.open(image_file)
    with col1:
        st.image(img, caption='Uploaded Image', use_column_width='always')

    ts = datetime.timestamp(datetime.now())
    img_name = str(ts)+image_file.name
    db.put(img_name, image_file)
    st.success("Saved Image")


    #call Model prediction--
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True) 
    model.cuda() if device == 'cuda' else model.cpu()
    pred = model(imgpath)
    pred.render()  # render bbox in image
    for im in pred.ims:
        im_base64 = Image.fromarray(im)
        db.put(f'{img_name}_pred', im_base64)

    #--Display predicton   
    img_ = Image.open(db.get(f'{img_name}_pred'))
    with col2:
        st.image(img_, caption='Model Prediction(s)', use_column_width='always')
    


# import torch
# from PIL import Image
# import requests
# import os
# import shutil
# import subprocess

# import streamlit as st
# from streamlit_lottie import st_lottie
# import database as db

# st.write('Hello world!')
# cwd = os.getcwd()
# st.write(cwd)


# image_file = st.file_uploader("Please upload a food image",type=['png','jpeg','jpg'])

# if image_file is not None:
#     file_details = {"FileName": image_file.name,"FileType": image_file.type}

#     st.write(file_details)

#     img = Image.open(image_file)
#     st.write('Original image')
#     st.image(img, use_column_width=False)

#     with open(os.path.join('user_uploads', image_file.name), "wb") as f: 
#         f.write(image_file.getbuffer())         
#         st.success("Saved File")
