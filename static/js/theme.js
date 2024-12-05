// Theme management
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'system';
        this.systemDark = window.matchMedia('(prefers-color-scheme: dark)');
        this.init();
    }

    init() {
        // Set initial theme
        this.applyTheme();
        
        // Listen for system theme changes
        this.systemDark.addEventListener('change', () => {
            if (this.theme === 'system') {
                this.applyTheme();
            }
        });

        // Setup theme toggle buttons
        document.querySelectorAll('[data-theme-value]').forEach(button => {
            button.addEventListener('click', () => {
                this.setTheme(button.dataset.themeValue);
            });
        });
    }

    setTheme(newTheme) {
        this.theme = newTheme;
        localStorage.setItem('theme', newTheme);
        this.applyTheme();
    }

    applyTheme() {
        const isDark = this.theme === 'dark' || 
                      (this.theme === 'system' && this.systemDark.matches);
        
        document.documentElement.classList.toggle('dark', isDark);
        
        // Update active state of theme buttons
        document.querySelectorAll('[data-theme-value]').forEach(button => {
            button.classList.toggle('active', button.dataset.themeValue === this.theme);
        });
    }

    getCurrentTheme() {
        return this.theme;
    }
}

// Initialize theme manager
window.themeManager = new ThemeManager();