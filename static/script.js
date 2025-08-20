document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const fileInputLabel = document.querySelector('.file-input-label');
    const fileInputText = document.querySelector('.file-input-text');
    const uploadBtn = document.getElementById('uploadBtn');
    const btnText = document.querySelector('.btn-text');
    const loadingSpinner = document.querySelector('.loading-spinner');
    
    const progressSection = document.getElementById('progressSection');
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('errorSection');
    const errorText = document.getElementById('errorText');
    
    // File input change handler
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            fileInputText.textContent = file.name;
            fileInputLabel.classList.add('file-selected');
        } else {
            fileInputText.textContent = 'Choose Image or Video';
            fileInputLabel.classList.remove('file-selected');
        }
    });
    
    // Form submission handler
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            showError('Please select a file');
            return;
        }
        
        // Validate file type
        const allowedTypes = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
            'video/mp4', 'video/avi', 'video/quicktime'
        ];
        
        if (!allowedTypes.includes(file.type)) {
            showError('File type not supported. Please upload an image (JPG, PNG, GIF) or video (MP4, AVI, MOV).');
            return;
        }
        
        // Validate file size (100MB max)
        const maxSize = 100 * 1024 * 1024;
        if (file.size > maxSize) {
            showError('File size too large. Please upload a file smaller than 100MB.');
            return;
        }
        
        uploadFile();
    });
    
    function uploadFile() {
        const formData = new FormData(uploadForm);
        
        // Show loading state
        showLoading();
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            if (data.success) {
                showResults(data);
            } else {
                showError(data.error || 'Upload failed');
            }
        })
        .catch(error => {
            hideLoading();
            showError('Network error: ' + error.message);
        });
    }
    
    function showLoading() {
        uploadBtn.disabled = true;
        btnText.style.display = 'none';
        loadingSpinner.style.display = 'inline-block';
        
        progressSection.style.display = 'block';
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
    }
    
    function hideLoading() {
        uploadBtn.disabled = false;
        btnText.style.display = 'inline-block';
        loadingSpinner.style.display = 'none';
        
        progressSection.style.display = 'none';
    }
    
    function showResults(data) {
        const resultInfo = document.getElementById('resultInfo');
        const originalMedia = document.getElementById('originalMedia');
        const processedMedia = document.getElementById('processedMedia');
        const downloadBtn = document.getElementById('downloadBtn');
        
        // Update result info
        resultInfo.innerHTML = `
            <strong>Processing Complete!</strong><br>
            File: ${data.original_filename}<br>
            Effect: ${data.effect}<br>
            Faces detected: ${data.faces_detected}
        `;
        
        // Clear previous media
        originalMedia.innerHTML = '';
        processedMedia.innerHTML = '';
        
        // Create media elements based on file type
        if (data.file_type === 'image') {
            const originalImg = document.createElement('img');
            originalImg.src = data.original_url;
            originalImg.alt = 'Original image';
            originalMedia.appendChild(originalImg);
            
            const processedImg = document.createElement('img');
            processedImg.src = data.processed_url;
            processedImg.alt = 'Processed image';
            processedMedia.appendChild(processedImg);
        } else if (data.file_type === 'video') {
            const originalVideo = document.createElement('video');
            originalVideo.src = data.original_url;
            originalVideo.controls = true;
            originalVideo.style.width = '100%';
            originalMedia.appendChild(originalVideo);
            
            const processedVideo = document.createElement('video');
            processedVideo.src = data.processed_url;
            processedVideo.controls = true;
            processedVideo.style.width = '100%';
            processedMedia.appendChild(processedVideo);
        }
        
        // Setup download button
        downloadBtn.style.display = 'inline-block';
        downloadBtn.onclick = function() {
            const filename = data.processed_url.split('/').pop();
            window.open(`/download/${filename}`, '_blank');
        };
        
        // Show results section
        resultSection.style.display = 'block';
        errorSection.style.display = 'none';
        
        // Scroll to results
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    function showError(message) {
        errorText.textContent = message;
        errorSection.style.display = 'block';
        resultSection.style.display = 'none';
        
        // Scroll to error
        errorSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Drag and drop functionality
    const uploadSection = document.querySelector('.upload-section');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadSection.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadSection.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadSection.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        uploadSection.classList.add('drag-over');
    }
    
    function unhighlight() {
        uploadSection.classList.remove('drag-over');
    }
    
    uploadSection.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }
});

// Add CSS for drag over state
const style = document.createElement('style');
style.textContent = `
    .upload-section.drag-over {
        border: 2px dashed #667eea;
        background-color: #f0f4ff;
        transform: scale(1.02);
        transition: all 0.3s ease;
    }
`;
document.head.appendChild(style);