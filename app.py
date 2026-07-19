import streamlit as st
from PIL import Image

# === KONFIGURASI ===
st.set_page_config(page_title="🤖 Robot Penebak Benda", page_icon="🤖", layout="centered")

# === ANIMASI ROBOT ===
def tampilkan_robot(lagi_proses=False):
    if lagi_proses:
        st.markdown("""
        <style>
        @keyframes loncat {0%{transform:translateY(0)}50%{transform:translateY(-12px)}100%{transform:translateY(0)}}
        @keyframes kedip {0%{opacity:1}45%{opacity:0}55%{opacity:0}100%{opacity:1}}
        .wadah-robot{animation:loncat 0.7s infinite;transform-origin:bottom center}
        </style>
        <div class="wadah-robot" style="text-align:center;">
        <svg width="200" height="260">
        <circle cx="100" cy="50" r="40" fill="#64C8FF" stroke="#3296C8" stroke-width="3"/>
        <circle cx="80" cy="40" r="6" fill="black"/>
        <circle cx="120" cy="40" r="6" fill="black"/>
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
        <style>@keyframes angkat {to{rotate:-20deg}}.tangan-kiri{transform-origin:left;animation:angkat 1s forwards}</style>
        <div style="text-align:center;">
        <svg width="200" height="260">
        <circle cx="100" cy="50" r="40" fill="#64C8FF" stroke="#3296C8" stroke-width="3"/>
        <circle cx="80" cy="40" r="6" fill="black"/>
        <circle cx="120" cy="40" r="6" fill="black"/>
        <path d="M80,60 Q100,75 120,60" stroke="black" stroke-width="2" fill="none"/>
        <rect x="60" y="90" width="80" height="120" fill="#64C8FF" stroke="#3296C8" stroke-width="3"/>
        <rect class="tangan-kiri" x="20" y="100" width="40" height="20" fill="#64C8FF"/>
        <rect x="140" y="100" width="40" height="20" fill="#64C8FF"/>
        <rect x="70" y="210" width="25" height="40" fill="#64C8FF"/>
        <rect x="105" y="210" width="25" height="40" fill="#64C8FF"/>
        </svg>
        </div>
        """, unsafe_allow_html=True)

# === JUDUL ===
st.title("🤖 Robot Penebak Benda")
tampilkan_robot(False)
st.info("📸 Ambil foto benda apa saja, saya akan menebaknya!")

# === INPUT GAMBAR ===
pilihan = st.radio("Pilih cara:", ["📷 Pakai Kamera Langsung", "📂 Unggah Foto"])
gambar_input = st.camera_input("Arahkan lalu ambil foto") if pilihan == "📷 Pakai Kamera Langsung" else st.file_uploader("Pilih foto", type=["jpg","jpeg","png"])

# === DAFTAR TERJEMAHAN LENGKAP ===
TERJEMAHAN = {
    "bottle": "Botol Air Minum", "lighter": "Korek Api", "cup": "Gelas / Cangkir",
    "book": "Buku", "mobile phone": "HP", "laptop": "Laptop", "keyboard": "Keyboard",
    "mouse": "Mouse", "monitor": "Monitor", "printer": "Printer", "chair": "Kursi",
    "table": "Meja", "pencil": "Pensil", "pen": "Pulpen", "shoe": "Sepatu", "bag": "Tas",
    "clock": "Jam", "flower": "Bunga", "tree": "Pohon", "car": "Mobil", "motorcycle": "Motor",
    "bicycle": "Sepeda", "plate": "Piring", "spoon": "Sendok", "fork": "Garpu", "rice": "Nasi",
    "water": "Air", "paper": "Kertas", "scissors": "Gunting", "glue": "Lem", "lighter": "Korek Api"
}

# === PROSES TEBAKAN ===
if gambar_input:
    gambar = Image.open(gambar_input)
    st.image(gambar, caption="📸 Benda yang kamu tunjukkan", use_column_width=True)
    
    if st.button("🔍 TEBAK NAMA BENDA", type="primary"):
        tampilkan_robot(True)
        
        # Gunakan deteksi bawaan Streamlit
        hasil = st.image_classifier(gambar)
        nama_inggris = hasil[0]["label"].lower()
        keyakinan = round(hasil[0]["score"] * 100, 1)
        
        # Terjemahkan ke Indonesia
        nama_benda = TERJEMAHAN.get(nama_inggris, nama_inggris.replace("_", " ").title())
        
        tampilkan_robot(False)
        st.success(f"✅ Menurut saya ini adalah: **{nama_benda}**")
        st.info(f"📊 Keyakinan saya: **{keyakinan}%**")
        
        # Suara robot
        teks = f"Halo! Benda ini adalah {nama_benda}, dengan keyakinan {keyakinan} persen."
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={teks}&tl=id-ID&client=tw-ob", format="audio/mpeg")

st.caption("🚀 Dibuat untuk Pembelajaran AI SMK TKJ")
