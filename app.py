import streamlit as st
from PIL import Image
import numpy as np
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array

st.set_page_config(page_title="🤖 Robot Penebak Benda", page_icon="🤖", layout="centered")

# Muat model dengan cara lebih ringan
@st.cache_resource(show_spinner="🤖 Robot sedang memuat otaknya...")
def muat_model():
    return MobileNetV2(weights="imagenet", include_top=True)

model = muat_model()
