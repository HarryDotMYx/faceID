class FrameService {
    constructor() {
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    async sendFrame(frameBlob) {
        const formData = new FormData();
        formData.append('frame', frameBlob);
        
        const response = await fetch('/process-frame/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': this.csrfToken
            }
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'Unknown error occurred');
        }
        
        return data;
    }
}