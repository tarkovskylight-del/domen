# 📝 Config Guide - config.env

Semua settings automation ada di file `config.env`. Edit file ini sesuai kebutuhan kamu!

## 🎯 Settings Penting

### HEADLESS (Default: True)
```env
HEADLESS=True   # Browser jalan di background (gak keliatan)
HEADLESS=False  # Browser keliatan (buat debugging/nonton proses)
```

**Kapan pakai False?**
- Waktu testing pertama kali
- Waktu debugging kalau ada error
- Waktu mau liat step-by-step prosesnya

**Kapan pakai True?**
- Waktu production (claim banyak domain)
- Lebih cepat & resource-efficient
- Gak butuh nonton prosesnya

### DEFAULT_PASSWORD
```env
DEFAULT_PASSWORD=JagoanDomain2024!
```
Password default yang akan dipake untuk semua akun (bisa diubah saat run)

### PROMO_CODE
```env
PROMO_CODE=FREEWEBID100
```
Kode promo yang akan di-apply otomatis

---

## ⏱️ Delays & Timeouts

### AFTER_CLICK_DELAY (Default: 2)
Delay dalam **detik** setelah klik button
```env
AFTER_CLICK_DELAY=2  # Standard
AFTER_CLICK_DELAY=3  # Kalau koneksi lambat
AFTER_CLICK_DELAY=1  # Kalau koneksi cepat
```

### ELEMENT_TIMEOUT (Default: 10)
Berapa lama menunggu element muncul (dalam **detik**)
```env
ELEMENT_TIMEOUT=10  # Standard
ELEMENT_TIMEOUT=15  # Kalau website sering lambat
```

### PAGE_TIMEOUT (Default: 30)
Timeout untuk load halaman (dalam **detik**)
```env
PAGE_TIMEOUT=30  # Standard
PAGE_TIMEOUT=45  # Untuk koneksi lambat
```

### PAYMENT_TIMEOUT (Default: 45)
Timeout khusus untuk konfirmasi pembayaran (dalam **detik**)
```env
PAYMENT_TIMEOUT=45  # Standard (proses payment bisa lambat)
PAYMENT_TIMEOUT=60  # Untuk koneksi sangat lambat
PAYMENT_TIMEOUT=30  # Kalau yakin koneksi cepat
```

**Note:** Payment timeout lebih lama dari timeout biasa karena proses pembayaran membutuhkan waktu loading ekstra

---

## 🧵 Thread Settings

### MAX_THREADS (Default: 10)
Maksimal threads yang diperbolehkan
```env
MAX_THREADS=10  # Maksimal 10 browser parallel
MAX_THREADS=5   # Lebih aman, untuk PC biasa
```

**Rekomendasi:**
- PC biasa: 3-5 threads
- PC kencang: 5-10 threads
- Koneksi lambat: 2-3 threads

---

## 🔄 Retry Settings

### MAX_RETRIES (Default: 2)
Berapa kali retry kalau domain taken atau error
```env
MAX_RETRIES=2  # Retry 2x per domain
MAX_RETRIES=3  # Lebih banyak retry
MAX_RETRIES=1  # Lebih cepat, tapi less forgiving
```

---

## 🐛 Debugging Settings

### SLOW_MOTION (Default: 0)
Slow motion dalam **milliseconds** (ms) - untuk debugging
```env
SLOW_MOTION=0     # Full speed (production)
SLOW_MOTION=100   # Slow untuk debugging
SLOW_MOTION=500   # Super slow, bisa liat tiap step
```

**Pakai slow motion kalau:**
- HEADLESS=False (lagi nonton browser)
- Mau liat detail tiap step
- Debugging masalah tertentu

### SCREENSHOT_ON_ERROR (Default: True)
Auto screenshot kalau ada error
```env
SCREENSHOT_ON_ERROR=True   # Auto screenshot saat error
SCREENSHOT_ON_ERROR=False  # No screenshot
```

Screenshots disimpan di folder `screenshots/`

### BROWSER_CONSOLE_LOGS (Default: False)
Show console logs dari browser
```env
BROWSER_CONSOLE_LOGS=False  # Normal (recommended)
BROWSER_CONSOLE_LOGS=True   # Show semua console logs (debugging)
```

---

## 📁 Files Settings

### RESULTS_FILE (Default: results.txt)
File untuk save hasil
```env
RESULTS_FILE=results.txt
RESULTS_FILE=domains_$(date).txt
```

### LOG_FILE (Default: domain_claimer.log)
File untuk logs
```env
LOG_FILE=domain_claimer.log
LOG_FILE=logs/claimer.log
```

---

## 💡 Contoh Konfigurasi

### Untuk Testing (First Time)
```env
HEADLESS=False
SLOW_MOTION=100
SCREENSHOT_ON_ERROR=True
MAX_THREADS=1
AFTER_CLICK_DELAY=3
```

### Untuk Production (Mass Claiming)
```env
HEADLESS=True
SLOW_MOTION=0
SCREENSHOT_ON_ERROR=True
MAX_THREADS=5
AFTER_CLICK_DELAY=2
```

### Untuk Koneksi Lambat
```env
HEADLESS=True
MAX_THREADS=2
AFTER_CLICK_DELAY=3
ELEMENT_TIMEOUT=15
PAGE_TIMEOUT=45
```

### Untuk Debugging Error
```env
HEADLESS=False
SLOW_MOTION=500
SCREENSHOT_ON_ERROR=True
BROWSER_CONSOLE_LOGS=True
MAX_THREADS=1
```

---

## 🎨 Tips

1. **Mulai dengan HEADLESS=False** untuk liat flow pertama kali
2. **Kalau udah yakin**, ubah ke HEADLESS=True untuk mass claiming
3. **Adjust delays** sesuai speed koneksi kamu
4. **Screenshot on error** sangat berguna untuk debugging
5. **Jangan terlalu banyak threads** kalau koneksi/PC lemah

---

## ⚡ Quick Changes

**Mau liat browser?**
```env
HEADLESS=False
```

**Mau lebih cepat?**
```env
AFTER_CLICK_DELAY=1
MIN_DELAY_BETWEEN_ATTEMPTS=1
MAX_DELAY_BETWEEN_ATTEMPTS=2
```

**Mau lebih aman?**
```env
AFTER_CLICK_DELAY=3
MAX_RETRIES=3
ELEMENT_TIMEOUT=15
```

**Lagi debug error?**
```env
HEADLESS=False
SLOW_MOTION=100
SCREENSHOT_ON_ERROR=True
MAX_THREADS=1
```

---

Setelah edit `config.env`, tinggal run ulang script:
```bash
python domain_claimer.py
```

Config akan auto-reload! 🚀
