#!/data/data/com.termux/files/usr/bin/bash

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  Catcast.tv Yayın Kurulum Scripti${NC}"
echo -e "${BLUE}========================================${NC}"

# 1. Depoları güncelle
echo -e "${YELLOW}[1/5] Depolar güncelleniyor...${NC}"
pkg update -y && pkg upgrade -y

# 2. Gerekli paketleri kur
echo -e "${YELLOW}[2/5] Gerekli paketler kuruluyor...${NC}"
pkg install -y python ffmpeg

# 3. Termux storage izni
echo -e "${YELLOW}[3/5] Depolama izni isteniyor...${NC}"
termux-setup-storage

# 4. Yayın scriptini oluştur
echo -e "${YELLOW}[4/5] Yayın scripti oluşturuluyor...${NC}"
cat > ~/catcast_yayin.py << 'EOF'
import subprocess
import sys
import time

# ===================== CATCAST AYARLARI =====================
RTMP_URL = "rtmp://s.catcast.tv/live"
STREAM_KEY = "mutluhub1?key=27610_50990_253571354411efe7"
rtmp_server = f"{RTMP_URL}/{STREAM_KEY}"

# ===================== YAYIN AYARLARI =====================
VIDEO_URL = "https://cdn.codenet.work/streamgo/stremgo123/4865.m3u8"
LOGO_URL = "https://raw.githubusercontent.com/mutlumedya/yayin/refs/heads/main/logo1.png"

print(f"🎬 Video Kaynağı: {VIDEO_URL}")
print(f"🎨 Logo: {LOGO_URL}")
print(f"🔑 Stream Key: {STREAM_KEY}")

# FFmpeg komutu - Logo SAĞ ÜSTTE (BÜYÜK)
command = [
    'ffmpeg',
    '-re',
    '-stream_loop', '-1',
    '-i', VIDEO_URL,
    '-i', LOGO_URL,
    '-filter_complex',
    '[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black[v0];'
    '[1:v]scale=250:70[logo];'  # 120'den 200'e çıkarıldı
    '[v0][logo]overlay=W-w-8:4[v1];'  # Logo SAĞ ÜST
    '[v1]drawtext=text=t.me/digitaltivi:fontcolor=white:fontsize=24:box=1:boxcolor=black@0.6:boxborderw=5:x=(w-text_w)/2:y=h-text_h-20[v]',
    '-map', '[v]',
    '-map', '0:a?',
    '-c:v', 'libx264',
    '-preset', 'veryfast',
    '-b:v', '4000k',
    '-c:a', 'aac',
    '-b:a', '128k',
    '-f', 'flv',
    rtmp_server
]

print("\n🎥 Catcast.tv yayını başlatılıyor...")
print("🖼️  Logo: Sağ üst (200x200 - büyük)")
print("📝 Alt yazı: t.me/digitaltivi")
print("⏸️  Durdurmak için: Ctrl + C\n")

try:
    proc = subprocess.Popen(command)
    
    # Yayını canlı tut
    while True:
        time.sleep(60)
        if proc.poll() is not None:
            print("⚠️ Yayın durdu, yeniden başlatılıyor...")
            proc = subprocess.Popen(command)
            
except KeyboardInterrupt:
    print("\n\n⛔ Yayın durduruluyor...")
    proc.terminate()
    print("✅ Yayın sonlandırıldı.")
EOF

# 5. Çalıştır
echo -e "${YELLOW}[5/5] Yayın başlatılıyor...${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✨ Kurulum tamam! Yayın başlıyor...${NC}"
echo -e "${BLUE}========================================${NC}\n"

python ~/catcast_yayin.py
