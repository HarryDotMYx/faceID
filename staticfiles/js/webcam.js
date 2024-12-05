// Webcam handling and face detection
class WebcamHandler {
    constructor() {
        this.video = document.getElementById('webcam');
        this.overlay = document.getElementById('overlay');
        this.ctx = this.overlay.getContext('2d');
        this.streaming = false;
        this.processingFrame = false;
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
            this.video.play();
            
            this.video.addEventListener('loadedmetadata', () => {
                this.overlay.width = this.video.videoWidth;
                this.overlay.height = this.video.videoHeight;
                this.streaming = true;
                this.processFrames();
            });
        } catch (err) {
            console.error('Error accessing webcam:', err);
            document.getElementById('errorMessage').textContent = 
                'Could not access webcam. Please ensure you have granted camera permissions.';
            document.getElementById('errorMessage').classList.remove('hidden');
        }
    }

    async processFrames() {
        if (!this.streaming || this.processingFrame) return;
        
        this.processingFrame = true;
        
        // Create canvas and get frame data
        const canvas = document.createElement('canvas');
        canvas.width = this.video.videoWidth;
        canvas.height = this.video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.video, 0, 0);
        
        // Convert to blob and send to server
        canvas.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append('frame', blob);
            
            try {
                const response = await fetch('/process-frame/', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                this.drawDetections(data.faces);
            } catch (err) {
                console.error('Error processing frame:', err);
            }
            
            this.processingFrame = false;
            // Continue processing frames
            requestAnimationFrame(() => this.processFrames());
        }, 'image/jpeg');
    }

    drawDetections(faces) {
        this.ctx.clearRect(0, 0, this.overlay.width, this.overlay.height);
        
        faces.forEach(face => {
            // Draw rectangle
            this.ctx.strokeStyle = '#00ff00';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(face.x, face.y, face.width, face.height);
            
            // Draw name label
            this.ctx.fillStyle = '#00ff00';
            this.ctx.font = '16px Arial';
            this.ctx.fillText(face.name, face.x, face.y - 5);
        });
    }

    stop() {
        this.streaming = false;
        if (this.video.srcObject) {
            this.video.srcObject.getTracks().forEach(track => track.stop());
        }
    }
}