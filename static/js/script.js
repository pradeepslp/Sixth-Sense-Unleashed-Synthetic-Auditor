document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const fileMsg = document.querySelector('.file-msg');
    const generateBtn = document.getElementById('generateBtn');

    fileInput.addEventListener('change', () => {
        const files = fileInput.files;
        if (files.length > 0) {
            fileMsg.textContent = `Selected: ${files[0].name}`;
            fileMsg.style.color = '#00ff41';
        }
    });

    generateBtn.addEventListener('click', (e) => {
        const btn = e.target;
        // Simple loading animation
        btn.innerHTML = 'ANALYZING VULNERABILITIES... <span class="blink">_</span>';
        btn.style.opacity = '0.7';
    });
});