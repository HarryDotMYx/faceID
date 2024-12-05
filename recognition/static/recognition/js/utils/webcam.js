class WebcamManager {
    constructor(videoElement) {
        this.video = videoElement;
        this.stream = null;
    }

    async initialize() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: "user",
                    frameRate: { ideal: 30 }
                }
            });
            
            this.video.srcObject = this.stream;
            
            return new Promise((resolve) => {
                this.video.onloadedmetadata = () => {
                    this.video.play();
                    resolve({
                        width: this.video.videoWidth,
                        height: this.video.videoHeight
                    });
                };
            });
        } catch (err) {
            throw new Error('Could not access webcam. Please ensure you have granted camera permissions.');
        }
    }

    stop() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
    }

    captureFrame() {
        const canvas = document.createElement('canvas');
        canvas.width = this.video.videoWidth;
        canvas.height = this.video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.video, 0, 0);
        return canvas;
    }
}

export default WebcamManager;