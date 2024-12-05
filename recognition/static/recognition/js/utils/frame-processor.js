class FrameProcessor {
    constructor() {
        this.processingFrame = false;
        this.frameCount = 0;
        this.fpsStartTime = null;
        this.fps = 0;
    }

    async processFrame(canvas) {
        if (this.processingFrame) return null;
        this.processingFrame = true;

        try {
            this.updateFPS();

            const blob = await new Promise(resolve => {
                canvas.toBlob(resolve, 'image/jpeg', 0.8);
            });
            
            const formData = new FormData();
            formData.append('frame', blob);
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            const response = await fetch('/recognition/process_frame/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            
            if (!response.ok) {
                throw new Error('Server error');
            }
            
            const data = await response.json();
            if (data.faces && data.faces.length > 0) {
                data.faces[0].fps = this.fps;
            }
            
            return data;
        } finally {
            this.processingFrame = false;
        }
    }

    updateFPS() {
        if (this.frameCount === 0) {
            this.fpsStartTime = performance.now();
        }
        this.frameCount++;
        
        if (this.frameCount >= 30) {
            const currentTime = performance.now();
            this.fps = Math.round((this.frameCount * 1000) / (currentTime - this.fpsStartTime));
            this.frameCount = 0;
        }
    }
}

export default FrameProcessor;