# Raspberry Pi 4/5 Setup Guide

## Requirements

- Raspberry Pi 4 (4GB+ RAM recommended) or Pi 5
- Raspberry Pi OS (64-bit)
- Docker installed
- Internet connection

## Quick Setup

### 1. Install Docker (if not installed)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

Log out and back in for group changes to take effect.

### 2. Clone Repository

```bash
git clone <your-repo>
cd retail_odyssey
```

### 3. Configure Environment

```bash
cp .env.example .env
nano .env  # Add your API keys
```

### 4. Build and Run (ARM-optimized)

```bash
docker-compose -f docker-compose.arm.yml up -d
```

### 5. Access Services

- **Backend API**: http://raspberrypi.local:8000
- **Grafana Dashboard**: http://raspberrypi.local:3000 (admin/admin)
- **Prometheus**: http://raspberrypi.local:9090

## Performance Notes

### Raspberry Pi 4 (4GB)
- ✅ Can run all services
- ⚠️ Image generation may be slower (10-15s)
- 💡 Recommended: Disable image generation for faster responses

### Raspberry Pi 5 (8GB)
- ✅ Runs smoothly
- ✅ Image generation ~5-8s
- ✅ Can handle multiple concurrent users

## Optimization Tips

### 1. Reduce Memory Usage

Edit `docker-compose.arm.yml`:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

### 2. Disable Image Generation (Optional)

If Pi 4 is struggling, comment out ImageGenAgent in orchestrator.

### 3. Use Swap Space

```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## Monitoring

Check resource usage:
```bash
docker stats
```

View logs:
```bash
docker-compose -f docker-compose.arm.yml logs -f backend
```

## Troubleshooting

### Out of Memory
- Reduce Grafana memory: Add `GF_DATABASE_WAL=false` to environment
- Disable Prometheus if not needed for demo

### Slow Image Generation
- This is normal on Pi 4 - Gemini API processes remotely
- Network speed is the bottleneck, not Pi CPU

### Port Already in Use
```bash
sudo lsof -ti:8000 | xargs sudo kill -9
```

## Demo Tips for Hackathon

1. **Show ARM Architecture**: Run `uname -m` → shows `aarch64`
2. **Highlight Efficiency**: "Running 5 AI agents + Grafana on a $35 Pi!"
3. **Real-time Metrics**: Show Grafana dashboard updating live
4. **Multi-platform**: "Same code runs on Pi, Mac M1, and x86"

## Hackathon Arm Challenge

✅ **Native ARM64 build**  
✅ **Optimized for Raspberry Pi**  
✅ **Multi-platform Docker images**  
✅ **Efficient resource usage**  

---

**Bonus**: Borrow a Pi 5 from the hackathon organizers (mentioned in slides: `hackuk.org/raspi`)
