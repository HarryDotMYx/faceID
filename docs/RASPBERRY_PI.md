# Facial Recognition System on Raspberry Pi

## Hardware Requirements

1. Raspberry Pi (Recommended: Raspberry Pi 4 Model B with at least 4GB RAM)
2. USB Webcam or Raspberry Pi Camera Module
3. MicroSD Card (16GB or larger)
4. Power Supply
5. Optional: Display, Keyboard, and Mouse

## Software Requirements

1. Raspberry Pi OS (64-bit recommended)
2. Python 3.8 or newer
3. OpenCV
4. dlib
5. face_recognition library
6. Django

## Installation Guide

### 1. Set Up Raspberry Pi OS

  bash
# Download and flash Raspberry Pi OS to your SD card using Raspberry Pi Imager
# Boot your Raspberry Pi and open terminal

# Update system packages
sudo apt update && sudo apt upgrade -y
  

### 2. Install Required Dependencies

  bash
# Install system dependencies
sudo apt install -y \
    python3-pip \
    python3-dev \
    cmake \
    build-essential \
    pkg-config \
    libx11-dev \
    libatlas-base-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libjpeg-dev \
    libopenblas-dev \
    liblapack-dev \
    python3-numpy \
    python3-opencv

# Install Python packages
pip3 install --upgrade pip
pip3 install -r requirements.txt
  

### 3. Clone and Set Up Project

  bash
# Clone the project
git clone <your-repository-url>
cd facial-recognition-django

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser
python manage.py createsuperuser
  

### 4. Configure Camera

#### For USB Webcam:
  
# No additional configuration needed
# The system will automatically detect USB webcams
  

#### For Raspberry Pi Camera Module:
  bash
# Enable camera interface
sudo raspi-config
# Navigate to Interface Options > Camera > Enable

# Reboot
sudo reboot
  

## Running the System

### 1. Start Development Server

  bash
# Start Django server
python manage.py runserver 0.0.0.0:8000
  

### 2. Access the Interface

- Open a web browser and navigate to `http://<raspberry-pi-ip>:8000`
- Log in with your credentials
- Upload face images for recognition

## Production Deployment

### 1. Configure Gunicorn

  bash
# Install Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/faceid.service

# Add the following content:
[Unit]
Description=FaceID Django Application
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/gunicorn core.wsgi:application --bind unix:/tmp/faceid.sock
Restart=always

[Install]
WantedBy=multi-user.target
  

### 2. Configure Nginx

  bash
# Install Nginx
sudo apt install nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/faceid

# Add the following content:
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/project;
    }

    location /media/ {
        root /path/to/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/tmp/faceid.sock;
    }
}

# Enable the site
sudo ln -s /etc/nginx/sites-available/faceid /etc/nginx/sites-enabled
  

### 3. Start Services

  bash
# Start and enable services
sudo systemctl start faceid
sudo systemctl enable faceid
sudo systemctl restart nginx
  

## Performance Optimization

1. **Camera Settings**
     
   # Adjust resolution for better performance
   camera_resolution = (640, 480)  # Lower resolution for faster processing
     

2. **Face Detection**
     
   # Use HOG instead of CNN for faster detection on Raspberry Pi
   face_locations = face_recognition.face_locations(frame, model="hog")
     

3. **Frame Processing**
     
   # Reduce frame processing frequency
   PROCESS_EVERY_N_FRAMES = 2  # Process every second frame
     

## Security Considerations

1. **SSL/TLS**
   - Enable HTTPS using Let's Encrypt
   - Configure SSL in Nginx

2. **File Permissions**
     bash
   # Set correct permissions
   sudo chown -R www-data:www-data /path/to/project/media
   sudo chmod -R 755 /path/to/project/media
     

3. **Environment Variables**
     bash
   # Store sensitive data in .env file
   SECRET_KEY=your_secret_key
   DEBUG=False
   ALLOWED_HOSTS=your_domain.com
     

## Troubleshooting

### Common Issues and Solutions

1. **Camera Not Detected**
     bash
   # Check USB camera
   ls /dev/video*
   
   # Check Pi Camera
   vcgencmd get_camera
     

2. **Performance Issues**
   - Reduce resolution
   - Increase process interval
   - Use HOG face detection
   - Close unnecessary applications

3. **Memory Issues**
     bash
   # Monitor memory usage
   free -h
   
   # Add swap if needed
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Set CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
     

## Maintenance

### Regular Tasks

1. **Backup**
     bash
   # Backup database and media files
   python manage.py dumpdata > backup.json
   rsync -av /path/to/project/media/ /backup/location/
     

2. **Updates**
     bash
   # Update system packages
   sudo apt update && sudo apt upgrade -y
   
   # Update Python packages
   pip install -r requirements.txt --upgrade
     

3. **Log Rotation**
     bash
   # Configure logrotate
   sudo nano /etc/logrotate.d/faceid
   
   # Add configuration:
   /path/to/project/logs/*.log {
       weekly
       rotate 4
       compress
       delaycompress
       missingok
       notifempty
   }
     

## API Documentation

### Face Detection Endpoints

1. **Process Frame**
     http
   POST /process-frame/
   Content-Type: multipart/form-data
   
   frame: <binary_data>
     

2. **Upload Face**
     http
   POST /recognition/face/upload/
   Content-Type: multipart/form-data
   
   image: <binary_data>
     

### Authentication Endpoints

1. **Login**
     http
   POST /login/
   Content-Type: application/x-www-form-urlencoded
   
   username: <username>
   password: <password>
     

2. **Register**
     http
   POST /users/register/
   Content-Type: application/x-www-form-urlencoded
   
   username: <username>
   email: <email>
   password1: <password>
   password2: <password_confirmation>
     

## GPIO Integration (Optional)

### Control External Devices

  
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # LED
GPIO.setup(23, GPIO.OUT)  # Relay

def on_face_recognized():
    GPIO.output(18, GPIO.HIGH)  # Turn on LED
    GPIO.output(23, GPIO.HIGH)  # Activate relay
    
def on_face_unknown():
    GPIO.output(18, GPIO.LOW)   # Turn off LED
    GPIO.output(23, GPIO.LOW)   # Deactivate relay
  

### Add Door Lock Control

  
class DoorControl:
    def __init__(self, pin=23):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        
    def unlock(self):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(5)  # Keep unlocked for 5 seconds
        GPIO.output(self.pin, GPIO.LOW)
        
    def lock(self):
        GPIO.output(self.pin, GPIO.LOW)
  

## Power Management

### Automatic Shutdown

  bash
# Create shutdown script
sudo nano /usr/local/bin/auto_shutdown.sh

#!/bin/bash
# Shutdown at specific time or after inactivity
IDLE_TIME=$(cat /proc/uptime | awk '{print $2}')
if [ $IDLE_TIME -gt 3600 ]; then
    sudo shutdown -h now
fi

# Make executable
sudo chmod +x /usr/local/bin/auto_shutdown.sh

# Add to crontab
crontab -e
# Add line:
0 * * * * /usr/local/bin/auto_shutdown.sh
  

### UPS Integration

  
from gpiozero import Button
import subprocess

# Monitor UPS status
power_status = Button(27)

def on_power_lost():
    # Gracefully shutdown system
    subprocess.call(['sudo', 'shutdown', '-h', 'now'])

power_status.when_pressed = on_power_lost
  

## Monitoring

### System Health Checks

  
import psutil
import logging

def check_system_health():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    
    logging.info(f"CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")
    
    if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
        logging.warning("System resources critical!")
  

## Backup and Recovery

### Automated Backup Script

  bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/path/to/backups"
PROJECT_DIR="/path/to/project"
DATE=$(date +%Y%m%d)

# Backup database
python manage.py dumpdata > $BACKUP_DIR/db_$DATE.json

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz $PROJECT_DIR/media/

# Backup configuration
cp $PROJECT_DIR/.env $BACKUP_DIR/env_$DATE.bak

# Remove old backups (keep last 7 days)
find $BACKUP_DIR -type f -mtime +7 -exec rm {} \;
  