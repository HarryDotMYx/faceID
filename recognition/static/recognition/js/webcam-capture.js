class WebcamCapture {
    constructor() {
        this.video = document.getElementById('webcam');
        this.canvas = document.getElementById('canvas');
        this.captureBtn = document.getElementById('captureBtn');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.preview = document.getElementById('preview');
        this.retakeBtn = document.getElementById('retakeBtn');
        this.errorMessage = document.getElementById('errorMessage');
        this.ctx = this.canvas.getContext('2d');
        this.stream = null;
        
        this.setupEventListeners();
    }

    async start() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: "user"
                }
            });
            
            this.video.srcObject = this.stream;
            await this.video.play();
            
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            
            this.video.classList.remove('hidden');
            this.captureBtn.classList.remove('hidden');
            
        } catch (err) {
            console.error('Error accessing webcam:', err);
            this.showError('Could not access webcam. Please ensure you have granted camera permissions.');
        }
    }

    setupEventListeners() {
        this.captureBtn.addEventListener('click', () => this.capture());
        this.retakeBtn.addEventListener('click', () => this.retake());
        this.uploadBtn.addEventListener('click', () => this.upload());
    }

    capture() {
        this.ctx.drawImage(this.video, 0, 0);
        this.preview.src = this.canvas.toDataURL('image/jpeg');
        this.preview.classList.remove('hidden');
        this.uploadBtn.classList.remove('hidden');
        this.retakeBtn.classList.remove('hidden');
        this.video.classList.add('hidden');
        this.captureBtn.classList.add('hidden');
    }

    retake() {
        this.preview.classList.add('hidden');
        this.uploadBtn.classList.add('hidden');
        this.retakeBtn.classList.add('hidden');
        this.video.classList.remove('hidden');
        this.captureBtn.classList.remove('hidden');
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.classList.remove('hidden');
    }

    async upload() {
        try {
            const blob = await new Promise(resolve => {
                this.canvas.toBlob(resolve, 'image/jpeg', 0.8);
            });
            
            const formData = new FormData();
            formData.append('image', blob, 'webcam.jpg');
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            const response = await fetch('/recognition/webcam/save/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            
            if (!response.ok) throw new Error('Upload failed');
            
            const result = await response.json();
            if (result.success) {
                window.location.href = '/recognition/face/upload/';
            } else {
                throw new Error(result.error);
            }
            
        } catch (err) {
            console.error('Error uploading image:', err);
            this.showError('Failed to upload image. Please try again.');
        }
    }

    stop() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const webcam = new WebcamCapture();
    webcam.start();
    
    window.addEventListener('beforeunload', () => {
        webcam.stop();
    });
});