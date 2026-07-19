import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

# === KONFIGURASI HALAMAN ===
st.set_page_config(page_title="🤖 AI Deteksi Benda & Alat TKJ", page_icon="🤖", layout="centered")

# === MUAT MODEL DENGAN AMAN ===
@st.cache_resource(show_spinner="🧠 Memuat model AI pintar...")
def muat_model():
    # Pakai model YOLOv8 paling ringan dan akurat
    return YOLO("yolov8n.pt")

try:
    model = muat_model()
    st.success("✅ Model AI siap digunakan!")
except Exception as e:
    st.error(f"❌ Gagal memuat model: {str(e)}")
    st.stop()

# === JUDUL & PENJELASAN ===
st.title("🤖 AI Deteksi Benda & Alat TKJ")
st.info("📸 Foto benda sehari-hari atau alat jaringan, AI akan mengenali namanya dengan akurat!")

# === INPUT FOTO ===
sumber = st.radio("Pilih sumber gambar:", ["📷 Kamera Langsung", "📂 Unggah Foto"])
gambar = None

if sumber == "📷 Kamera Langsung":
    gambar = st.camera_input("Arahkan kamera ke benda lalu ambil foto")
else:
    gambar = st.file_uploader("Pilih foto dari galeri", type=["jpg", "jpeg", "png"])

# === PROSES DETEKSI ===
if gambar:
    img = Image.open(gambar)
    st.image(img, caption="📸 Foto yang dianalisis", use_column_width=True)
    
    if st.button("🔍 DETEKSI BENDA", type="primary"):
        with st.spinner("🧠 AI sedang menganalisis ciri benda..."):
            # Ubah format gambar
            arr = np.array(img)
            # Jalankan deteksi
            hasil = model.predict(arr, conf=0.5, verbose=False)
            
            if len(hasil[0].boxes) == 0:
                st.warning("⚠️ Tidak ada benda terdeteksi jelas, coba foto lebih terang atau dekatkan ke benda.")
            else:
                st.success("✅ **Hasil Deteksi AI:**")
                for kotak in hasil[0].boxes:
                    nama = model.names[int(kotak.cls[0])]
                    persen = round(float(kotak.conf[0]) * 100, 1)
                    st.write(f"• **{nama}** : {persen}% keyakinan")
                
                # Tampilkan gambar dengan kotak deteksi
                hasil_gambar = hasil[0].plot()[:, :, ::-1]
                st.image(hasil_gambar, caption="📊 Gambar dengan penandaan AI", use_column_width=True)

# === KAKI HALAMAN ===
st.markdown("---")
st.caption("🚀 Dibuat untuk Pembelajaran AI & TKJ | Menggunakan Model YOLOv8")
