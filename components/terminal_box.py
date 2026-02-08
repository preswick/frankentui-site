"""Terminal Box Components with Unicode Borders"""

from fasthtml.common import *

# Border character sets
BORDERS = {
    'rounded': {
        'tl': '\u256d', 'tr': '\u256e', 'bl': '\u2570', 'br': '\u256f',
        'h': '\u2500', 'v': '\u2502'
    },
    'square': {
        'tl': '\u250c', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518',
        'h': '\u2500', 'v': '\u2502'
    },
    'double': {
        'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255a', 'br': '\u255d',
        'h': '\u2550', 'v': '\u2551'
    },
    'heavy': {
        'tl': '\u250f', 'tr': '\u2513', 'bl': '\u2517', 'br': '\u251b',
        'h': '\u2501', 'v': '\u2503'
    }
}


def TerminalBox(*content, title=None, border='rounded', width=None, cls='', **kwargs):
    """
    Create a terminal-style box with Unicode borders.

    Args:
        content: Child elements
        title: Optional title in the top border
        border: Border style ('rounded', 'square', 'double', 'heavy')
        width: Optional width (CSS value)
        cls: Additional CSS classes
    """
    b = BORDERS.get(border, BORDERS['rounded'])

    # Build the top border line
    if title:
        title_text = f" {title} "
        # Pad with horizontal chars
        top_line = f"{b['tl']}{b['h']}{title_text}{b['h'] * 20}{b['tr']}"
    else:
        top_line = f"{b['tl']}{b['h'] * 30}{b['tr']}"

    # Build the bottom border line
    bottom_line = f"{b['bl']}{b['h'] * 30}{b['br']}"

    style = f"width: {width};" if width else ""

    return Div(
        # Top border
        Div(top_line, cls="text-muted select-none", style="font-family: var(--font-mono); line-height: 1;"),
        # Content with side borders
        Div(
            Span(b['v'], cls="text-muted select-none"),
            Div(*content, cls="flex-1 px-2"),
            Span(b['v'], cls="text-muted select-none"),
            cls="flex items-start"
        ),
        # Bottom border
        Div(bottom_line, cls="text-muted select-none", style="font-family: var(--font-mono); line-height: 1;"),
        cls=f"terminal-box font-mono {cls}",
        style=style,
        **kwargs
    )


def AsciiBox(*content, title=None, border='rounded', **kwargs):
    """
    Create a box using pure ASCII art borders (pre-rendered).
    Good for static content where exact alignment matters.
    """
    b = BORDERS.get(border, BORDERS['rounded'])

    # Pre-render the entire box as a PRE element
    lines = []

    # Top
    if title:
        title_padded = f" {title} "
        remaining = 28 - len(title_padded)
        lines.append(f"{b['tl']}{b['h']}{title_padded}{b['h'] * remaining}{b['tr']}")
    else:
        lines.append(f"{b['tl']}{b['h'] * 30}{b['tr']}")

    # Content placeholder (will be replaced)
    content_marker = "<<CONTENT>>"
    lines.append(f"{b['v']} {content_marker.ljust(28)} {b['v']}")

    # Bottom
    lines.append(f"{b['bl']}{b['h'] * 30}{b['br']}")

    box_text = '\n'.join(lines)

    return Div(
        Pre(box_text.replace(content_marker, ""), cls="ascii-box text-muted m-0"),
        Div(*content, cls="ascii-box-content"),
        cls="relative",
        **kwargs
    )


def Panel(*content, title=None, actions=None, cls='', **kwargs):
    """
    Create a panel with optional header and actions.

    Args:
        content: Panel body content
        title: Panel title
        actions: Optional actions/buttons for the header
        cls: Additional CSS classes
    """
    header = None
    if title or actions:
        header = Div(
            H3(title, cls="panel-title") if title else None,
            Div(actions) if actions else None,
            cls="panel-header"
        )

    return Div(
        header,
        Div(*content, cls="panel-content"),
        cls=f"panel {cls}",
        **kwargs
    )


def Card(title, description=None, href=None, tags=None, cls='', **kwargs):
    """
    Create a card component for grid layouts.

    Args:
        title: Card title
        description: Card description
        href: Optional link URL
        tags: Optional list of tags
        cls: Additional CSS classes
    """
    tag_elements = None
    if tags:
        tag_elements = Div(
            *[Span(tag, cls="tag tag-primary") for tag in tags],
            cls="mt-2"
        )

    content = Div(
        H4(title, cls="card-title"),
        P(description, cls="card-description") if description else None,
        tag_elements,
        cls="card-body"
    )

    if href:
        return A(
            content,
            href=href,
            cls=f"card block no-underline {cls}",
            **kwargs
        )

    return Div(
        content,
        cls=f"card {cls}",
        **kwargs
    )
