function toggleTheme() {
    var body = document.getElementsByTagName('body')[0];
    body.classList.toggle('dark-theme');
    
    var isDarkMode = body.classList.contains('dark-theme');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
}


// Detectar si el dispositivo es táctil
if ('ontouchstart' in window || navigator.msMaxTouchPoints) {
    document.documentElement.classList.add('mobile-touch');
}
