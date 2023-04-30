import streamlit as st
from deta import Deta
from PIL import Image


# Connect to Deta Base with your Data Key
deta = Deta(st.secrets["DETA_KEY"])

db = deta.Drive("user-images")
image_file = st.file_uploader("Please upload a food image",type=['png','jpeg','jpg'])

if image_file is not None:
    db.put(image_file.name, image_file)
    st.success('Successfully saved image')

    img_ = db.get(image_file.name)

    img = Image.open(img_)
    st.image(img, use_column_width=False)
