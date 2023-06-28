function togglePasswordVisibility(inputId) {
    var passwordInput = document.getElementById(inputId);
    var icon = passwordInput.nextElementSibling.querySelector('i.fa-eye');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}