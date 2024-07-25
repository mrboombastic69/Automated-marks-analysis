document.addEventListener('DOMContentLoaded', function() {
    const analyzeContent = document.getElementById('analyze-content');
    const historyContent = document.getElementById('history-content');
    const settingsContent = document.getElementById('settings-content');
    
    const uploadContainer = document.getElementById('upload-container');
    const fileInput = document.getElementById('file-input');
    const fileStatus = document.getElementById('file-status');
    const downloadBtn = document.getElementById('download-btn');
    const host = 'http://127.0.0.1:5000/files'; // Set your server address here

    function showContent(content) {
        analyzeContent.style.display = 'none';
        historyContent.style.display = 'none';
        settingsContent.style.display = 'none';
        content.style.display = 'block';
    }
    showContent(analyzeContent);

    document.getElementById('analyze-btn').addEventListener('click', function() {
        showContent(analyzeContent);
    });

    document.getElementById('history-btn').addEventListener('click', function() {
        showContent(historyContent);
    });

    document.getElementById('settings-btn').addEventListener('click', function() {
        showContent(settingsContent);
    });

    function log(message) {
        console.log(message);
    }

    uploadContainer.addEventListener('dragover', function(event) {
        event.preventDefault();
        uploadContainer.classList.add('dragging');
        log('Dragging over the container');
    });

    uploadContainer.addEventListener('dragleave', function(event) {
        uploadContainer.classList.remove('dragging');
        log('Drag leave from the container');
    });

    uploadContainer.addEventListener('drop', function(event) {
        event.preventDefault();
        uploadContainer.classList.remove('dragging');
        const files = event.dataTransfer.files;
        log('File dropped');
        handleFiles(files);
    });

    fileInput.addEventListener('change', function(event) {
        const files = event.target.files;
        log('File selected through file input');
        handleFiles(files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            fileStatus.textContent = `File chosen: ${file.name}`;
            log(`File chosen: ${file.name}`);
            uploadFile(file);
        } else {
            fileStatus.textContent = 'No file chosen';
            log('No file chosen');
        }
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        log('Starting file upload');
        fetch(`${host}/upload`, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                fileStatus.textContent = 'File uploaded successfully!';
                downloadBtn.style.display = 'inline-block';
                downloadBtn.href = `${host}/download/${data.processed_file}`;
                log('File uploaded successfully');
            } else {
                fileStatus.textContent = 'File upload failed. Please try again.';
                log('File upload failed');
            }
        })
        .catch(error => {
            fileStatus.textContent = 'Error uploading file. Please try again.';
            log(`Error: ${error}`);
        });
    }
});
