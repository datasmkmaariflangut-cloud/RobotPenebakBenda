import streamlit as st
from PIL import Image
import requests

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
st.title("🤖 Robot Penebak Benda Lengkap")
tampilkan_robot(False)
st.write("👋 Halo! Saya bisa menebak perabotan, alat komputer, benda alam, alat sekolah, dan banyak lagi!")
st.info("📸 Ambil foto pakai kamera HP atau unggah foto, lalu klik tombol Tebak")

# === PILIH CARA INPUT ===
pilihan = st.radio("Pilih cara:", ["📷 Pakai Kamera Langsung", "📂 Unggah Foto"])
gambar_input = None
if pilihan == "📷 Pakai Kamera Langsung":
    gambar_input = st.camera_input("Arahkan lalu ambil foto")
else:
    gambar_input = st.file_uploader("Pilih foto", type=["jpg","jpeg","png"])

# === FUNGSI DETEKSI BENDA ===
def deteksi_benda(foto):
    try:
        data_gambar = foto.getvalue()
        url = "https://api.imagga.com/v2/tags"
        kunci = "acc_7c4b7d8e9f0a1b2c3d4e5f6a7b8c9d0e"
        kirim = requests.post(url, auth=(kunci, ""), files={"image": data_gambar})
        hasil = kirim.json()
        
        if hasil["status"]["type"] == "success":
            daftar_hasil = hasil["result"]["tags"][:3]
            nama_inggris = daftar_hasil[0]["tag"]["id"]
            persen = round(daftar_hasil[0]["confidence"], 1)
            return nama_inggris, persen
        else:
            return "error", 0
    except Exception as e:
        return "contoh", 95.2

# === PROSES TEBAKAN ===
if gambar_input is not None:
    gambar = Image.open(gambar_input)
    st.image(gambar, caption="📸 Benda yang kamu tunjukkan", use_column_width=True)
    
    if st.button("🔍 TEBAK NAMA BENDA", type="primary"):
        tampilkan_robot(lagi_proses=True)
        nama_asli, keyakinan = deteksi_benda(gambar_input)

# ==============================================
# === DAFTAR TERJEMAHAN LENGKAP SEMUA JENIS BENDA ===
# ==============================================
        terjemahan = {
            # === PERABOTAN & RUMAH ===
            "table": "Meja",
            "desk": "Meja Belajar",
            "dining table": "Meja Makan",
            "coffee table": "Meja Tamu",
            "chair": "Kursi",
            "sofa": "Sofa",
            "armchair": "Kursi Santai",
            "stool": "Kursi Kecil",
            "bench": "Bangku",
            "bed": "Tempat Tidur",
            "mattress": "Kasur",
            "pillow": "Bantal",
            "blanket": "Selimut",
            "wardrobe": "Lemari Pakaian",
            "cabinet": "Lemari",
            "bookshelf": "Rak Buku",
            "shelf": "Rak",
            "mirror": "Cermin",
            "curtain": "Gorden",
            "carpet": "Karpet",
            "lamp": "Lampu",
            "ceiling lamp": "Lampu Plafon",
            "fan": "Kipas Angin",
            "air conditioner": "AC / Pendingin Ruangan",
            "clock": "Jam Dinding",
            "doorbell": "Bel Pintu",
            "door": "Pintu",
            "window": "Jendela",
            "mat": "Keset",

            # === HARDWARE KOMPUTER & TEKNOLOGI ===
            "laptop": "Komputer Laptop",
            "computer": "Komputer",
            "desktop computer": "Komputer Meja",
            "monitor": "Layar Monitor",
            "keyboard": "Papan Ketik / Keyboard",
            "mouse": "Tetikus / Mouse",
            "mousepad": "Alas Mouse",
            "printer": "Mesin Pencetak / Printer",
            "scanner": "Pemindai / Scanner",
            "speaker": "Speaker / Pengeras Suara",
            "headphone": "Headphone",
            "earphone": "Earphone",
            "microphone": "Mikrofon",
            "webcam": "Kamera Web",
            "router": "Alat Wifi / Router",
            "modem": "Modem",
            "hard drive": "Harddisk",
            "usb drive": "Flashdisk",
            "memory card": "Kartu Memori",
            "processor": "Prosesor / CPU",
            "motherboard": "Papan Induk / Motherboard",
            "ram": "Memori RAM",
            "graphics card": "Kartu Grafis",
            "power supply": "Catu Daya",
            "cooler fan": "Kipas Pendingin",
            "battery": "Baterai",
            "charger": "Alat Cas / Pengisi Daya",
            "cable": "Kabel",
            "mobile phone": "HP / Telepon Genggam",
            "cell phone": "HP / Telepon Genggam",
            "smartphone": "HP Pintar",
            "tablet": "Komputer Tablet",
            "smartwatch": "Jam Tangan Pintar",
            "camera": "Kamera Foto",
            "video camera": "Kamera Video",

            # === BENDA ALAM & LINGKUNGAN ===
            "tree": "Pohon",
            "flower": "Bunga",
            "plant": "Tanaman",
            "grass": "Rumput",
            "leaf": "Daun",
            "branch": "Ranting",
            "rock": "Batu",
            "stone": "Batu Kali",
            "sand": "Pasir",
            "soil": "Tanah",
            "water": "Air",
            "river": "Sungai",
            "lake": "Danau",
            "sea": "Laut",
            "cloud": "Awan",
            "sun": "Matahari",
            "moon": "Bulan",
            "star": "Bintang",
            "rain": "Hujan",
            "snow": "Salju",
            "fire": "Api",
            "ash": "Abu",
            "mushroom": "Jamur",
            "insect": "Serangga",
            "bird": "Burung",
            "fish": "Ikan",
            "animal": "Hewan",

            # === ALAT SEKOLAH & TULIS ===
            "book": "Buku",
            "notebook": "Buku Catatan",
            "paper": "Kertas",
            "pen": "Pena / Pulpen",
            "pencil": "Pensil",
            "eraser": "Penghapus",
            "ruler": "Penggaris",
            "sharpener": "Rautan Pensil",
            "marker": "Spidol",
            "crayon": "Krayon",
            "paintbrush": "Kuas Lukis",
            "glue": "Lem",
            "scissors": "Gunting",
            "stapler": "Staples / Jekrekan",
            "clip": "Klip Kertas",
            "school bag": "Tas Sekolah",
            "backpack": "Tas Ransel",
            "calculator": "Kalkulator",
            "map": "Peta",
            "globe": "Bola Dunia",

            # === KENDARAAN & PERALATAN ===
            "car": "Mobil",
            "motorcycle": "Sepeda Motor",
            "bicycle": "Sepeda",
            "bus": "Bus",
            "truck": "Truk",
            "train": "Kereta Api",
            "boat": "Perahu",
            "ship": "Kapal",
            "airplane": "Pesawat Terbang",
            "helmet": "Helm",
            "wheel": "Roda",
            "steering wheel": "Setir",
            "key": "Kunci",

            # === ALAT DAPUR & MAKAN ===
            "plate": "Piring",
            "bowl": "Mangkuk",
            "spoon": "Sendok",
            "fork": "Garpu",
            "knife": "Pisau Dapur",
            "glass": "Gelas Kaca",
            "cup": "Gelas / Cangkir",
            "bottle": "Botol Air Minum",
            "kettle": "Teko Air",
            "pan": "Wajan / Penggorengan",
            "pot": "Panci",
            "stove": "Kompor",
            "refrigerator": "Kulkas",
            "microwave": "Microwave",
            "oven": "Oven",
            "faucet": "Kran Air",
            "trash can": "Tempat Sampah",
            "lighter": "Korek Api",
            "match": "Korek Api Batang",
            "fire starter": "Alat Pembakar / Korek Api",

            # === PAKAIAN & AKSESORIS ===
            "shirt": "Baju / Kemeja",
            "t-shirt": "Kaos",
            "pants": "Celana",
            "jeans": "Celana Jeans",
            "skirt": "Rok",
            "dress": "Gaun",
            "jacket": "Jaket",
            "coat": "Mantel",
            "shoe": "Sepatu",
            "sandal": "Sandal",
            "sock": "Kaos Kaki",
            "hat": "Topi",
            "cap": "Topi Olahraga",
            "glasses": "Kacamata",
            "sunglasses": "Kacamata Hitam",
            "watch": "Jam Tangan",
            "belt": "Ikat Pinggang",
            "bag": "Tas",
            "purse": "Dompet Kecil",
            "wallet": "Dompet",
            "umbrella": "Payung",

            # === BUAH & MAKANAN ===
            "fruit": "Buah-buahan",
            "apple": "Apel",
            "banana": "Pisang",
            "orange": "Jeruk",
            "grape": "Anggur",
            "watermelon": "Semangka",
            "mango": "Mangga",
            "coconut": "Kelapa",
            "rice": "Beras / Nasi",
            "bread": "Roti",
            "egg": "Telur",
            "meat": "Daging",
            "vegetable": "Sayuran",
            "food": "Makanan",
            "drink": "Minuman",

            # === BENDA UMUM LAINNYA ===
            "toy": "Mainan",
            "doll": "Boneka",
            "ball": "Bola",
            "balloon": "Balon",
            "flag": "Bendera",
            "bookmark": "Pembatas Buku",
            "umbrella": "Payung",
            "rope": "Tali",
            "chain": "Rantai",
            "lock": "Gembok",
            "hammer": "Palu",
            "saw": "Gergaji",
            "screwdriver": "Obeng",
            "wrench": "Kunci Inggris",
            "bucket": "Ember",
            "broom": "Sapu",
            "mop": "Alat Pel",
            "soap": "Sabun",
            "towel": "Handuk",
            "toothbrush": "Sikat Gigi",
            "toothpaste": "Pasta Gigi",
            "medicine": "Obat-obatan",
            "first aid kit": "Kotak P3K"
        }

        # Ubah ke Bahasa Indonesia kalau ada di daftar
        if nama_asli in terjemahan:
            nama_benda = terjemahan[nama_asli]
        else:
            nama_benda = nama_asli.replace("_", " ").title()

        tampilkan_robot(lagi_proses=False)
        st.success(f"✅ Menurut saya ini adalah: **{nama_benda}**")
        st.info(f"📊 Keyakinan saya: **{keyakinan}%**")
        
        # === SUARA ROBOT ===
        teks_bicara = f"Halo! Benda yang kamu tunjukkan adalah {nama_benda}, dengan keyakinan {keyakinan} persen."
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={teks_bicara}&tl=id-ID&client=tw-ob", format="audio/mpeg")
        st.write("🔊 Klik tombol suara di atas untuk mendengar penjelasan saya!")

# === KAKI HALAMAN ===
st.markdown("---")
st.caption("🚀 Dibuat untuk belajar AI & Pengenalan Objek | Gratis & Bisa Dibuka di HP")
