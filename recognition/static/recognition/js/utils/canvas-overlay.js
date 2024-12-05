class CanvasOverlay {
    constructor(canvasElement) {
        this.canvas = canvasElement;
        this.ctx = this.canvas.getContext('2d');
    }

    setDimensions(width, height) {
        this.canvas.width = width;
        this.canvas.height = height;
    }

    clear() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawDetections(faces) {
        this.clear();
        
        faces.forEach(face => {
            // Set colors based on recognition status
            const isRecognized = face.name !== 'Unknown';
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
            const label = face.name;
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
}

export default CanvasOverlay;