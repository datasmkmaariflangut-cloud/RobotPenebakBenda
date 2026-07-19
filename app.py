import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array

st.set_page_config(page_title="🤖 Robot Penebak Benda", page_icon="🤖", layout="centered")

@st.cache_resource(show_spinner=False)
def muat_model():
    return MobileNetV2(weights='imagenet')
model = muat_model()

def deteksi_objek(gambar):
    gambar = gambar.convert('RGB')
    gambar_ubah = gambar.resize((224, 224))
    gambar_ubah = img_to_array(gambar_ubah)
    gambar_ubah = np.expand_dims(gambar_ubah, axis=0)
    gambar_ubah = preprocess_input(gambar_ubah)
    prediksi = model.predict(gambar_ubah, verbose=0)
    hasil = decode_predictions(prediksi, top=1)[0][0]
    nama_benda = hasil[1].replace('_', ' ').title()
    persen = round(hasil[2]*100, 1)
    return nama_benda, persen

def tampilkan_robot(lagi_proses=False):
    if lagi_proses:
        st.markdown("""
        <style>
        @keyframes loncat {0%{transform:translateY(0)}50%{transform:translateY(-12px)}100%{transform:translateY(0)}}
        @keyframes kedip {0%{opacity:1}45%{opacity:0}55%{opacity:0}100%{opacity:1}}
        @keyframes goyang {0%{rotate:-3deg}50%{rotate:3deg}100%{rotate:-3deg}}
        .wadah-robot{animation:loncat 0.7s infinite,goyang 1.2s infinite;transform-origin:bottom center}
        .mata{animation:kedip 1.5s infinite}
        </style>
        <div class="wadah-robot" style="text-align:center;">
        <svg width="200" height="260">
        <circle cx="100" cy="50" r="40" fill="#64C8FF" stroke="#3296C8" stroke-width="3"/>
        <circle class="mata" cx="80" cy="40" r="6" fill="black"/>
        <circle class="mata" cx="120" cy="40" r="6" fill="black"/>
        <path d="M75,60 Q100,50 125,60" stroke="black" stroke-width="2" fill="none"/>
        <rect x="60" y="90" width="80" height="120" fill="#64C8FF" stroke="#3296C8" stroke-width="3"/>
        <rect x="20" y="100" width="40" height="20" fill="#64C8FF"/>
        <rect x="140" y="100" width="40" height="20" fill="#64C8FF"/>
        <rect x="70" y="210" width="25" height="40" fill="#64C8FF"/>
        <rect x="105" y="210" width="25" height="40" fill="#64C8FF"/>
        </svg>
        <p style="color:#ff6600;font-weight:bold;">🤔 Sedang memikirkan jawabannya...</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        @keyframes angkat {to{rotate:-20deg}}
        .tangan-kiri{transform-origin:left;animation:angkat 1s forwards}
        .tangan-kanan{transform-origin:right;animation:angkat 1s forwards}
        </style>
        <div style="text-align:center;">
        <svg width="200" height="260">
        <circle cx="100" cy="50" r="40" fill="#64C8FF" stroke="#3296C8" stroke-width="3"/>
        <circle cx="80" cy="40" r="6" fill="black"/>
        <circle cx="120" cy="40" r="6" fill="black"/>
        <path d="M80,60 Q100,75 120,60" stroke="black" stroke-width="2" fill="none"/>
        <rect x="60" y="90" width="80" height="120" fill="#64C8FF" stroke="#3296C8" stroke-width="3"/>
        <rect class="tangan-kiri" x="20" y="100" width="40" height="20" fill="#64C8FF"/>
        <rect class="tangan-kanan" x="140" y="100" width="40" height="20" fill="#64C8FF"/>
        <rect x="70" y="210" width="25" height="40" fill="#64C8FF"/>
        <rect x="105" y="210" width="25" height="40" fill="#64C8FF"/>
        </svg>
        </div>
        """, unsafe_allow_html=True)

st.title("🤖 Robot Penebak Benda")
tampilkan_robot(False)
st.write("👋 Halo! Saya siap menebak nama benda yang kamu tunjukkan!")
st.info("📸 Ambil foto pakai kamera HP atau unggah foto, lalu klik tombol Tebak")

pilihan = st.radio("Pilih cara:", ["📷 Pakai Kamera Langsung", "📂 Unggah Foto"])
gambar_input = st.camera_input("Arahkan lalu ambil foto") if pilihan == "📷 Pakai Kamera Langsung" else st.file_uploader("Pilih foto", type=["jpg","jpeg","png"])

if gambar_input:
    gambar = Image.open(gambar_input)
    st.image(gambar, use_column_width=True)
    if st.button("🔍 TEBAK NAMA BENDA", type="primary"):
        tampilkan_robot(True)
        nama, keyakinan = deteksi_objek(gambar)
        tampilkan_robot(False)
        st.success(f"✅ Ini adalah: **{nama}**")
        st.info(f"📊 Keyakinan: **{keyakinan}%**")
        suara = f"Halo! Benda ini adalah {nama}, dengan keyakinan {keyakinan} persen."
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={suara}&tl=id-ID&client=tw-ob", format="audio/mpeg")
        st.write("🔊 Klik tombol suara untuk mendengar!")

st.caption("🚀 Gratis & Bisa Dibuka di HP Mana Saja")
