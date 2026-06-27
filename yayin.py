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
import threading

# ===================== CATCAST AYARLARI =====================
RTMP_URL = "rtmp://s.catcast.tv/live"

# ===================== YAYIN TANIMLARI =====================
# Her yayın için ayrı stream key ve video URL
streams = [
    {
        "name": "Yayın 1",
        "stream_key": "mutluhub1?key=27610_50990_253571354411efe7",
        "video_url": "https://cdn.codenet.work/streamgo/stremgo123/4864.m3u8"
    },
    {
        "name": "Yayın 2",
        "stream_key": "mutluhub2?key=27610_50991_253571354411efe8",  # Değiştir
        "video_url": "https://cdn.codenet.work/streamgo/stremgo123/4865.m3u8"  # Değiştir
    },
    {
        "name": "Yayın 3",
        "stream_key": "mutluhub3?key=27610_50992_253571354411efe9",  # Değiştir
        "video_url": "https://cdn.codenet.work/streamgo/stremgo123/4866.m3u8"  # Değiştir
    }
]

# ===================== ORTAK AYARLAR =====================
LOGO_URL = "https://raw.githubusercontent.com/mutlumedya/yayin/refs/heads/main/logo.png"
TEXT = "t.me/digitaltivi"
FONT_SIZE = 24

def start_stream(stream_config):
    """Tek bir yayını başlat"""
    rtmp_server = f"{RTMP_URL}/{stream_config['stream_key']}"
    
    print(f"🎬 {stream_config['name']} başlatılıyor...")
    print(f"   Video: {stream_config['video_url']}")
    print(f"   Stream Key: {stream_config['stream_key'][:20]}... (gizli)")
    
    # FFmpeg komutu - Logo SAĞ ÜSTTE
    command = [
        'ffmpeg',
        '-re',
        '-stream_loop', '-1',
        '-i', stream_config['video_url'],
        '-i', LOGO_URL,
        '-filter_complex',
        '[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black[v0];'
        '[1:v]scale=250:80[logo];'
        '[v0][logo]overlay=W-w-8:3[v1];'
        f'[v1]drawtext=text={TEXT}:fontcolor=white:fontsize={FONT_SIZE}:box=1:boxcolor=black@0.6:boxborderw=5:x=(w-text_w)/2:y=h-text_h-20[v]',
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
    
    try:
        proc = subprocess.Popen(command)
        while True:
            time.sleep(60)
            if proc.poll() is not None:
                print(f"⚠️ {stream_config['name']} durdu, yeniden başlatılıyor...")
                proc = subprocess.Popen(command)
    except KeyboardInterrupt:
        print(f"\n⛔ {stream_config['name']} durduruluyor...")
        proc.terminate()

# ===================== TÜM YAYINLARI BAŞLAT =====================
print("=" * 50)
print(f"📺 {len(streams)} Yayın Başlatılıyor")
print("=" * 50)
print(f"🎨 Logo: {LOGO_URL}")
print(f"📝 Alt yazı: {TEXT}")
print("=" * 50)

threads = []
for stream in streams:
    thread = threading.Thread(target=start_stream, args=(stream,))
    thread.daemon = True
    thread.start()
    threads.append(thread)
    time.sleep(2)  # Her yayın arasında 2 saniye bekle

print(f"\n✅ {len(streams)} yayın başlatıldı!")
print("⏸️  Durdurmak için: Ctrl + C\n")

try:
    # Ana thread'i canlı tut
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("\n\n⛔ Tüm yayınlar durduruluyor...")
    print("✅ Yayınlar sonlandırıldı.")
EOF

# 5. Çalıştır
echo -e "${YELLOW}[5/5] Yayın başlatılıyor...${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✨ Kurulum tamam! Yayın başlıyor...${NC}"
echo -e "${BLUE}========================================${NC}\n"

python ~/catcast_yayin.py
