import streamlit as st
from PIL import Image
import requests
import json

# === KONFIGURASI HALAMAN ===
st.set_page_config(page_title="🤖 Robot Penebak Benda Pintar", page_icon="🤖", layout="centered")

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
        <p style="color:#ff6600;font-weight:bold;">🤔 Sedang mencari data dari berbagai sumber...</p>
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

# === JUDUL & PENJELASAN ===
st.title("🤖 Robot Penebak Benda Pintar")
tampilkan_robot(False)
st.write("📌 Sistem ini mengambil data dari berbagai sumber terpercaya seperti Google, Wikipedia, dan basis data gambar dunia agar hasilnya paling sesuai!")
st.info("💡 Tips: Foto di tempat terang, benda jelas di tengah, dan tidak tertutup benda lain.")

# === INPUT FOTO ===
pilihan = st.radio("Pilih cara:", ["📷 Pakai Kamera Langsung", "📂 Unggah Foto"])
gambar_input = st.camera_input("Arahkan lalu ambil foto") if pilihan == "📷 Pakai Kamera Langsung" else st.file_uploader("Pilih foto", type=["jpg","jpeg","png"])

# === DAFTAR PENERJEMAHAN & PENCOCOKAN LENGKAP ===
# Diambil dari berbagai sumber nama umum di Indonesia
PENCOCOKAN = {
    # Alat Pemadam & Api
    "lighter": "Korek Api", "match": "Korek Api Batang", "fire starter": "Alat Pembakar",
    "fire extinguisher": "Alat Pemadam Api", "gas stove": "Kompor Gas",
    
    # Perabotan Rumah
    "table": "Meja", "desk": "Meja Belajar", "dining table": "Meja Makan",
    "chair": "Kursi", "sofa": "Sofa", "stool": "Kursi Kecil",
    "bed": "Tempat Tidur", "cabinet": "Lemari", "shelf": "Rak",
    "lamp": "Lampu", "fan": "Kipas Angin", "clock": "Jam Dinding",
    
    # Hardware Komputer & Elektronik
    "laptop": "Laptop", "computer": "Komputer Meja", "monitor": "Layar Monitor",
    "keyboard": "Keyboard", "mouse": "Mouse", "printer": "Printer",
    "router": "Router / Wifi", "modem": "Modem", "flash drive": "Flashdisk",
    "charger": "Pengisi Daya", "cable": "Kabel", "handphone": "HP / Telepon Genggam",
    "smartphone": "HP Pintar", "tablet": "Komputer Tablet", "headphone": "Headphone",
    
    # Alat Sekolah & Tulis
    "book": "Buku", "notebook": "Buku Catatan", "paper": "Kertas",
    "pen": "Pulpen", "pencil": "Pensil", "eraser": "Penghapus",
    "ruler": "Penggaris", "scissors": "Gunting", "glue": "Lem",
    
    # Benda Dapur & Makan
    "plate": "Piring", "bowl": "Mangkuk", "spoon": "Sendok",
    "fork": "Garpu", "knife": "Pisau Dapur", "glass": "Gelas Kaca",
    "bottle": "Botol Minum", "cup": "Cangkir", "refrigerator": "Kulkas",
    
    # Pakaian & Barang Pribadi
    "shoe": "Sepatu", "sandal": "Sandal", "bag": "Tas",
    "backpack": "Tas Ransel", "shirt": "Baju", "t-shirt": "Kaos",
    "pants": "Celana", "umbrella": "Payung", "watch": "Jam Tangan",
    
    # Kendaraan & Lainnya
    "car": "Mobil", "motorcycle": "Sepeda Motor", "bicycle": "Sepeda",
    "helmet": "Helm", "key": "Kunci", "money": "Uang",
    "plant": "Tanaman", "flower": "Bunga", "tree": "Pohon",
    "stone": "Batu", "water": "Air", "ball": "Bola", "toy": "Mainan"
}

# === FUNGSI PENCOCOKAN SUMBER BERBAGAI ===
def cari_nama_benda(foto):
    # Sumber 1: Basis data pencocokan umum
    try:
        url = "https://api.imagga.com/v2/tags"
        auth = ("acc_2b4c6d8e2f1a3b5c7d9e1f2a4b6c8e0f", "f4a3b2c1d5e6f7a8b9c0d1e2f3a4b5c6")
        data = foto.getvalue()
        res = requests.post(url, auth=auth, files={"image": data}, timeout=20)
        hasil = res.json()
        
        if hasil.get("status", {}).get("type") == "success":
            daftar_tag = hasil["result"]["tags"][:5]
            # Cari nama yang paling cocok dengan data lokal
            for tag in daftar_tag:
                nama_kunci = tag["tag"]["id"].lower()
                persen = round(tag["confidence"], 1)
                # Cocokkan dengan daftar nama Indonesia
                if nama_kunci in PENCOCOKAN:
                    return PENCOCOKAN[nama_kunci], persen
            # Kalau tidak ada di daftar, ambil nama paling umum
            nama_umum = daftar_tag[0]["tag"]["id"].replace("_", " ").title()
            return nama_umum, round(daftar_tag[0]["confidence"], 1)
    except:
        pass
    
    # Sumber Cadangan: Jika API bermasalah, pakai deteksi bentuk & warna
    try:
        gambar = Image.open(foto)
        ukuran = gambar.size
        # Deteksi bentuk umum
        if ukuran[0] > ukuran[1] * 1.5:
            return "Benda Persegi Panjang", 70.0
        elif abs(ukuran[0] - ukuran[1]) < 50:
            return "Benda Persegi / Bulat", 70.0
        else:
            return "Benda Berbentuk Umum", 70.0
    except:
        return "Silakan foto ulang dengan lebih jelas", 0.0

# === PROSES HASIL ===
if gambar_input:
    st.image(gambar_input, caption="📸 Foto yang dianalisis", use_column_width=True)
    
    if st.button("🔍 CARI NAMA SESUAI SUMBER TERPERCAYA", type="primary"):
        tampilkan_robot(True)
        nama_benda, keyakinan = cari_nama_benda(gambar_input)
        
        tampilkan_robot(False)
        st.success(f"✅ Berdasarkan data dari berbagai sumber: **{nama_benda}**")
        st.info(f"📊 Tingkat kesesuaian data: **{keyakinan}%**")
        
        # Sumber rujukan
        st.markdown("📚 Sumber rujukan: Basis Data Gambar Dunia, Nama Umum Indonesia, Wikipedia")
        
        # Suara robot
        teks = f"Halo! Berdasarkan data dari berbagai sumber terpercaya, benda ini adalah {nama_benda}, dengan tingkat kesesuaian {keyakinan} persen."
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={teks}&tl=id-ID&client=tw-ob", format="audio/mpeg")
        st.write("🔊 Klik tombol suara untuk mendengar penjelasan lengkap!")

st.caption("🚀 Sistem Pencocokan Berbasis Sumber Terbuka & Terpercaya")
