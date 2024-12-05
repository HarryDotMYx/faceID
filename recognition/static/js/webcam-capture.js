class WebcamCapture {
    constructor() {
        this.video = document.getElementById('webcam');
        this.canvas = document.getElementById('canvas');
        this.captureBtn = document.getElementById('captureBtn');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.preview = document.getElementById('preview');
        this.retakeBtn = document.getElementById('retakeBtn');
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
            
            // Set canvas size to match video
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            
            // Show capture interface
            this.video.classList.remove('hidden');
            this.captureBtn.classList.remove('hidden');
            
        } catch (err) {
            console.error('Error accessing webcam:', err);
            document.getElementById('errorMessage').textContent = 
                'Could not access webcam. Please ensure you have granted camera permissions.';
            document.getElementById('errorMessage').classList.remove('hidden');
        }
    }

    setupEventListeners() {
        this.captureBtn.addEventListener('click', () => this.capture());
        this.retakeBtn.addEventListener('click', () => this.retake());
        this.uploadBtn.addEventListener('click', () => this.upload());
    }

    capture() {
        // Draw current video frame to canvas
        this.ctx.drawImage(this.video, 0, 0);
        
        // Show preview and upload button
        this.preview.src = this.canvas.toDataURL('image/jpeg');
        this.preview.classList.remove('hidden');
        this.uploadBtn.classList.remove('hidden');
        this.retakeBtn.classList.remove('hidden');
        
        // Hide video and capture button
        this.video.classList.add('hidden');
        this.captureBtn.classList.add('hidden');
    }

    retake() {
        // Hide preview and buttons
        this.preview.classList.add('hidden');
        this.uploadBtn.classList.add('hidden');
        this.retakeBtn.classList.add('hidden');
        
        // Show video and capture button
        this.video.classList.remove('hidden');
        this.captureBtn.classList.remove('hidden');
    }

    async upload() {
        try {
            // Convert canvas to blob
            const blob = await new Promise(resolve => {
                this.canvas.toBlob(resolve, 'image/jpeg', 0.8);
            });
            
            // Create form data
            const formData = new FormData();
            formData.append('image', blob, 'webcam.jpg');
            
            // Add CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Upload image
            const response = await fetch('/recognition/save-webcam-image/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            
            if (!response.ok) throw new Error('Upload failed');
            
            const result = await response.json();
            if (result.success) {
                window.location.href = '/recognition/upload/';
            } else {
                throw new Error(result.error);
            }
            
        } catch (err) {
            console.error('Error uploading image:', err);
            document.getElementById('errorMessage').textContent = 
                'Failed to upload image. Please try again.';
            document.getElementById('errorMessage').classList.remove('hidden');
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
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        webcam.stop();
    });
});