import torch
from PIL import Image
import requests
import os
import shutil
import random
import detect
import cv2
import numpy as np

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from allrecipes import AllRecipes

cwd = os.getcwd()

banner_img = Image.open('statics/food-banner.png')
st.image(banner_img, use_column_width=True)

image_file = None

selected = option_menu(
    menu_title=None,
    options=["What's on your plate?", "Recipe Recommendations"],
    icons=['cloud-upload', 'bookmark-heart'],
    default_index=0,
    orientation='horizontal'
    )


with open('data_food_robo.yaml') as f:
    data = f.readlines()
    categories = data[-1]
    categories = categories.strip('names: [').strip(']')

cat_list = [cat[1:-1] for cat in categories.split(', ')]

image_file_name = None

if selected == "What's on your plate?":
    col1, col2 = st.columns(2)
    image_file = st.file_uploader('',type=['png', 'jpeg', 'jpg'])


    if image_file is not None:
        print(image_file)
        image = Image.open(image_file)
        img_array = np.array(image)

        with col1:
            st.write('Original image')
            original_img = Image.open(image_file)
            st.image(original_img, use_column_width=True)

            with open(f'{cwd}/user_uploads/{image_file.name}', "wb") as f: 
                f.write(image_file.getbuffer())    
                st.success("Saved File")

        with col2:
            st.write('Inferenced image')

            inferred_img, inferred_label, _ = detect.run(
                objs=[ cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR) ],
                weights='best.pt'
                )
                        
            st.image(inferred_img, use_column_width=True)
            st.write(inferred_label)

        if inferred_label not in st.session_state:
            st.session_state.inferred_label = inferred_label



if selected == "Recipe Recommendations":
    inferred_label = st.session_state.inferred_label

    labels = list(set(inferred_label))

    for ingre in labels:
        search_string = ingre
        query_result = AllRecipes.search(search_string)
        num = random.randint(0, len(query_result)-1)
        recipe = query_result[num]

        name = recipe['name']
        url = recipe['url']
        rate = recipe['rate']
        image = recipe['image']

        detailed_recipe = AllRecipes.get(url) 
        servings = detailed_recipe['nb_servings']
        ingres = detailed_recipe['ingredients']

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(name)
            st.image(image, use_column_width=True)
            st.write(f'Rating: {rate}')
            st.write(f'[More details >]({url})')
        with col2:
            st.subheader('')
            st.write(f'Servings: {servings}')
            st.write('Ingredients:')
            for ingre in ingres:
                st.write(ingre)

        st.write('---')