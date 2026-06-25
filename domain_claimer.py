"""
Jagoan Hosting Free Domain Claimer
Multi-threaded automation script using Playwright
"""

import asyncio
import random
import string
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import logging
from pathlib import Path
import requests

# Load configuration from config.env
def load_config():
    """Load configuration from config.env file"""
    config = {}
    config_file = Path(__file__).parent / "config.env"
    
    if not config_file.exists():
        print(f"⚠️  Warning: config.env not found, using defaults")
        return get_default_config()
    
    with open(config_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Convert boolean strings
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                # Convert numbers
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit():
                    value = float(value)
                
                config[key] = value
    
    return config

def get_default_config():
    """Default configuration values"""
    return {
        'HEADLESS': True,
        'WINDOW_WIDTH': 1920,
        'WINDOW_HEIGHT': 1080,
        'DEFAULT_PASSWORD': 'JagoanDomain2024!',
        'PROMO_CODE': 'FREEMYID100',
        'DOMAIN_EXTENSION': 'my.id',
        'RESULTS_FILE': 'results.txt',
        'LOG_FILE': 'domain_claimer.log',
        'AFTER_CLICK_DELAY': 2,
        'AFTER_FORM_FILL_DELAY': 1,
        'ELEMENT_TIMEOUT': 10,
        'PAGE_TIMEOUT': 30,
        'PAYMENT_TIMEOUT': 30,
        'MIN_DELAY_BETWEEN_ATTEMPTS': 2,
        'MAX_DELAY_BETWEEN_ATTEMPTS': 4,
        'MAX_THREADS': 10,
        'MAX_RETRIES': 2,
        'SLOW_MOTION': 0,
        'BROWSER_CONSOLE_LOGS': False,
        'SCREENSHOT_ON_ERROR': True,
        'SCREENSHOT_FOLDER': 'screenshots',
        'TELEGRAM_BOT_TOKEN': '',
        'TELEGRAM_CHAT_ID': ''
    }

# Load configuration
CONFIG = load_config()

# Setup logging with UTF-8 encoding to handle emojis
class UTF8StreamHandler(logging.StreamHandler):
    """Custom handler that uses UTF-8 encoding for console output"""
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            # Remove emojis for Windows console compatibility
            msg = msg.encode('ascii', 'ignore').decode('ascii')
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG.get('LOG_FILE', 'domain_claimer.log'), encoding='utf-8'),
        UTF8StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "https://beli.jagoanhosting.com/domain-murah"
PROMO_CODE = CONFIG.get('PROMO_CODE', 'FREEMYID100')
DOMAIN_EXTENSION = CONFIG.get('DOMAIN_EXTENSION', 'my.id').strip().lstrip('.')
RESULTS_FILE = CONFIG.get('RESULTS_FILE', 'results.txt')
FIXED_PASSWORD = CONFIG.get('DEFAULT_PASSWORD', 'JagoanDomain2024!')


def send_telegram(message: str):
    """Send a message to Telegram. Silently skip if token/chat_id not set."""
    token = CONFIG.get('TELEGRAM_BOT_TOKEN', '').strip()
    chat_id = CONFIG.get('TELEGRAM_CHAT_ID', '').strip()
    if not token or not chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        resp = requests.post(url, json=payload, timeout=10)
        if not resp.ok:
            logger.warning(f"Telegram send failed: {resp.status_code} {resp.text}")
    except Exception as e:
        logger.warning(f"Telegram error: {e}")

# Domain wordlists — pakai kata2 yang jarang / unik / niche
# Hindari kata generik yang udah pasti diclaim (toko, jaya, cyber, hub, dll)

WORDS_A = [
    # English — unik, jarang dijadiin domain
    "obsidian", "cobalt", "indigo", "quartz", "onyx", "amber", "zircon",
    "cerium", "helium", "argon", "krypton", "xenon", "neon", "radon",
    "photon", "proton", "neutron", "meson", "boson", "quark", "lepton",
    "tachyon", "chronon", "magnon", "phonon", "exciton", "polaron",
    "vortex", "helix", "fractal", "entropy", "synapse", "cortex",
    "axon", "dendrite", "myelin", "neuron", "ganglion", "plexus",
    "stratum", "laminar", "turbine", "cyclone", "typhoon", "zephyr",
    "nimbus", "cirrus", "cumulus", "stratus", "aurora", "solstice",
    "equinox", "perihelion", "aphelion", "zenith", "nadir", "azimuth",
    "parallax", "refraction", "diffraction", "dispersion", "prism",
    "lattice", "matrix", "tensor", "vector", "scalar", "gradient",
    "diverge", "converge", "tangent", "secant", "cosine", "radiant",
    "lumen", "candela", "kelvin", "pascal", "joule", "farad", "ohmic",
    "gauss", "tesla", "weber", "henry", "siemen", "coulomb", "ampere",
    "wyvern", "gryphon", "chimera", "basilisk", "kraken", "leviathan",
    "behemoth", "juggernaut", "colossus", "monolith", "obelisk", "spire",
    "citadel", "rampart", "bastion", "bulwark", "parapet", "crenate",
    "labyrinth", "catacombs", "sanctum", "vestibule", "portico", "atrium",
    # Indonesian — bukan yg generik
    "kencana", "kumala", "wahana", "wahyu", "waskita", "widya", "windu",
    "wiraga", "wisesa", "wisnu", "yudha", "yuga", "yudhis", "adikara",
    "adiguna", "adiluhung", "adhikarya", "adiwira", "adikarsa", "adidaya",
    "bhaskara", "bimantara", "brawijaya", "cendekia", "candrakanta",
    "darpala", "darwis", "dayatama", "digdaya", "dirgantara", "dwikarsa",
    "erlangga", "eskalasi", "etalase", "etanola", "ewangga", "fadillah",
    "galaksi", "galatama", "galgala", "ganesha", "ganendra", "ganestha",
    "hastaguna", "hastabrata", "hayunara", "helanca", "hermina", "hidayat",
    "ikalino", "ikamaya", "ikasatria", "imajinasi", "imbangan", "inovata",
    "jalabumi", "jalakarsa", "jalapratama", "jalasena", "jalatama",
    "kahuripan", "kalimaya", "kalingga", "karisma", "karuhun", "kasatmata",
    "kendali", "kencono", "kenthongan", "kepodang", "kerabat", "keraton",
    "laksamana", "langkawi", "laraska", "latansa", "lavesta", "lembayung",
    "madhura", "mahardika", "mahkota", "maharani", "mahasurya", "mahavira",
    "nararya", "narayana", "narendra", "narmada", "narpati", "nasiruna",
    "pahala", "palagan", "palguna", "palimanan", "panakawan", "pandhita",
    "rajendra", "raksasa", "ramanda", "rangkuti", "ranjana", "rantepao",
    "sabdatama", "sabrang", "sahasika", "samodra", "sampurna", "sancaya",
    "tagarela", "tajakusuma", "talenta", "talisma", "tamansari", "tandika",
    "udayana", "ugrasena", "ujwalata", "upadesa", "upakara", "upasara",
    "vaibhava", "vajrayana", "vanabara", "vandana", "varuna", "vasudeva",
    "wahyuning", "walidata", "wanabakti", "wandira", "wangsapati", "wardaya",
    "yatmaka", "yayasan", "yogabrata", "yogakarta", "yogananda", "yuddhistira",
    "zaituna", "zamzami", "zaneta", "zarindra", "zastrouw", "zulkarnain"
]

WORDS_B = [
    # English suffix — jarang dipakai
    "rift", "vale", "glen", "cove", "fjord", "atoll", "lagoon", "geyser",
    "tundra", "steppe", "savanna", "taiga", "canyon", "ravine", "gorge",
    "escarp", "plateau", "caldera", "isthmus", "peninsula", "archipelago",
    "soleil", "lumiere", "ombre", "eclat", "mirage", "oasis", "zenith",
    "noctis", "lunaris", "solaris", "astralis", "celestis", "ethereal",
    "cryptis", "nexalis", "fluxion", "syntaxis", "paradox", "catalyst",
    "alembic", "crucible", "retort", "amalgam", "alloy", "carbide",
    "silicate", "titanate", "ferrite", "garnite", "pyrite", "calcite",
    "basalt", "granite", "diorite", "gabbro", "pumice", "obsidite",
    "codex", "grimoire", "lexicon", "compendium", "annals", "chronicle",
    "palimpsest", "folio", "quire", "fascicle", "canto", "strophe",
    "theorem", "axiom", "lemma", "corollary", "postulate", "conjecture",
    "mantra", "sutra", "tantra", "dharma", "karma", "nirvana", "moksha",
    "prana", "chakra", "mudra", "yantra", "bardo", "dharani", "samadhi",
    # Indonesian suffix — spesifik bukan generik
    "wangi", "asri", "elok", "indah", "permai", "cantik", "molek",
    "agung", "mulia", "luhur", "tinggi", "megah", "gagah", "perkasa",
    "paripurna", "sempurna", "purna", "saksama", "teliti", "cermat",
    "wicaksana", "bijaksana", "arif", "pandai", "cendekia", "pintar",
    "wirausaha", "wirawan", "pejuang", "penegak", "pembela", "pengayom",
    "cahyaning", "suharto", "soeharto", "suwardi", "sukarno", "suryadi",
    "nirmala", "nirmana", "nirwana", "nirwasita", "nirsabda", "nirlaba",
    "pratama", "perdana", "pertama", "utama", "wahana", "wiyata", "widyata"
]

EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]

class DomainClaimer:
    def __init__(self, thread_id: int, total_domains: int, password: str):
        self.thread_id = thread_id
        self.total_domains = total_domains
        self.password = password
        self.success_count = 0
        
    def generate_cool_domain(self) -> str:
        """Generate highly unique domain — rare words + optional number suffix"""
        w1 = random.choice(WORDS_A)
        w2 = random.choice(WORDS_B)
        while w1.lower() == w2.lower():
            w2 = random.choice(WORDS_B)

        base = f"{w1}{w2}"

        # 40% chance: tambah 1-2 digit di akhir domain biar makin unik
        if random.random() < 0.4:
            digits = random.randint(1, 2)
            num = random.randint(10 ** (digits - 1) if digits > 1 else 1, 10 ** digits - 1)
            base = f"{base}{num}"

        return base

    def generate_random_name(self) -> str:
        """Generate simple random name"""
        first_names = ["Agus", "Budi", "Citra", "Dewi", "Eko", "Fitri", "Guntur", 
                       "Hana", "Indra", "Joko", "Kiki", "Linda", "Maya", "Novi"]
        last_names = ["Santoso", "Pratama", "Wijaya", "Kusuma", "Putra", "Putri",
                      "Saputra", "Wati", "Kurniawan", "Sari"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def generate_random_email(self, domain_name: str = '') -> str:
        """Generate email based on domain name + random numbers (natural-looking)"""
        base = domain_name.lower() if domain_name else ''.join(random.choices(string.ascii_lowercase, k=6))
        num_digits = random.randint(1, 3)
        number = random.randint(10 ** (num_digits - 1) if num_digits > 1 else 1, 10 ** num_digits - 1)
        mail_domain = random.choice(EMAIL_DOMAINS)
        return f"{base}{number}@{mail_domain}"
    
    def generate_phone_number(self) -> str:
        """Generate random Indonesian phone number (without +62)"""
        # Format: 812-3456-7890
        prefix = random.choice(['812', '813', '821', '822', '823', '851', '852', '853'])
        middle = ''.join(random.choices(string.digits, k=4))
        last = ''.join(random.choices(string.digits, k=4))
        return f"{prefix}{middle}{last}"
    
    async def claim_domain(self, domain_name: str) -> dict:
        """Main function to claim a single domain"""
        logger.info(f"[Thread-{self.thread_id}] Starting claim for: {domain_name}.{DOMAIN_EXTENSION}")
        
        # Create screenshot folder if needed
        if CONFIG.get('SCREENSHOT_ON_ERROR'):
            screenshot_folder = Path(CONFIG.get('SCREENSHOT_FOLDER', 'screenshots'))
            screenshot_folder.mkdir(exist_ok=True)
        
        async with async_playwright() as p:
            # Launch browser with config settings
            browser = await p.chromium.launch(
                headless=CONFIG.get('HEADLESS', True),
                slow_mo=CONFIG.get('SLOW_MOTION', 0),
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context(
                viewport={
                    'width': CONFIG.get('WINDOW_WIDTH', 1920),
                    'height': CONFIG.get('WINDOW_HEIGHT', 1080)
                },
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            page = await context.new_page()
            
            # Enable console logs if configured
            if CONFIG.get('BROWSER_CONSOLE_LOGS'):
                page.on("console", lambda msg: logger.debug(f"Browser console: {msg.text}"))
            
            try:
                # Step 1: Navigate to domain search page
                url = f"{BASE_URL}?domain={domain_name}.{DOMAIN_EXTENSION}"
                logger.info(f"[Thread-{self.thread_id}] Navigating to: {url}")
                await page.goto(url, wait_until='networkidle', timeout=CONFIG.get('PAGE_TIMEOUT', 30) * 1000)
                await asyncio.sleep(CONFIG.get('AFTER_CLICK_DELAY', 2))
                
                # Step 2: Check if domain is available and click "Tambah ke keranjang"
                logger.info(f"[Thread-{self.thread_id}] Checking domain availability...")
                
                # Wait for page to load and check availability
                await asyncio.sleep(2)
                
                # Check for "Tambah ke keranjang" button (means domain is available)
                try:
                    cart_button = page.locator('button:has-text("Tambah ke keranjang")').first
                    await cart_button.wait_for(state='visible', timeout=CONFIG.get('ELEMENT_TIMEOUT', 10) * 1000)
                    
                    # Domain is available!
                    logger.info(f"[Thread-{self.thread_id}] Domain {domain_name}.{DOMAIN_EXTENSION} is available!")
                    await cart_button.click()
                    logger.info(f"[Thread-{self.thread_id}] Clicked 'Tambah ke keranjang'")
                    await asyncio.sleep(CONFIG.get('AFTER_CLICK_DELAY', 2))
                    
                except Exception as e:
                    # Button not found - check if it's because domain is not available
                    # Look for "Domain tidak tersedia" text specifically in the domain row
                    try:
                        domain_unavailable_text = page.locator('text=Domain tidak tersedia').first
                        if await domain_unavailable_text.is_visible(timeout=2000):
                            logger.warning(f"[Thread-{self.thread_id}] Domain {domain_name}.{DOMAIN_EXTENSION} is not available")
                            return {"success": False, "error": "Domain not available"}
                    except:
                        pass
                    
                    logger.warning(f"[Thread-{self.thread_id}] Could not find cart button - domain might not be available or page error")
                    return {"success": False, "error": "Domain not available or page error"}
                
                # Step 3: Wait for "Berhasil ditambah" and click "Lanjut"
                logger.info(f"[Thread-{self.thread_id}] Waiting for success message...")
                await page.wait_for_selector('text=Berhasil ditambah', timeout=CONFIG.get('ELEMENT_TIMEOUT', 10) * 1000)
                
                lanjut_button = page.locator('button:has-text("Lanjut")').first
                await lanjut_button.click()
                logger.info(f"[Thread-{self.thread_id}] Clicked 'Lanjut' button")
                await asyncio.sleep(CONFIG.get('AFTER_CLICK_DELAY', 2) + 1)
                
                # Step 4: Fill promo code
                logger.info(f"[Thread-{self.thread_id}] Applying promo code...")
                promo_input = page.locator('input[placeholder="Masukkan Kode Promo"]')
                await promo_input.fill(PROMO_CODE)
                
                promo_button = page.locator('button:has-text("Pakai Promo")')
                await promo_button.click()
                logger.info(f"[Thread-{self.thread_id}] Applied promo code: {PROMO_CODE}")
                await asyncio.sleep(CONFIG.get('AFTER_CLICK_DELAY', 2) + 1)
                
                # Step 5: Click "Saya belum punya akun"
                logger.info(f"[Thread-{self.thread_id}] Selecting 'Saya belum punya akun'...")
                register_radio = page.locator('input[type="radio"][value="register"]')
                await register_radio.click()
                await asyncio.sleep(CONFIG.get('AFTER_CLICK_DELAY', 2))
                
                # Step 6: Fill registration form
                logger.info(f"[Thread-{self.thread_id}] Filling registration form...")
                email = self.generate_random_email(domain_name)
                phone = self.generate_phone_number()
                name = self.generate_random_name()
                
                # Fill form fields
                await page.locator('input[name="email"]').last.fill(email)
                await page.locator('input[name="telepon"]').fill(phone)
                await page.locator('input[name="nama"]').fill(name)
                await page.locator('input[name="password"]').last.fill(self.password)
                
                logger.info(f"[Thread-{self.thread_id}] Form filled - Email: {email}, Name: {name}")
                await asyncio.sleep(CONFIG.get('AFTER_FORM_FILL_DELAY', 1))
                
                # Click Register button (use more specific selector to avoid "Register with Google")
                register_button = page.locator('button.col-span-full:has-text("Register")').first
                await register_button.click()
                logger.info(f"[Thread-{self.thread_id}] Clicked 'Register' button")
                await asyncio.sleep(CONFIG.get('AFTER_CLICK_DELAY', 2) + 6)
                
                # Step 7: Wait for account info and click "Bayar Sekarang"
                logger.info(f"[Thread-{self.thread_id}] Waiting for account confirmation...")
                await page.wait_for_selector('text=Informasi Akun Pemesan', timeout=CONFIG.get('ELEMENT_TIMEOUT', 10) * 1000 + 5000)
                await asyncio.sleep(3) # Extra delay to ensure registration and session settle down
                
                bayar_button = page.locator('button:has-text("Bayar Sekarang")').last
                await bayar_button.click()
                logger.info(f"[Thread-{self.thread_id}] Clicked 'Bayar Sekarang'")
                await asyncio.sleep(CONFIG.get('AFTER_CLICK_DELAY', 2) + 3)
                
                # Step 8: Wait for payment success
                logger.info(f"[Thread-{self.thread_id}] Waiting for payment confirmation...")
                
                # Check for success indicators - wait for the payment-paid page URL pattern or success text
                try:
                    # Wait for either URL pattern or success text indicator
                    # The success page has URL like: page=payment-paid
                    # And contains text "Pembayaran Berhasil" or "PAID"
                    payment_timeout = CONFIG.get('PAYMENT_TIMEOUT', 45) * 1000
                    
                    try:
                        # Try waiting for URL first (faster)
                        await page.wait_for_url("**/beon_custom_payment**page=payment-paid**", timeout=payment_timeout)
                    except PlaywrightTimeout:
                        # Fallback: check for success text indicators
                        await page.wait_for_selector('text=Pembayaran Berhasil', timeout=10000)
                    
                    logger.info(f"[Thread-{self.thread_id}] [SUCCESS] Payment successful!")
                    
                    # Save result
                    result = {
                        "success": True,
                        "email": email,
                        "domain": f"{domain_name}.{DOMAIN_EXTENSION}",
                        "password": self.password,
                        "name": name,
                        "phone": phone
                    }
                    
                    self.save_result(result)
                    self.success_count += 1
                    
                    return result
                    
                except PlaywrightTimeout:
                    logger.warning(f"[Thread-{self.thread_id}] Payment confirmation timeout")
                    if CONFIG.get('SCREENSHOT_ON_ERROR'):
                        screenshot_path = Path(CONFIG.get('SCREENSHOT_FOLDER', 'screenshots')) / f"error_thread{self.thread_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        await page.screenshot(path=str(screenshot_path))
                        logger.info(f"[Thread-{self.thread_id}] Screenshot saved: {screenshot_path}")
                    return {"success": False, "error": "Payment timeout"}
                
            except Exception as e:
                logger.error(f"[Thread-{self.thread_id}] Error: {str(e)}")
                if CONFIG.get('SCREENSHOT_ON_ERROR'):
                    try:
                        screenshot_path = Path(CONFIG.get('SCREENSHOT_FOLDER', 'screenshots')) / f"error_thread{self.thread_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        await page.screenshot(path=str(screenshot_path))
                        logger.info(f"[Thread-{self.thread_id}] Screenshot saved: {screenshot_path}")
                    except:
                        pass
                return {"success": False, "error": str(e)}
            
            finally:
                await browser.close()
    
    def save_result(self, result: dict):
        """Save successful result to file and notify via Telegram"""
        if result.get("success"):
            line = f"{result['email']}:{result['domain']}"
            with open(RESULTS_FILE, 'a', encoding='utf-8') as f:
                f.write(line + "\n")
            logger.info(f"[Thread-{self.thread_id}] [SAVED] {line}")

            # Telegram notification
            msg = f"<code>{result['email']}:{result['domain']}</code>"
            send_telegram(msg)
    
    async def run(self):
        """Run the claiming process"""
        for i in range(self.total_domains):
            domain_name = self.generate_cool_domain()
            logger.info(f"[Thread-{self.thread_id}] Attempt {i+1}/{self.total_domains}")
            
            result = await self.claim_domain(domain_name)
            
            # Retry logic
            retries = 0
            while not result.get("success") and retries < CONFIG.get('MAX_RETRIES', 2):
                retries += 1
                logger.warning(f"[Thread-{self.thread_id}] Failed (retry {retries}/{CONFIG.get('MAX_RETRIES', 2)}), trying with new domain...")
                domain_name = self.generate_cool_domain()
                result = await self.claim_domain(domain_name)
            
            # Small delay between attempts
            delay = random.uniform(
                CONFIG.get('MIN_DELAY_BETWEEN_ATTEMPTS', 2),
                CONFIG.get('MAX_DELAY_BETWEEN_ATTEMPTS', 4)
            )
            await asyncio.sleep(delay)
        
        logger.info(f"[Thread-{self.thread_id}] Completed! Success: {self.success_count}/{self.total_domains}")


async def run_thread(thread_id: int, domains_per_thread: int, password: str):
    """Run a single thread"""
    claimer = DomainClaimer(thread_id, domains_per_thread, password)
    await claimer.run()


async def main():
    """Main entry point"""
    print("=" * 60)
    print("🚀 JAGOAN HOSTING FREE DOMAIN CLAIMER")
    print("=" * 60)
    print()
    
    # Show current config
    tg_status = "✅ Aktif" if CONFIG.get('TELEGRAM_BOT_TOKEN', '').strip() else "❌ Tidak dikonfigurasi"
    print("⚙️  Current Configuration:")
    print(f"   - Headless mode: {CONFIG.get('HEADLESS')}")
    print(f"   - Promo code: {CONFIG.get('PROMO_CODE')}")
    print(f"   - Results file: {CONFIG.get('RESULTS_FILE')}")
    print(f"   - Screenshot on error: {CONFIG.get('SCREENSHOT_ON_ERROR')}")
    print(f"   - Telegram notif: {tg_status}")
    print(f"   💡 Edit config.env untuk ubah settings")
    print()
    
    # Get user input
    try:
        num_threads = int(input(f"Berapa jumlah threads yang mau dijalankan? (1-{CONFIG.get('MAX_THREADS', 10)}): "))
        if num_threads < 1 or num_threads > CONFIG.get('MAX_THREADS', 10):
            print(f"❌ Thread harus antara 1-{CONFIG.get('MAX_THREADS', 10)}")
            return
        
        total_domains = int(input("Berapa total domain yang mau di-claim? "))
        if total_domains < 1:
            print("❌ Jumlah domain harus minimal 1")
            return
        
        password = input(f"Masukkan password untuk semua akun (default: {CONFIG.get('DEFAULT_PASSWORD')}): ").strip()
        if not password:
            password = CONFIG.get('DEFAULT_PASSWORD')
        
    except ValueError:
        print("❌ Input tidak valid!")
        return
    
    # Calculate domains per thread
    domains_per_thread = total_domains // num_threads
    remaining = total_domains % num_threads
    
    print()
    print(f"📊 Konfigurasi:")
    print(f"   - Threads: {num_threads}")
    print(f"   - Total domains: {total_domains}")
    print(f"   - Domains per thread: {domains_per_thread}")
    print(f"   - Password: {password}")
    print(f"   - Results file: {CONFIG.get('RESULTS_FILE')}")
    print(f"   - Headless: {CONFIG.get('HEADLESS')} (edit config.env untuk ubah)")
    print()
    print("⏳ Starting automation...")
    print()
    
    # Create results file with header
    with open(CONFIG.get('RESULTS_FILE'), 'a', encoding='utf-8') as f:
        f.write(f"\n# Batch started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Create tasks for all threads
    tasks = []
    for i in range(num_threads):
        # Distribute remaining domains to first threads
        domains_for_this_thread = domains_per_thread + (1 if i < remaining else 0)
        task = run_thread(i + 1, domains_for_this_thread, password)
        tasks.append(task)
    
    # Run all threads concurrently
    await asyncio.gather(*tasks)
    
    print()
    print("=" * 60)
    print("✅ SELESAI!")
    print(f"📁 Hasil disimpan di: {CONFIG.get('RESULTS_FILE')}")
    print(f"📝 Logs disimpan di: {CONFIG.get('LOG_FILE')}")
    if CONFIG.get('SCREENSHOT_ON_ERROR'):
        print(f"📸 Screenshots (jika ada error) di: {CONFIG.get('SCREENSHOT_FOLDER')}/")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Dihentikan oleh user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
