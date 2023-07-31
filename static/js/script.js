function toggleTheme() {
    var body = document.getElementsByTagName('body')[0];
    body.classList.toggle('dark-theme');
    
    var isDarkMode = body.classList.contains('dark-theme');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
}

document.addEventListener('DOMContentLoaded', function() {
    var isDarkMode = localStorage.getItem('theme') === 'dark';
    var body = document.getElementsByTagName('body')[0];
    if (isDarkMode) {
        body.classList.add('dark-theme');
    }

    var themeSwitch = document.getElementById('theme-switch');
    themeSwitch.checked = isDarkMode;
});
