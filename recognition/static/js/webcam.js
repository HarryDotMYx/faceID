class WebcamHandler {
    constructor() {
        this.video = document.getElementById('webcam');
        this.overlay = document.getElementById('overlay');
        this.errorMessage = document.getElementById('errorMessage');
        this.streaming = false;
        this.processingFrame = false;
        this.processInterval = null;
        
        // Initialize overlay canvas
        this.overlay.style.position = 'absolute';
        this.overlay.style.top = '0';
        this.overlay.style.left = '0';
    }

    async start() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: "user"
                }
            });
            
            this.video.srcObject = stream;
            
            // Wait for video to be ready
            await new Promise((resolve) => {
                this.video.onloadedmetadata = () => {
                    this.video.play();
                    resolve();
                };
            });

            // Set canvas dimensions to match video
            this.overlay.width = this.video.videoWidth;
            this.overlay.height = this.video.videoHeight;
            this.ctx = this.overlay.getContext('2d');
            
            this.streaming = true;
            
            // Start processing frames
            this.processInterval = setInterval(() => this.processFrame(), 500);
            
        } catch (err) {
            console.error('Error accessing webcam:', err);
            this.showError('Could not access webcam. Please ensure you have granted camera permissions.');
        }
    }

    async processFrame() {
        if (!this.streaming || this.processingFrame) return;
        
        this.processingFrame = true;
        
        try {
            // Create temporary canvas for frame capture
            const canvas = document.createElement('canvas');
            canvas.width = this.video.videoWidth;
            canvas.height = this.video.videoHeight;
            const ctx = canvas.getContext('2d');
            
            // Draw current video frame
            ctx.drawImage(this.video, 0, 0);
            
            // Convert to blob
            const blob = await new Promise(resolve => {
                canvas.toBlob(resolve, 'image/jpeg', 0.8);
            });
            
            // Create form data
            const formData = new FormData();
            formData.append('frame', blob);
            
            // Add CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Send to server
            const response = await fetch('/recognition/process_frame/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            
            if (!response.ok) throw new Error('Server error');
            
            const data = await response.json();
            this.drawDetections(data.faces);
            
        } catch (err) {
            console.error('Error processing frame:', err);
            this.showError('Error processing video frame');
        } finally {
            this.processingFrame = false;
        }
    }

    drawDetections(faces) {
        // Clear previous drawings
        this.ctx.clearRect(0, 0, this.overlay.width, this.overlay.height);
        
        faces.forEach(face => {
            // Draw rectangle around face
            this.ctx.strokeStyle = '#00ff00';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(face.x, face.y, face.width, face.height);
            
            // Draw name label
            this.ctx.fillStyle = 'rgba(0, 255, 0, 0.8)';
            this.ctx.font = '16px Arial';
            const textWidth = this.ctx.measureText(face.name).width;
            this.ctx.fillRect(face.x, face.y - 25, textWidth + 10, 20);
            
            this.ctx.fillStyle = '#000000';
            this.ctx.fillText(face.name, face.x + 5, face.y - 10);
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