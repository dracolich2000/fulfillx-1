const errorMessage = document.getElementById('error-message');
        if (errorMessage.innerText.trim() !== '') {
            errorMessage.style.display = 'block';
            errorMessage.style.textAlign = 'center';
            errorMessage.style.color = 'red';
        }