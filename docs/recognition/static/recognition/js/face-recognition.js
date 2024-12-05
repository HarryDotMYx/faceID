class FaceRecognitionSystem {
    constructor() {
        this.video = document.getElementById('webcam');
        this.overlay = document.getElementById('overlay');
        this.errorMessage = document.getElementById('errorMessage');
        this.fpsDisplay = document.getElementById('fpsDisplay');
        this.fallbackMessage = document.getElementById('fallbackMessage');
        
        this.camera = new CameraService(this.video);
        this.frameService = new FrameService();
        this.renderer = new OverlayRenderer(this.overlay.getContext('2d'));
        
        this.streaming = false;
        this.processingFrame = false;
        this.processInterval = null;
        this.frameCount = 0;
        this.lastTime = performance.now();
    }

    async start() {
        try {
            this.fallbackMessage.classList.add('hidden');
            this.video.classList.remove('hidden');

            const { width, height } = await this.camera.initialize();
            this.overlay.width = width;
            this.overlay.height = height;
            
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
            const frameBlob = await this.camera.captureFrame();
            const data = await this.frameService.sendFrame(frameBlob);
            
            if (data.faces) {
                this.renderer.render_detections(data.faces, this.overlay.width, this.overlay.height);
                this.updateFPS();
            }
            
        } catch (err) {
            console.error('Error processing frame:', err);
            this.showError(err.message || 'Error processing video frame');
        } finally {
            this.processingFrame = false;
        }
    }

    updateFPS() {
        this.frameCount++;
        const currentTime = performance.now();
        const elapsed = currentTime - this.lastTime;

        if (elapsed >= 1000) {
            const fps = Math.round((this.frameCount * 1000) / elapsed);
            this.fpsDisplay.textContent = `FPS: ${fps}`;
            this.frameCount = 0;
            this.lastTime = currentTime;
        }
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
        this.camera.stop();
        this.renderer.clear();
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