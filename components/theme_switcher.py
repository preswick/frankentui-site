"""Theme Switcher Component with localStorage Persistence"""

from fasthtml.common import *

THEMES = [
    {'id': 'cyberpunk', 'name': 'Cyberpunk Aurora', 'icon': '\u2726'},  # Four-pointed star
    {'id': 'darcula', 'name': 'Darcula', 'icon': '\u263e'},            # Last quarter moon
    {'id': 'nordic', 'name': 'Nordic Frost', 'icon': '\u2744'},         # Snowflake
    {'id': 'light', 'name': 'Lumen Light', 'icon': '\u2600'},           # Sun
]

def theme_script():
    """
    JavaScript for theme switching with localStorage persistence.
    Should be included in the page head.
    """
    return Script("""
        // Theme management
        const THEMES = ['cyberpunk', 'darcula', 'nordic', 'light'];

        function getStoredTheme() {
            return localStorage.getItem('ftui-theme') || 'cyberpunk';
        }

        function setTheme(theme) {
            if (!THEMES.includes(theme)) theme = 'cyberpunk';

            // Update data attribute
            document.documentElement.setAttribute('data-theme', theme);

            // Store preference
            localStorage.setItem('ftui-theme', theme);

            // Update active button state
            document.querySelectorAll('[data-theme-btn]').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.themeBtn === theme);
            });

            // Dispatch custom event
            window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
        }

        function cycleTheme() {
            const current = getStoredTheme();
            const currentIndex = THEMES.indexOf(current);
            const nextIndex = (currentIndex + 1) % THEMES.length;
            setTheme(THEMES[nextIndex]);
        }

        // Apply stored theme on load (before content renders to prevent flash)
        (function() {
            const theme = getStoredTheme();
            document.documentElement.setAttribute('data-theme', theme);
        })();

        // Re-apply after DOM ready (for button states)
        document.addEventListener('DOMContentLoaded', () => {
            setTheme(getStoredTheme());
        });
    """)


def ThemeSwitcher(compact=False, cls='', **kwargs):
    """
    Theme switcher component.

    Args:
        compact: If True, shows only a cycle button instead of all options
        cls: Additional CSS classes
    """
    if compact:
        return Button(
            Span('\u25d0', cls="text-lg"),  # Circle with left half black
            onclick="cycleTheme()",
            cls=f"theme-switcher-compact btn {cls}",
            title="Cycle theme",
            type="button",
            **kwargs
        )

    # Full theme switcher with all options
    buttons = []
    for theme in THEMES:
        buttons.append(
            Button(
                Span(theme['icon'], cls="mr-1"),
                Span(theme['name'], cls="hidden sm:inline"),
                onclick=f"setTheme('{theme['id']}')",
                data_theme_btn=theme['id'],
                cls="theme-btn px-2 py-1 text-sm border border-transparent hover:border-accent-primary transition-all",
                type="button",
                title=theme['name']
            )
        )

    return Div(
        *buttons,
        cls=f"theme-switcher flex gap-1 flex-wrap {cls}",
        **kwargs
    )


def ThemeToggle(cls='', **kwargs):
    """
    Simple theme toggle button that cycles through themes.
    Shows current theme icon.
    """
    return Button(
        # Icons for each theme (shown/hidden based on current theme)
        Span('\u2726', cls="theme-icon", data_theme_icon="cyberpunk"),
        Span('\u263e', cls="theme-icon hidden", data_theme_icon="darcula"),
        Span('\u2744', cls="theme-icon hidden", data_theme_icon="nordic"),
        Span('\u2600', cls="theme-icon hidden", data_theme_icon="light"),
        onclick="cycleTheme()",
        cls=f"theme-toggle p-2 hover:glow-box-subtle transition-all {cls}",
        title="Change theme",
        type="button",
        **kwargs
    )
