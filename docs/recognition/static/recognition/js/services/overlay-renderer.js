class OverlayRenderer {
    constructor(ctx) {
        this.ctx = ctx;
    }

    render_detections(faces, width, height) {
        this.ctx.clearRect(0, 0, width, height);
        
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

    clear() {
        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
        }
    }
}