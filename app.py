import streamlit as st
from PIL import Image
import requests

# === KONFIGURASI HALAMAN ===
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
        <p style="color:#ff6600;font-weight:bold;">🤔 Sedang memproses foto ini...</p>
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
st.info("📸 Pastikan foto terang, benda jelas di tengah, dan hanya satu jenis benda utama ya!")

# === INPUT FOTO ===
pilihan = st.radio("Pilih cara:", ["📷 Pakai Kamera Langsung", "📂 Unggah Foto"])
gambar_input = st.camera_input("Arahkan lalu ambil foto") if pilihan == "📷 Pakai Kamera Langsung" else st.file_uploader("Pilih foto", type=["jpg","jpeg","png"])

# === DAFTAR TERJEMAHAN LENGKAP ===
TERJEMAHAN = {
    "bottle": "Botol Air Minum", "lighter": "Korek Api", "cup": "Gelas / Cangkir", "glass": "Gelas Kaca",
    "book": "Buku", "mobile phone": "HP / Telepon Genggam", "cell phone": "HP / Telepon Genggam",
    "smartphone": "HP Pintar", "laptop": "Komputer Laptop", "computer": "Komputer", "monitor": "Layar Monitor",
    "keyboard": "Papan Ketik / Keyboard", "mouse": "Tetikus / Mouse", "printer": "Mesin Pencetak / Printer",
    "usb drive": "Flashdisk", "charger": "Alat Cas", "cable": "Kabel", "router": "Alat Wifi",
    "chair": "Kursi", "table": "Meja", "desk": "Meja Belajar", "sofa": "Sofa", "bed": "Tempat Tidur",
    "pen": "Pena / Pulpen", "pencil": "Pensil", "eraser": "Penghapus", "ruler": "Penggaris",
    "shoe": "Sepatu", "sandal": "Sandal", "bag": "Tas", "backpack": "Tas Ransel",
    "car": "Mobil", "motorcycle": "Sepeda Motor", "bicycle": "Sepeda", "helmet": "Helm",
    "plate": "Piring", "spoon": "Sendok", "fork": "Garpu", "pan": "Wajan", "pot": "Panci",
    "tree": "Pohon", "flower": "Bunga", "plant": "Tanaman", "rock": "Batu", "water": "Air",
    "banana": "Pisang", "apple": "Apel", "orange": "Jeruk", "mango": "Mangga", "rice": "Nasi",
    "paper": "Kertas", "key": "Kunci", "scissors": "Gunting", "glue": "Lem", "ball": "Bola"
}

# === FUNGSI DETEKSI BENDA ASLI ===
def deteksi_benda(foto):
    try:
        url = "https://api.imagga.com/v2/tags"
        auth = ("acc_7c4b7d8e9f0a1b2c3d4e5f6a7b8c9d0e", "")
        data = foto.getvalue()
        res = requests.post(url, auth=auth, files={"image": data}, timeout=20)
        hasil = res.json()
        
        if hasil.get("status", {}).get("type") == "success":
            tag_teratas = hasil["result"]["tags"][0]
            nama = tag_teratas["tag"]["id"].lower()
            persen = round(tag_teratas["confidence"], 1)
            return nama, persen
        else:
            return "tidak terdeteksi", 0.0
    except Exception as e:
        return "tidak terdeteksi", 0.0

# === PROSES HASIL ===
if gambar_input:
    st.image(gambar_input, caption="📸 Foto yang diambil", use_column_width=True)
    
    if st.button("🔍 TEBAK NAMA BENDA", type="primary"):
        tampilkan_robot(True)
        nama_asli, keyakinan = deteksi_benda(gambar_input)
        
        # Terjemahkan atau tampilkan asli
        if nama_asli in TERJEMAHAN:
            nama_benda = TERJEMAHAN[nama_asli]
        elif nama_asli != "tidak terdeteksi":
            nama_benda = nama_asli.replace("_", " ").title()
        else:
            nama_benda = "Benda tidak terdeteksi jelas, coba foto ulang lebih terang"
        
        tampilkan_robot(False)
        st.success(f"✅ Menurut saya ini adalah: **{nama_benda}**")
        st.info(f"📊 Tingkat keyakinan: **{keyakinan}%**")
        
        # Suara robot
        teks = f"Halo! Benda yang kamu tunjukkan adalah {nama_benda}, dengan keyakinan {keyakinan} persen."
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={teks}&tl=id-ID&client=tw-ob", format="audio/mpeg")

st.caption("🚀 Dibuat untuk Belajar AI SMK TKJ")
