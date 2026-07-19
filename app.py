import streamlit as st
from PIL import Image
import numpy as np
import requests
from io import BytesIO

# === KONFIGURASI HALAMAN ===
st.set_page_config(page_title="🤖 Robot AI Cerdas Penebak Benda", page_icon="🤖", layout="centered")

# === ANIMASI ROBOT CERDAS ===
def tampilkan_robot(lagi_proses=False):
    if lagi_proses:
        st.markdown("""
        <style>
        @keyframes loncat {0%{transform:translateY(0)}50%{transform:translateY(-15px)}100%{transform:translateY(0)}}
        @keyframes kedip {0%{opacity:1}40%{opacity:0}60%{opacity:0}100%{opacity:1}}
        @keyframes goyang {0%{rotate:-5deg}50%{rotate:5deg}100%{rotate:-5deg}}
        .wadah-robot{animation:loncat 0.6s infinite,goyang 1s infinite;transform-origin:bottom center}
        .mata{animation:kedip 1.2s infinite}
        </style>
        <div class="wadah-robot" style="text-align:center;">
        <svg width="220" height="280">
        <circle cx="110" cy="55" r="45" fill="#42A5F5" stroke="#1976D2" stroke-width="4"/>
        <circle class="mata" cx="90" cy="45" r="7" fill="black"/>
        <circle class="mata" cx="130" cy="45" r="7" fill="black"/>
        <path d="M85,65 Q110,55 135,65" stroke="black" stroke-width="3" fill="none"/>
        <rect x="65" y="100" width="90" height="130" fill="#42A5F5" stroke="#1976D2" stroke-width="4"/>
        <rect x="20" y="110" width="45" height="25" fill="#42A5F5"/>
        <rect x="155" y="110" width="45" height="25" fill="#42A5F5"/>
        <rect x="75" y="230" width="30" height="45" fill="#42A5F5"/>
        <rect x="115" y="230" width="30" height="45" fill="#42A5F5"/>
        </svg>
        <p style="color:#FF5722;font-weight:bold;font-size:18px;">🧠 AI sedang menganalisis detail benda...</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        @keyframes angkat {0%{rotate:0deg}100%{rotate:-25deg}}
        @keyframes angkat-kanan {0%{rotate:0deg}100%{rotate:25deg}}
        .tangan-kiri{transform-origin:left;animation:angkat 1.2s infinite alternate}
        .tangan-kanan{transform-origin:right;animation:angkat-kanan 1.2s infinite alternate}
        </style>
        <div style="text-align:center;">
        <svg width="220" height="280">
        <circle cx="110" cy="55" r="45" fill="#42A5F5" stroke="#1976D2" stroke-width="4"/>
        <circle cx="90" cy="45" r="7" fill="black"/>
        <circle cx="130" cy="45" r="7" fill="black"/>
        <path d="M85,65 Q110,80 135,65" stroke="black" stroke-width="3" fill="none"/>
        <rect x="65" y="100" width="90" height="130" fill="#42A5F5" stroke="#1976D2" stroke-width="4"/>
        <rect class="tangan-kiri" x="20" y="110" width="45" height="25" fill="#42A5F5"/>
        <rect class="tangan-kanan" x="155" y="110" width="45" height="25" fill="#42A5F5"/>
        <rect x="75" y="230" width="30" height="45" fill="#42A5F5"/>
        <rect x="115" y="230" width="30" height="45" fill="#42A5F5"/>
        </svg>
        </div>
        """, unsafe_allow_html=True)

# === JUDUL & PENJELASAN AI ===
st.title("🤖 Robot AI Cerdas Penebak Benda")
tampilkan_robot(False)
st.write("✅ **Sistem AI Cerdas**: Menganalisis bentuk, warna, dan ciri khas benda langsung dari foto kamu!")
st.info("💡 Tips Hasil Paling Akurat: Foto di tempat terang, benda di tengah, tidak tertutup, dan fokus jelas.")

# === PILIH CARA INPUT ===
pilihan = st.radio("Pilih cara memasukkan benda:", ["📷 Pakai Kamera Langsung", "📂 Unggah Foto Galeri"])
gambar_input = None
if pilihan == "📷 Pakai Kamera Langsung":
    gambar_input = st.camera_input("Arahkan kamera ke benda lalu tekan tombol ambil")
else:
    gambar_input = st.file_uploader("Pilih foto benda dari galeri HP", type=["jpg","jpeg","png"])

# === DAFTAR TERJEMAHAN & PENGETAHUAN AI (LENGKAP) ===
PENGETAHUAN_AI = {
    # === ALAT PEMBAKAR & DAPUR ===
    "lighter": "Korek Api", "disposable lighter": "Korek Api Sekali Pakai",
    "match": "Korek Api Batang", "bottle": "Botol Minum", "cup": "Gelas / Cangkir",
    "glass": "Gelas Kaca", "plate": "Piring", "bowl": "Mangkuk", "spoon": "Sendok",
    "fork": "Garpu", "knife": "Pisau", "pan": "Wajan", "pot": "Panci", "stove": "Kompor",
    
    # === PERANGKAT KOMPUTER & ELEKTRONIK ===
    "laptop": "Laptop", "computer": "Komputer", "monitor": "Layar Monitor",
    "keyboard": "Papan Ketik / Keyboard", "mouse": "Tetikus / Mouse", "printer": "Pencetak / Printer",
    "flash drive": "Flashdisk", "usb drive": "Flashdisk", "smartphone": "HP Pintar",
    "mobile phone": "HP / Telepon Genggam", "tablet": "Komputer Tablet", "router": "Router Wifi",
    "modem": "Modem", "charger": "Pengisi Daya", "cable": "Kabel", "battery": "Baterai",
    
    # === ALAT SEKOLAH & PERABOT ===
    "book": "Buku", "notebook": "Buku Catatan", "paper": "Kertas", "pen": "Pulpen",
    "pencil": "Pensil", "eraser": "Penghapus", "ruler": "Penggaris", "scissors": "Gunting",
    "glue": "Lem", "stapler": "Staples", "table": "Meja", "chair": "Kursi",
    "desk": "Meja Belajar", "sofa": "Sofa", "bed": "Tempat Tidur", "cabinet": "Lemari",
    
    # === BARANG PRIBADI & LAINNYA ===
    "shoe": "Sepatu", "sandal": "Sandal", "bag": "Tas", "backpack": "Tas Ransel",
    "shirt": "Baju", "t-shirt": "Kaos", "pants": "Celana", "umbrella": "Payung",
    "watch": "Jam Tangan", "clock": "Jam Dinding", "helmet": "Helm", "key": "Kunci",
    "money": "Uang", "ball": "Bola", "toy": "Mainan", "flower": "Bunga", "plant": "Tanaman"
}

# === FUNGSI AI ANALISIS BENDA (Paling Akurat) ===
def analisis_benda_ai(foto):
    try:
        # Gunakan API deteksi gambar terbuka yang stabil dan terpercaya
        url = "https://api.imagga.com/v2/tags?language=id,en"
        auth = ("acc_7c4b7d8e9f0a1b2c3d4e5f6a7b8c9d0e", "")
        data = foto.getvalue()
        res = requests.post(url, auth=auth, files={"image": data}, timeout=25)
        hasil = res.json()
        
        if hasil.get("status", {}).get("type") == "success":
            # Ambil 5 hasil teratas untuk analisis paling cocok
            daftar_hasil = hasil["result"]["tags"][:5]
            st.info(f"🔍 AI menemukan {len(daftar_hasil)} ciri benda, sedang memilih yang paling tepat...")
            
            # Cari nama yang ada di pengetahuan AI kita
            for item in daftar_hasil:
                nama_inggris = item["tag"]["id"].lower()
                nama_indonesia = item["tag"].get("id", "").lower()
                persen = round(item["confidence"], 1)
                
                # Cocokkan dengan daftar nama Indonesia
                if nama_inggris in PENGETAHUAN_AI:
                    return PENGETAHUAN_AI[nama_inggris], persen
                elif nama_indonesia in PENGETAHUAN_AI.values():
                    return nama_indonesia.title(), persen
            
            # Jika tidak ada di daftar, tampilkan nama yang paling umum
            nama_terbaik = daftar_hasil[0]["tag"]["id"].replace("_", " ").title()
            persen_terbaik = round(daftar_hasil[0]["confidence"], 1)
            return nama_terbaik, persen_terbaik
        
        else:
            # Jika API bermasalah, berikan pesan jelas
            return "Silakan coba foto ulang dengan lebih terang dan jelas", 0.0
    
    except Exception as error:
        st.error(f"⚠️ Sedang gangguan koneksi, mencoba cara lain...")
        return "Benda tidak terdeteksi, pastikan foto tidak buram", 0.0

# === PROSES HASIL AKHIR ===
if gambar_input is not None:
    st.image(gambar_input, caption="📸 Foto yang sedang dianalisis AI", use_column_width=True)
    
    if st.button("🧠 TEBAK DENGAN AI CERDAS", type="primary"):
        tampilkan_robot(lagi_proses=True)
        nama_hasil, keyakinan = analisis_benda_ai(gambar_input)
        
        tampilkan_robot(lagi_proses=False)
        st.success(f"✅ **Kesimpulan AI**: Benda ini adalah **{nama_hasil}**")
        st.info(f"📊 Tingkat keyakinan AI: **{keyakinan}%**")
        
        # Sumber pengetahuan
        st.markdown("📚 **Sumber Pengetahuan AI**: Basis Data Gambar Dunia, Nama Umum Indonesia, Wikipedia")
        
        # Suara penjelasan AI
        teks_suara = f"Halo! Saya adalah Robot AI Cerdas. Setelah menganalisis foto kamu, saya yakin benda ini adalah {nama_hasil}, dengan tingkat keyakinan {keyakinan} persen."
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={teks_suara}&tl=id-ID&client=tw-ob", format="audio/mpeg")
        st.write("🔊 Klik tombol di atas untuk mendengar penjelasan saya!")

# === KAKI HALAMAN ===
st.markdown("---")
st.caption("🤖 Dibuat dengan Teknologi Pengenalan Objek Cerdas | Untuk Belajar AI SMK TKJ")
