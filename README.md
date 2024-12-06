# Facial Recognition System

A robust facial recognition system built with Django and modern JavaScript, featuring real-time face detection, verification, and user management.

## Features

- 🎥 Real-time face detection and recognition
- 👤 User authentication and profile management
- 📸 Multiple face image upload methods (file upload & webcam capture)
- 🔄 Live face verification
- 📊 Recognition statistics and reporting
- 🌓 Dark/Light theme support
- 🔒 Secure file handling and data protection

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: JavaScript, TailwindCSS
- **Face Recognition**: face-recognition, OpenCV
- **Database**: SQLite3
- **Security**: Django's built-in security features

## Prerequisites

- Python 3.8+
- Node.js 14+
- pip
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HarryDotMYx/faceID.git
cd faceID
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
npm install
```

4. Setup database:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Project Structure

```
facial-recognition-system/
├── recognition/          # Main application
│   ├── urls/            # URL routing
│   ├── views/           # View handlers
│   ├── utils/           # Utility functions
│   ├── static/          # Static files
│   └── templates/       # HTML templates
├── users/               # User management
├── docs/                # Documentation
├── static/              # Global static files
└── templates/           # Global templates
```

## Key Components

### Face Management
- Upload face images
- Process and validate faces
- Generate and store face encodings
- Train recognition model

### Live Recognition
- Real-time video capture
- Frame processing
- Face detection and matching
- Result visualization

### User Management
- User registration and authentication
- Profile management
- Face image management
- Recognition history

## Security Features

- CSRF protection
- Secure file uploads
- User authentication
- Input validation
- Secure media handling

## Performance Optimization

- Efficient frame processing
- Optimized face detection
- Resource management
- Caching mechanisms

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- [face-recognition](https://github.com/ageitgey/face_recognition) library
- [Django](https://www.djangoproject.com/)
- [TailwindCSS](https://tailwindcss.com/)
- [OpenCV](https://opencv.org/)

##
Made with 💓💖💝💘💌 <3 


## Docs?
- Read at [docs](https://github.com/HarryDotMYx/faceID/tree/main/docs)