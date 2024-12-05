class FaceRecognitionSystem {
    constructor() {
        this.video = document.getElementById('webcam');
        this.overlay = document.getElementById('overlay');
        this.errorMessage = document.getElementById('errorMessage');
        this.fpsDisplay = document.getElementById('fpsDisplay');
        this.fallbackMessage = document.getElementById('fallbackMessage');
        this.streaming = false;
        this.processingFrame = false;
        this.processInterval = null;
        this.ctx = this.overlay.getContext('2d');
    }

    async start() {
        try {
            this.fallbackMessage.classList.add('hidden');
            this.video.classList.remove('hidden');

            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: "user",
                    frameRate: { ideal: 30 }
                }
            });
            
            this.video.srcObject = stream;
            
            await new Promise((resolve) => {
                this.video.onloadedmetadata = () => {
                    this.video.play();
                    resolve();
                };
            });

            this.overlay.width = this.video.videoWidth;
            this.overlay.height = this.video.videoHeight;
            
            this.streaming = true;
            this.processInterval = setInterval(() => this.processFrame(), 100);
            
        } catch (err) {
            console.error('Error starting face recognition:', err);
            this.showError('Could not access webcam. Please ensure you have granted camera permissions.');
        }
    }

    async processFrame() {
        if (!this.streaming || this.processingFrame) return;
        this.processingFrame = true;
        
        try {
            const canvas = document.createElement('canvas');
            canvas.width = this.video.videoWidth;
            canvas.height = this.video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0);
            
            const blob = await new Promise(resolve => {
                canvas.toBlob(resolve, 'image/jpeg', 0.8);
            });
            
            const formData = new FormData();
            formData.append('frame', blob);
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            const response = await fetch('/process-frame/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const data = await response.json();
            if (!data.success) {
                throw new Error(data.error || 'Unknown error occurred');
            }
            
            if (data.faces) {
                this.drawDetections(data.faces);
            }
            
        } catch (err) {
            console.error('Error processing frame:', err);
            this.showError(err.message || 'Error processing video frame');
        } finally {
            this.processingFrame = false;
        }
    }

    drawDetections(faces) {
        this.ctx.clearRect(0, 0, this.overlay.width, this.overlay.height);
        
        faces.forEach(face => {
            const isRecognized = face.name !== 'Unknown';
            
            // Set colors based on recognition status
            const strokeColor = isRecognized ? '#00ff00' : '#ff0000';
            const bgColor = isRecognized ? 'rgba(0, 255, 0, 0.2)' : 'rgba(255, 0, 0, 0.2)';
            const textColor = isRecognized ? '#00ff00' : '#ff0000';
            
            // Draw face rectangle with background
            this.ctx.fillStyle = bgColor;
            this.ctx.fillRect(face.x, face.y, face.width, face.height);
            
            this.ctx.strokeStyle = strokeColor;
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(face.x, face.y, face.width, face.height);
            
            // Draw name label
            const label = face.confidence ? `${face.name} (${face.confidence}%)` : face.name;
            this.ctx.font = '16px Arial';
            const textWidth = this.ctx.measureText(label).width;
            
            // Label background
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            this.ctx.fillRect(face.x, face.y - 25, textWidth + 10, 25);
            
            // Label text
            this.ctx.fillStyle = textColor;
            this.ctx.fillText(label, face.x + 5, face.y - 7);
        });
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.classList.remove('hidden');
    }

    stop() {
        this.streaming = false;
        if (this.processInterval) {
            clearInterval(this.processInterval);
        }
        if (this.video.srcObject) {
            this.video.srcObject.getTracks().forEach(track => track.stop());
        }
        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.overlay.width, this.overlay.height);
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const faceRecognition = new FaceRecognitionSystem();
    faceRecognition.start();
    
    window.addEventListener('beforeunload', () => {
        faceRecognition.stop();
    });
});