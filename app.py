import torch
from PIL import Image
import requests
import os
import shutil
import random
import detect

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from allrecipes import AllRecipes

cwd = os.getcwd()

banner_img = Image.open('statics/food-banner.png')
st.image(banner_img, use_column_width=True)


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


if selected == "What's on your plate?":
    col1, col2 = st.columns(2)
    image_file = st.file_uploader('',type=['png', 'jpeg', 'jpg'])

    if image_file is not None:

        with col1:
            st.write('Original image')
            original_img = Image.open(image_file)
            st.image(original_img, use_column_width=True)

            with open(os.path.join(f'{cwd}/user_uploads', image_file.name), "wb") as f: 
                f.write(image_file.getbuffer())    
                st.success("Saved File")

        with col2:
            st.write('Inferenced image')

            # Check Folder is exists or Not
            folderPath = f'{cwd}/inferenced_imgs'
            if os.path.exists(folderPath):    
                # Delete Folder code
                shutil.rmtree(folderPath)

            
            detect.run(source='user_uploads', 
                       weights='best.pt', 
                       project=f'{cwd}', 
                       name='inferenced_imgs', 
                       save_txt=True)
            
            inferred_img = os.path.join('inferenced_imgs/', image_file.name)
            st.image(inferred_img, use_column_width=True)


elif selected == "Recipe Recommendations":
    image_file_name = 'pizza_salad'
    labels_path = f'inferenced_imgs/labels/{image_file_name}.txt'
    with open(labels_path) as f:
        lines = f.readlines()
        labels = set()
        for line in lines:
            labels.add(line.split(' ')[0])

    labels = list(labels)
    labels_w = []
    for num in labels:
        labels_w.append(cat_list[int(num)])


    for ingre in labels_w:
        search_string = ingre
        query_result = AllRecipes.search(search_string)
        num = random.randint(0, len(query_result))
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