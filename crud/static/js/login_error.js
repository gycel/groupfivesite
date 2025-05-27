document.addEventListener('DOMContentLoaded', function() {
    const hasError = window.location.search.includes('error') ||
                    document.querySelector('[data-django-message]')?.textContent.includes('Invalid');

    if (hasError) {
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const loginError = document.createElement('loginError');

         //Apply red border
        emailInput.style.borderColor = '#ef4444';
        passwordInput.style.borderColor = '#ef4444';
            
         // Show error message 
        loginError.classList.remove('hidden');

        // Clear errors message
        function clearError() {
            usernameInput.style.borderColor = '';
            passwordInput.style.borderColor = '';
            loginError.classList.add('hidden');
        }
        emailInput.addEventListener('input', clearError);
        passwordInput.addEventListener('input', clearError);
    }
});