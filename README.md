# 🚀 Jagoan Hosting Free Domain Claimer

Automation script untuk claim domain gratis dari Jagoan Hosting menggunakan promo code `FREEWEBID100`.

## ✨ Features

- ✅ **Config file support** (`config.env`) - Easy customization!
- ✅ **Headless/Non-headless mode** - Toggle via config
- ✅ Multi-threading support (parallel claiming)
- ✅ **Smart domain name generator** - Cool & unique names
  - 2-word combos: "cybercore", "quantumhub" 
  - 3-word combos: "aetherluminaverse" (lebih unik!)
  - 60+ kata dalam wordlist
  - **Fast domain availability detection** - Tidak buang waktu
- ✅ Random email & data generator
- ✅ Auto-fill registration form
- ✅ Auto-apply promo code
- ✅ Auto-payment processing
- ✅ Save results ke file `results.txt`
- ✅ Logging lengkap (console + file)
- ✅ **Screenshot on error** - Auto capture kalau ada error
- ✅ Retry mechanism kalau domain taken
- ✅ Anti-detection features
- ✅ **Fully configurable delays & timeouts**

## 📋 Requirements

- Python 3.8+
- Playwright
- Internet connection
- **Windows/Linux/MacOS** support
- **VPS-ready** - Can run 24/7 on cloud servers! 🚀

---

## 🖥️ Platform Support

### Local Computer (Windows/Mac/Linux)
- ✅ Visual mode (see browser)
- ✅ Debugging friendly
- ✅ Perfect for testing

### VPS/Cloud Server (Ubuntu/Debian)
- ✅ Headless mode (no display needed)
- ✅ 24/7 automation
- ✅ Stable performance
- ✅ Mass claiming support

📖 **[VPS Deployment Guide →](VPS_DEPLOYMENT.md)**

## ⚙️ Configuration

Semua settings bisa diatur di **`config.env`**! 

**Settings penting:**
- `HEADLESS=True/False` - Show browser atau tidak
- `DEFAULT_PASSWORD` - Password default untuk semua akun
- `MAX_THREADS` - Max threads yang diperbolehkan
- `SLOW_MOTION` - Slow motion untuk debugging (ms)
- Dan banyak lagi!

📖 **Baca [CONFIG_GUIDE.md](CONFIG_GUIDE.md) untuk penjelasan lengkap semua settings**

### Quick Config Examples:

**Untuk testing (first time):**
```env
HEADLESS=False
SLOW_MOTION=100
MAX_THREADS=1
```

**Untuk production (mass claiming):**
```env
HEADLESS=True
SLOW_MOTION=0
MAX_THREADS=5
```

## 🔧 Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
python -m playwright install chromium
```

**Atau pakai setup.bat (Windows):**
```bash
setup.bat
```

## 🚀 Usage

Jalankan script:
```bash
python domain_claimer.py
```

Script akan menanyakan:
1. **Jumlah threads** (1-10): Berapa browser yang mau jalan parallel
2. **Total domains**: Berapa total domain yang mau di-claim
3. **Password**: Password untuk semua akun (default: `JagoanDomain2024!`)

### Contoh:

```
Berapa jumlah threads yang mau dijalankan? (1-10): 3
Berapa total domain yang mau di-claim? 10
Masukkan password untuk semua akun (default: JagoanDomain2024!): MyPassword123

📊 Konfigurasi:
   - Threads: 3
   - Total domains: 10
   - Domains per thread: 3
   - Password: MyPassword123
   - Results file: results.txt

⏳ Starting automation...
```

## 📁 Output

Results disimpan di `results.txt` dengan format:
```
email@example.com:cooldomainname.web.id
random123@gmail.com:techzone99.web.id
user456@yahoo.com:cybernode.web.id
```

## 📝 Logs

- Console output: Real-time progress
- `domain_claimer.log`: Detailed logs untuk debugging

## ⚙️ Flow

1. Generate random domain name yang cool
2. Buka halaman domain search
3. Check availability → Klik "Tambah ke keranjang"
4. Klik "Lanjut"
5. Input promo code `FREEWEBID100` → Klik "Pakai Promo"
6. Pilih "Saya belum punya akun"
7. Fill form registration (email, phone, nama, password)
8. Klik "Register"
9. Klik "Bayar Sekarang"
10. Wait for payment success
11. Save hasil ke file

## 🎯 Domain Name Generator

Script akan generate domain name yang cool dengan kombinasi:
- **Single word + number**: `cyber123`, `nexus99`, `quantum42`
- **Two words combo**: `techzone`, `cybernode`, `smartcode`

## 📧 Email & Data Generator

- **Email**: Random 8 karakter + angka @ (gmail/yahoo/outlook/hotmail)
- **Nama**: Random nama Indonesia yang simple
- **Phone**: Random nomor Indonesia (format: 812XXXXXXXX)
- **Password**: Fixed untuk semua akun (sesuai input user)

## ⚠️ Notes

- **Edit `config.env`** untuk ubah settings (headless, delays, dll)
- Script menggunakan headless browser by default (tidak terlihat)
- Untuk **liat browser**, set `HEADLESS=False` di config.env
- Setiap thread = 1 browser instance
- Delay otomatis untuk anti-detection
- Retry otomatis kalau domain taken
- Safe error handling
- **Screenshot auto-capture** kalau ada error (di folder `screenshots/`)

## 📝 Files Generated

- **`results.txt`** - Hasil claiming (email:domain)
- **`domain_claimer.log`** - Detailed logs
- **`screenshots/`** - Screenshot errors (kalau SCREENSHOT_ON_ERROR=True)

## 🐛 Troubleshooting

**Error: "Playwright not found"**
```bash
pip install playwright
python -m playwright install chromium
```

**Error: "Domain not available"**
- Script akan otomatis retry dengan domain baru

**Slow performance**
- Kurangi jumlah threads
- Check internet connection

## 📊 Performance

- **1 thread**: ~2-3 menit per domain
- **5 threads**: ~3-5 menit untuk 10 domains
- **10 threads**: ~5-7 menit untuk 20 domains

## 🔒 Security

- Password fixed untuk semua akun (easy management)
- Email random untuk setiap domain
- No credential stored in code
- Results saved locally

## 📞 Support

Kalau ada error atau butuh customization, tinggal modify script sesuai kebutuhan!

---

Made with ❤️ for claiming free domains
