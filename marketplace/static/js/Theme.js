
windows.onload = () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        dpcument.getElementById('theme-icon').className = 'bi bi-moon-fill';
    }else {
        document.getElementById('theme-icon').className = 'bi bi-sun-fill';
    }
};

// Toggle theme Function
function toggleTheme() {
    const body = document.body;
    const icon = document.getElementById('theme-icon');

    body.classList.toggle('dark-theme');
    if (body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
        icon.className = 'bi bi-moon-fill';
    }else {
        localStorage.setItem('theme', 'light');
        icon.className = 'bi bi-sun-fill';
    }
}