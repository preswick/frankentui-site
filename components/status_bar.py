"""Vim-style Status Bar Component"""

from fasthtml.common import *
from datetime import datetime

def status_item(content, cls='', separator=True, **kwargs):
    """
    Create a status bar item.

    Args:
        content: Item content
        cls: Additional CSS classes
        separator: Whether to show separator before this item
    """
    sep = Span('\u2502', cls="text-muted mx-2") if separator else None  # Vertical bar

    return Span(
        sep,
        Span(content, cls=cls),
        **kwargs
    )


def StatusBar(
    left=None,
    center=None,
    right=None,
    mode=None,
    file_info=None,
    position=None,
    cls='',
    **kwargs
):
    """
    Create a Vim-style status bar footer.

    Args:
        left: Content for left section
        center: Content for center section
        right: Content for right section
        mode: Optional mode indicator (like Vim's NORMAL/INSERT)
        file_info: Optional file info text
        position: Optional position indicator (like line:col)
        cls: Additional CSS classes
    """
    # Build left section
    left_content = []
    if mode:
        mode_cls = {
            'NORMAL': 'bg-accent-primary',
            'INSERT': 'bg-accent-success',
            'VISUAL': 'bg-accent-secondary',
            'COMMAND': 'bg-accent-warning',
        }.get(mode.upper(), 'bg-accent-primary')

        left_content.append(
            Span(
                f" {mode.upper()} ",
                cls=f"{mode_cls} text-bg-deep font-bold px-2"
            )
        )

    if left:
        left_content.append(Span(left, cls="ml-2"))

    # Build center section
    center_content = []
    if file_info:
        center_content.append(Span(file_info, cls="text-muted"))
    if center:
        center_content.append(center)

    # Build right section
    right_content = []
    if right:
        right_content.append(Span(right))
    if position:
        right_content.append(Span(position, cls="text-muted ml-2"))

    return Footer(
        Div(
            # Left section
            Div(*left_content, cls="flex items-center"),
            # Center section
            Div(*center_content, cls="flex items-center justify-center flex-1"),
            # Right section
            Div(*right_content, cls="flex items-center"),
            cls="flex items-center justify-between w-full"
        ),
        cls=f"status-bar fixed bottom-0 left-0 right-0 bg-surface border-t border-overlay px-4 py-2 font-mono text-sm {cls}",
        **kwargs
    )


def SimpleStatusBar(left_text='', right_text='', cls='', **kwargs):
    """
    Create a simple status bar with left and right text.
    """
    return Footer(
        Div(
            Span(left_text, cls="text-muted"),
            Span(right_text, cls="text-muted"),
            cls="flex justify-between items-center container"
        ),
        cls=f"status-bar bg-surface border-t border-overlay py-3 {cls}",
        **kwargs
    )


def PageFooter(site_name='FrankenTUI', show_time=False, cls='', **kwargs):
    """
    Create a page footer with optional live time display.
    """
    time_element = None
    if show_time:
        time_element = Span(
            datetime.now().strftime('%H:%M'),
            id="footer-time",
            cls="text-accent-primary"
        )

    return Footer(
        Div(
            Div(
                Span('\u2726 ', cls="text-accent-primary"),  # Star
                Span(site_name, cls="font-bold"),
                Span(' \u2726', cls="text-accent-primary"),
                cls="flex items-center gap-1"
            ),
            Div(
                time_element,
                Span(' | ', cls="text-muted") if show_time else None,
                Span('\u00a9 2025', cls="text-muted"),
                cls="flex items-center"
            ) if show_time else Span('\u00a9 2025', cls="text-muted"),
            cls="flex justify-between items-center"
        ),
        cls=f"container py-6 border-t border-overlay mt-auto {cls}",
        **kwargs
    )
