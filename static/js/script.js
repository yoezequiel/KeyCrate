function toggleTheme() {
    var body = document.getElementsByTagName('body')[0];
    body.classList.toggle('dark-theme');
    
    var isDarkMode = body.classList.contains('dark-theme');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
}