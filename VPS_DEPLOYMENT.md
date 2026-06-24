# 🚀 VPS Deployment Guide

Panduan lengkap untuk deploy script di VPS (Ubuntu/Debian).

---

## 📋 Requirements

### VPS Specs (Minimal)
- **OS**: Ubuntu 20.04+ / Debian 10+
- **RAM**: 2GB (untuk 1-3 threads), 4GB+ (untuk 5-10 threads)
- **CPU**: 1-2 cores
- **Storage**: 10GB+
- **Network**: Stable internet connection

### VPS Providers (Recommended)
- DigitalOcean (Droplet)
- Vultr
- Linode
- AWS Lightsail
- Contabo
- IDCloudHost (Indonesia)

---

## 🛠️ Step-by-Step Installation

### 1. Connect to VPS
```bash
ssh root@your-vps-ip
# atau
ssh username@your-vps-ip
```

### 2. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Install Python 3.8+
```bash
# Check Python version
python3 --version

# If not installed or old version
sudo apt install python3 python3-pip python3-venv -y
```

### 4. Install Dependencies untuk Playwright (PENTING!)
```bash
# Install dependencies untuk headless browser
sudo apt install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libxshmfence1
```

### 5. Upload Script ke VPS

**Option A: Via SCP (from local PC)**
```bash
# From your local PC
scp -r "d:\bot create\DOMEN_JAGO" username@your-vps-ip:/home/username/
```

**Option B: Via Git (if you have repo)**
```bash
# On VPS
cd ~
git clone your-repo-url
cd DOMEN_JAGO
```

**Option C: Manual (if no Git)**
```bash
# On VPS - create directory
cd ~
mkdir DOMEN_JAGO
cd DOMEN_JAGO

# Then upload files using SFTP client (FileZilla, WinSCP, etc)
```

### 6. Create Virtual Environment
```bash
cd ~/DOMEN_JAGO
python3 -m venv venv
source venv/bin/activate
```

### 7. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 8. Install Playwright Browsers
```bash
# Install Chromium browser for Playwright
python -m playwright install chromium

# Install browser dependencies
python -m playwright install-deps chromium
```

### 9. Configure Script
```bash
# Copy example config
cp config.env.example config.env

# Edit config
nano config.env
```

**Important VPS Config Settings:**
```env
# MUST be True for VPS (no display)
HEADLESS=True

# Adjust based on VPS specs
MAX_THREADS=3          # 2GB RAM
MAX_THREADS=5          # 4GB RAM
MAX_THREADS=10         # 8GB+ RAM

# Other settings
SLOW_MOTION=0
SCREENSHOT_ON_ERROR=True
PAYMENT_TIMEOUT=30
```

Save: `Ctrl+O` → Enter → `Ctrl+X`

---

## 🚀 Running on VPS

### Quick Test (Foreground)
```bash
cd ~/DOMEN_JAGO
source venv/bin/activate
python domain_claimer.py
```

### Run in Background with nohup
```bash
cd ~/DOMEN_JAGO
source venv/bin/activate
nohup python domain_claimer.py > output.log 2>&1 &

# Check process
ps aux | grep domain_claimer

# View logs real-time
tail -f output.log
tail -f domain_claimer.log
```

### Run with Screen (Recommended)
```bash
# Install screen if not available
sudo apt install screen -y

# Create new screen session
screen -S domain-claimer

# Inside screen, run script
cd ~/DOMEN_JAGO
source venv/bin/activate
python domain_claimer.py

# Detach from screen: Ctrl+A then D
# Your script continues running!

# Re-attach to screen
screen -r domain-claimer

# List all screens
screen -ls

# Kill screen
screen -X -S domain-claimer quit
```

### Run with Tmux (Alternative)
```bash
# Install tmux
sudo apt install tmux -y

# Create new tmux session
tmux new -s domain-claimer

# Inside tmux, run script
cd ~/DOMEN_JAGO
source venv/bin/activate
python domain_claimer.py

# Detach from tmux: Ctrl+B then D

# Re-attach to tmux
tmux attach -t domain-claimer

# List sessions
tmux ls

# Kill session
tmux kill-session -t domain-claimer
```

---

## 📊 Monitoring

### Check Running Process
```bash
ps aux | grep python
```

### Monitor Logs
```bash
# Real-time log monitoring
tail -f ~/DOMEN_JAGO/domain_claimer.log

# Last 50 lines
tail -n 50 ~/DOMEN_JAGO/domain_claimer.log

# Search for errors
grep "ERROR" ~/DOMEN_JAGO/domain_claimer.log

# Search for success
grep "SUCCESS" ~/DOMEN_JAGO/domain_claimer.log
```

### Check Results
```bash
cat ~/DOMEN_JAGO/results.txt

# Count successful domains
wc -l ~/DOMEN_JAGO/results.txt
```

### Monitor System Resources
```bash
# CPU & Memory usage
htop

# Or use top
top

# Disk usage
df -h

# Check available memory
free -h
```

---

## 🔄 Automation with Cron

### Schedule Regular Runs

```bash
# Edit crontab
crontab -e

# Add scheduled job (example: run every 6 hours)
0 */6 * * * cd /home/username/DOMEN_JAGO && /home/username/DOMEN_JAGO/venv/bin/python domain_claimer.py >> /home/username/DOMEN_JAGO/cron.log 2>&1

# Or daily at 2 AM
0 2 * * * cd /home/username/DOMEN_JAGO && /home/username/DOMEN_JAGO/venv/bin/python domain_claimer.py >> /home/username/DOMEN_JAGO/cron.log 2>&1
```

**Cron Schedule Examples:**
```bash
# Every hour
0 * * * * command

# Every 6 hours
0 */6 * * * command

# Every day at 2 AM
0 2 * * * command

# Every Sunday at 3 AM
0 3 * * 0 command

# Every 1st of month at midnight
0 0 1 * * command
```

---

## 📥 Downloading Results

### Via SCP (to local PC)
```bash
# From local PC
scp username@your-vps-ip:/home/username/DOMEN_JAGO/results.txt ./results.txt
scp username@your-vps-ip:/home/username/DOMEN_JAGO/domain_claimer.log ./domain_claimer.log
```

### Via SFTP Client
Use FileZilla, WinSCP, or Cyberduck to download files via GUI

### View Results Directly
```bash
# On VPS
cat ~/DOMEN_JAGO/results.txt
```

---

## 🐛 Troubleshooting

### Issue 1: Playwright Browser Installation Failed
```bash
# Reinstall with dependencies
python -m playwright install --with-deps chromium

# Or install system dependencies manually
sudo apt install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2
```

### Issue 2: Out of Memory
```bash
# Check memory
free -h

# Solution: Reduce MAX_THREADS in config.env
nano ~/DOMEN_JAGO/config.env
# Set: MAX_THREADS=2 or MAX_THREADS=1
```

### Issue 3: Browser Crashes
```bash
# Check if running as root (not recommended)
whoami

# If root, create non-root user
adduser domainbot
usermod -aG sudo domainbot
su - domainbot

# Then reinstall and run as non-root user
```

### Issue 4: Permission Denied
```bash
# Fix permissions
cd ~/DOMEN_JAGO
chmod +x domain_claimer.py
chmod 644 config.env
```

### Issue 5: Process Killed/Stopped
```bash
# Check if process is killed by OOM killer
dmesg | grep -i kill

# Solution: Reduce threads or upgrade VPS RAM
```

---

## 🔐 Security Best Practices

### 1. Don't Run as Root
```bash
# Create dedicated user
sudo adduser domainbot
sudo usermod -aG sudo domainbot
su - domainbot
```

### 2. Secure Config File
```bash
# Restrict config.env access
chmod 600 ~/DOMEN_JAGO/config.env
```

### 3. Firewall Setup
```bash
# Enable UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 22/tcp
sudo ufw status
```

### 4. Keep System Updated
```bash
# Regular updates
sudo apt update && sudo apt upgrade -y
```

### 5. Use SSH Key Authentication
```bash
# On local PC, generate SSH key
ssh-keygen -t rsa -b 4096

# Copy to VPS
ssh-copy-id username@your-vps-ip

# Disable password authentication (optional, after SSH key works)
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

---

## 📈 Performance Optimization

### Resource Usage by Thread Count

| Threads | RAM Usage | CPU Usage | Recommended VPS |
|---------|-----------|-----------|-----------------|
| 1       | ~500MB    | ~20%      | 1GB RAM         |
| 2-3     | ~1.2GB    | ~40%      | 2GB RAM         |
| 5       | ~2.5GB    | ~60%      | 4GB RAM         |
| 10      | ~5GB      | ~90%      | 8GB RAM         |

### Optimization Tips

1. **Start Small**: Test with 1-2 threads first
2. **Monitor Resources**: Use `htop` to watch RAM/CPU
3. **Gradual Scaling**: Increase threads slowly
4. **Network**: Ensure stable connection (test with `ping google.com`)
5. **Disk I/O**: Use SSD-based VPS for better performance

---

## 🎯 Production Setup Example

### Complete Production Setup Script

Create file: `~/setup_vps.sh`

```bash
#!/bin/bash

echo "🚀 Setting up Domain Claimer on VPS..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install Playwright dependencies
sudo apt install -y \
    libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 \
    libasound2 libatspi2.0-0 libxshmfence1

# Install screen/tmux
sudo apt install screen tmux htop -y

# Create virtual environment
cd ~/DOMEN_JAGO
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
python -m playwright install-deps chromium

# Setup config
if [ ! -f config.env ]; then
    cp config.env.example config.env
    echo "⚠️  Please edit config.env before running!"
    nano config.env
fi

# Set permissions
chmod 600 config.env
chmod +x domain_claimer.py

echo "✅ Setup complete!"
echo ""
echo "To run script:"
echo "  cd ~/DOMEN_JAGO"
echo "  source venv/bin/activate"
echo "  python domain_claimer.py"
echo ""
echo "Or use screen:"
echo "  screen -S domain-claimer"
echo "  cd ~/DOMEN_JAGO && source venv/bin/activate && python domain_claimer.py"
```

Run setup:
```bash
chmod +x ~/setup_vps.sh
~/setup_vps.sh
```

---

## 📝 Quick Reference

### Start Script
```bash
cd ~/DOMEN_JAGO && source venv/bin/activate && python domain_claimer.py
```

### Background with Screen
```bash
screen -S domain-claimer
cd ~/DOMEN_JAGO && source venv/bin/activate && python domain_claimer.py
# Ctrl+A then D to detach
```

### Check Status
```bash
screen -r domain-claimer           # Reattach
tail -f ~/DOMEN_JAGO/domain_claimer.log  # View logs
cat ~/DOMEN_JAGO/results.txt       # View results
```

### Stop Script
```bash
screen -r domain-claimer           # Reattach
# Then Ctrl+C
```

---

## 🎉 Success Checklist

- [ ] VPS created and accessible via SSH
- [ ] System updated
- [ ] Python 3.8+ installed
- [ ] Playwright dependencies installed
- [ ] Script uploaded to VPS
- [ ] Virtual environment created
- [ ] Python dependencies installed
- [ ] Playwright browsers installed
- [ ] config.env configured (HEADLESS=True)
- [ ] Test run successful
- [ ] Background execution working (screen/tmux)
- [ ] Logs accessible
- [ ] Results saving correctly
- [ ] Monitoring setup (htop, logs)

---

## 💡 Pro Tips

1. **Use Screen/Tmux**: Essential untuk long-running tasks
2. **Monitor Logs**: `tail -f` adalah teman terbaik kamu
3. **Start Conservative**: Mulai dengan 2-3 threads, naikkan bertahap
4. **Regular Backups**: Download `results.txt` secara berkala
5. **Resource Monitoring**: Cek RAM/CPU pakai `htop`
6. **Network Stability**: Test dengan `ping -c 100 google.com`
7. **Timezone Setting**: Set timezone VPS ke timezone kamu
   ```bash
   sudo timedatectl set-timezone Asia/Jakarta
   ```

---

## 🆘 Need Help?

### Common Commands
```bash
# Check Python version
python3 --version

# Check running processes
ps aux | grep python

# Kill process by PID
kill -9 <PID>

# Check disk space
df -h

# Check memory
free -h

# Check network
ping google.com
```

### Log Locations
- Main log: `~/DOMEN_JAGO/domain_claimer.log`
- Results: `~/DOMEN_JAGO/results.txt`
- Screenshots: `~/DOMEN_JAGO/screenshots/`

---

**Happy Claiming! 🚀**

VPS = 24/7 automation = More domains! 🎊
