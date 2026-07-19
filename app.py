import gradio as gr
from ultralytics import YOLO

# Muat model ringan yang sudah dilatih
model = YOLO("yolov8n.pt")  # Bisa ganti model khusus alat TKJ nanti

def deteksi_alat(foto):
    hasil = model.predict(foto, conf=0.6)
    nama_alat = []
    for benda in hasil[0].boxes:
        nama = model.names[int(benda.cls[0])]
        nama_alat.append(f"✅ {nama} ({round(float(benda.conf[0])*100,1)}%)")
    return "\n".join(nama_alat) if nama_alat else "Benda tidak terdeteksi, coba foto lebih jelas"

# Tampilan aplikasi
antarmuka = gr.Interface(
    fn=deteksi_alat,
    inputs=gr.Image(type="filepath", label="📸 Foto Alat TKJ"),
    outputs="text",
    title="🤖 AI Penebak Alat TKJ",
    description="Foto alat jaringan, saya akan sebutkan namanya!"
)

antarmuka.launch()
