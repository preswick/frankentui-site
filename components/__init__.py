"""FrankenTUI Components for FastHTML"""

from .terminal_box import TerminalBox, AsciiBox, Panel, Card
from .theme_switcher import ThemeSwitcher, theme_script
from .status_bar import StatusBar, status_item, PageFooter, SimpleStatusBar

__all__ = [
    'TerminalBox', 'AsciiBox', 'Panel', 'Card',
    'ThemeSwitcher', 'theme_script',
    'StatusBar', 'status_item', 'PageFooter', 'SimpleStatusBar'
]
