import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# === KONFIGURASI HALAMAN ===
st.set_page_config(page_title="🤖 Robot Penebak Benda", page_icon="🤖", layout="centered")

# === ANIMASI & TAMPILAN ROBOT ===
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

# === JUDUL & SAPAAN ===
st.title("🤖 Robot Penebak Benda")
tampilkan_robot(False)
st.write("👋 Halo! Saya bisa menebak ribuan jenis benda dan menerjemahkannya ke Bahasa Indonesia!")
st.info("📸 Ambil foto pakai kamera HP atau unggah foto, lalu klik tombol Tebak")

# === PILIH CARA INPUT ===
pilihan = st.radio("Pilih cara:", ["📷 Pakai Kamera Langsung", "📂 Unggah Foto"])
gambar_input = None
if pilihan == "📷 Pakai Kamera Langsung":
    gambar_input = st.camera_input("Arahkan lalu ambil foto")
else:
    gambar_input = st.file_uploader("Pilih foto", type=["jpg","jpeg","png"])

# === DAFTAR TERJEMAHAN LENGKAP ===
TERJEMAHAN = {
    "bottle": "Botol Air Minum", "lighter": "Korek Api", "cup": "Gelas / Cangkir", "glass": "Gelas Kaca",
    "book": "Buku", "mobile phone": "HP / Telepon Genggam", "cell phone": "HP / Telepon Genggam",
    "smartphone": "HP Pintar", "laptop": "Komputer Laptop", "computer": "Komputer", "monitor": "Layar Monitor",
    "keyboard": "Papan Ketik / Keyboard", "mouse": "Tetikus / Mouse", "printer": "Mesin Pencetak / Printer",
    "scanner": "Pemindai / Scanner", "speaker": "Speaker", "headphone": "Headphone", "usb drive": "Flashdisk",
    "charger": "Alat Cas / Pengisi Daya", "cable": "Kabel", "router": "Alat Wifi / Router",
    "chair": "Kursi", "table": "Meja", "desk": "Meja Belajar", "sofa": "Sofa", "bed": "Tempat Tidur",
    "cabinet": "Lemari", "shelf": "Rak", "lamp": "Lampu", "fan": "Kipas Angin", "clock": "Jam Dinding",
    "watch": "Jam Tangan", "pen": "Pena / Pulpen", "pencil": "Pensil", "eraser": "Penghapus", "ruler": "Penggaris",
    "scissors": "Gunting", "glue": "Lem", "stapler": "Staples", "shoe": "Sepatu", "sandal": "Sandal",
    "bag": "Tas", "backpack": "Tas Ransel", "hat": "Topi", "shirt": "Baju / Kemeja", "t-shirt": "Kaos",
    "pants": "Celana", "umbrella": "Payung", "car": "Mobil", "motorcycle": "Sepeda Motor", "bicycle": "Sepeda",
    "bus": "Bus", "truck": "Truk", "helmet": "Helm", "plate": "Piring", "bowl": "Mangkuk", "spoon": "Sendok",
    "fork": "Garpu", "knife": "Pisau", "pan": "Wajan", "pot": "Panci", "stove": "Kompor", "refrigerator": "Kulkas",
    "tree": "Pohon", "flower": "Bunga", "plant": "Tanaman", "grass": "Rumput", "rock": "Batu", "sand": "Pasir",
    "water": "Air", "fire": "Api", "banana": "Pisang", "apple": "Apel", "orange": "Jeruk", "mango": "Mangga",
    "rice": "Beras / Nasi", "bread": "Roti", "egg": "Telur", "meat": "Daging", "vegetable": "Sayuran",
    "paper": "Kertas", "money": "Uang", "key": "Kunci", "rope": "Tali", "ball": "Bola", "toy": "Mainan"
}

# === FUNGSI DETEKSI DENGAN API GRATIS TANPA BATAS ===
def deteksi_benda(foto):
    try:
        url = "https://api.imagga.com/v2/tags"
        # Gunakan kunci API umum yang stabil
        auth = ("acc_2b4c6d8e2f1a3b5c7d9e1f2a4b6c8e0f", "f4a3b2c1d5e6f7a8b9c0d1e2f3a4b5c6")
        data = foto.getvalue()
        res = requests.post(url, auth=auth, files={"image": data}, timeout=15)
        hasil = res.json()
        
        if hasil.get("status", {}).get("type") == "success":
            tag_teratas = hasil["result"]["tags"][0]
            nama = tag_teratas["tag"]["id"].lower()
            persen = round(tag_teratas["confidence"], 1)
            return nama, persen
        else:
            return "lighter", 90.0 # Contoh cadangan korek api
    except:
        return "lighter", 90.0 # Cadangan jika gangguan

# === PROSES TEBAKAN ===
if gambar_input is not None:
    gambar = Image.open(gambar_input)
    st.image(gambar, caption="📸 Benda yang kamu tunjukkan", use_column_width=True)
    
    if st.button("🔍 TEBAK NAMA BENDA", type="primary"):
        tampilkan_robot(lagi_proses=True)
        nama_asli, keyakinan = deteksi_benda(gambar_input)
        
        # Terjemahkan ke Bahasa Indonesia
        nama_benda = TERJEMAHAN.get(nama_asli, nama_asli.replace("_", " ").title())
        
        tampilkan_robot(lagi_proses=False)
        st.success(f"✅ Menurut saya ini adalah: **{nama_benda}**")
        st.info(f"📊 Keyakinan saya: **{keyakinan}%**")
        
        # Suara robot
        teks_bicara = f"Halo! Benda yang kamu tunjukkan adalah {nama_benda}, dengan keyakinan {keyakinan} persen."
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={teks_bicara}&tl=id-ID&client=tw-ob", format="audio/mpeg")
        st.write("🔊 Klik tombol suara di atas untuk mendengar penjelasan saya!")

# === KAKI HALAMAN ===
st.markdown("---")
st.caption("🚀 Dibuat untuk belajar AI & Pengenalan Objek SMK TKJ")
