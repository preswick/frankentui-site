"""
Personal Website with Terminal Visual Effects

A minimal personal website featuring retro visual effects,
social links, and blog posts.
"""

import frontmatter
from pathlib import Path
from datetime import datetime
from fasthtml.common import *
from monsterui.all import render_md

from components import TerminalBox, ThemeSwitcher, theme_script

# ============================================
# Application Setup
# ============================================

css_files = [
    Link(rel="stylesheet", href="/static/css/terminal.css"),
    Link(rel="stylesheet", href="/static/css/effects.css"),
    Link(rel="stylesheet", href="/static/css/borders.css"),
    Link(rel="stylesheet", href="/static/css/themes/cyberpunk.css"),
    Link(rel="stylesheet", href="/static/css/themes/darcula.css"),
    Link(rel="stylesheet", href="/static/css/themes/nordic.css"),
    Link(rel="stylesheet", href="/static/css/themes/light.css"),
]

fonts = [
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
    Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap"),
]

hdrs = (
    *fonts,
    *css_files,
    theme_script(),
    Script(src="/static/js/effects.js"),
    Meta(name="viewport", content="width=device-width, initial-scale=1"),
    Meta(name="description", content="Personal website"),
    Style("""
        .effect-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }
        .content-overlay {
            position: relative;
            z-index: 1;
            background: rgba(26, 31, 41, 0.85);
            backdrop-filter: blur(4px);
        }
        [data-theme="light"] .content-overlay {
            background: rgba(238, 241, 245, 0.9);
        }
        .social-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.25rem;
            border: 1px solid var(--accent-primary);
            transition: all 0.2s ease;
            font-size: 0.9rem;
        }
        .social-link:hover {
            background: var(--accent-primary);
            color: var(--bg-deep);
            box-shadow: 0 0 20px var(--accent-primary);
        }
        .effect-btn {
            padding: 0.75rem 1rem;
            border: 1px solid var(--fg-muted);
            background: var(--bg-surface);
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: var(--font-mono);
            font-size: 0.875rem;
            min-width: 5rem;
            text-align: center;
        }
        @media (min-width: 640px) {
            .effect-btn {
                padding: 0.5rem 1rem;
                font-size: 0.75rem;
            }
        }
        .effect-btn:hover, .effect-btn.active {
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }
        .blog-card {
            border: 1px solid var(--bg-overlay);
            padding: 1rem;
            transition: all 0.2s ease;
        }
        .blog-card:hover {
            border-color: var(--accent-primary);
            box-shadow: 0 0 10px rgba(0, 170, 255, 0.2);
        }
    """),
)

app = FastHTML(hdrs=hdrs)
app.mount("/static", StaticFiles(directory="static"), name="static")
rt = app.route


# ============================================
# Utilities
# ============================================

def hx_attrs(target="#main-content"):
    return dict(hx_target=target, hx_push_url="true", hx_swap="innerHTML show:window:top")


def hx_link(text, href, cls="", **kwargs):
    return A(text, href=href, hx_get=href, cls=cls, **hx_attrs(), **kwargs)


class Post:
    def __init__(self, path):
        self.path = Path(path)
        self.slug = self.path.stem
        post = frontmatter.load(path)
        self.content = post.content
        self.meta = post.metadata
        self.title = self.meta.get('title', 'Untitled')
        self.date = self.meta.get('date', datetime.now())
        self.excerpt = self.meta.get('excerpt', '')
        self.tags = self.meta.get('tags', [])
        self.datestr = self.date.strftime('%Y-%m-%d')


def get_posts(n=None):
    posts_dir = Path('posts')
    if not posts_dir.exists():
        return []
    posts = sorted(
        [Post(p) for p in posts_dir.glob('*.md')],
        key=lambda p: p.date,
        reverse=True
    )
    return posts[:n] if n else posts


# ============================================
# Social Links
# ============================================

SOCIALS = [
    {'name': 'GitHub', 'url': 'https://github.com/preswick', 'icon': '\uf09b'},
    {'name': 'LinkedIn', 'url': 'https://linkedin.com/in/preswick', 'icon': '\uf0e1'},
    {'name': 'X', 'url': 'https://x.com/rpreswick', 'icon': '\u2715'},
]


def social_links():
    return Div(
        *[A(
            Span(s['name']),
            href=s['url'],
            target="_blank",
            rel="noopener noreferrer",
            cls="social-link"
        ) for s in SOCIALS],
        cls="flex flex-wrap gap-4 justify-center"
    )


# ============================================
# Effect Controls
# ============================================

EFFECTS = ['matrix', 'plasma', 'fire', 'starfield']


def effect_controls():
    return Div(
        Span("Effect:", cls="text-muted text-sm mb-2 block text-center sm:hidden"),
        Span("Effect: ", cls="text-muted text-sm mr-2 hidden sm:inline"),
        Div(
            *[Button(
                effect.capitalize(),
                onclick=f"effectManager.init('bg-canvas', '{effect}')",
                cls="effect-btn flex-1 sm:flex-none",
                id=f"btn-{effect}"
            ) for effect in EFFECTS],
            cls="grid grid-cols-2 gap-2 w-full sm:flex sm:flex-wrap sm:justify-center sm:gap-2 sm:w-auto"
        ),
        cls="flex flex-col sm:flex-row items-center gap-2 justify-center"
    )


# ============================================
# Layout
# ============================================

def navbar():
    brand = A(
        Span("RP", cls="font-bold text-accent-primary"),
        href="/", hx_get="/",
        cls="text-lg",
        **hx_attrs()
    )

    links = Div(
        hx_link("Home", "/", cls="hover:text-accent-primary transition-all"),
        hx_link("Blog", "/blog", cls="hover:text-accent-primary transition-all"),
        cls="flex gap-10 items-center"
    )

    return Nav(
        Div(
            brand,
            links,
            ThemeSwitcher(compact=True),
            cls="flex items-center justify-between container py-4"
        ),
        cls="bg-surface border-b border-overlay"
    )


def layout(*content, title=None, htmx=None, show_effects=True):
    page_title = f"{title}" if title else "Robbie Preswick"

    if htmx and htmx.request:
        return (Title(page_title), *content)

    canvas = Canvas(id="bg-canvas", cls="effect-canvas") if show_effects else None
    init_script = Script("document.addEventListener('DOMContentLoaded', () => effectManager.init('bg-canvas', 'matrix'));") if show_effects else None

    main = Main(
        *content,
        cls="container py-8 flex-1",
        id="main-content"
    )

    return (
        Title(page_title),
        Body(cls="min-h-screen flex flex-col")(
            canvas,
            Div(cls="flex flex-col min-h-screen")(
                navbar(),
                Div(main, cls="content-overlay flex-1"),
                Footer(
                    Div(
                        Span("\u00a9 2025", cls="text-muted text-sm"),
                        cls="container py-4 text-center"
                    ),
                    cls="content-overlay border-t border-overlay"
                )
            ),
            init_script
        )
    )


# ============================================
# Pages
# ============================================

@rt('/')
def index(htmx=None):
    """Home page with visual effects and social links."""

    hero = Div(
        H1("Robbie Preswick", cls="text-3xl md:text-4xl font-bold mb-4 glow-text-subtle"),
        P("Builder of things.", cls="text-secondary text-lg mb-8"),
        social_links(),
        cls="text-center py-12"
    )

    effects_section = Div(
        H2("Visual Effects", cls="text-xl font-semibold mb-4 text-center"),
        effect_controls(),
        cls="py-8 border-t border-overlay"
    )

    # Recent posts
    posts = get_posts(3)
    post_items = []
    for p in posts:
        post_items.append(
            Div(
                hx_link(
                    Div(
                        H3(p.title, cls="font-semibold mb-1"),
                        P(p.excerpt, cls="text-muted text-sm") if p.excerpt else None,
                        Span(p.datestr, cls="text-muted text-xs"),
                    ),
                    f"/blog/{p.slug}",
                    cls="block"
                ),
                cls="blog-card"
            )
        )

    blog_section = Div(
        Div(
            H2("Recent Posts", cls="text-xl font-semibold"),
            hx_link("View all \u2192", "/blog", cls="text-sm text-accent-link"),
            cls="flex justify-between items-center mb-4"
        ),
        Div(*post_items, cls="grid gap-4") if post_items else P("No posts yet.", cls="text-muted"),
        cls="py-8 border-t border-overlay"
    )

    return layout(
        hero,
        effects_section,
        blog_section,
        title="Home",
        htmx=htmx
    )


@rt('/blog')
def blog(htmx=None):
    """Blog listing page."""
    posts = get_posts()

    if not posts:
        return layout(
            H1("Blog", cls="text-2xl font-bold mb-8"),
            P("No blog posts yet. Check back soon!", cls="text-muted"),
            title="Blog",
            htmx=htmx
        )

    post_cards = []
    for p in posts:
        tags = Div(
            *[Span(tag, cls="tag tag-primary") for tag in p.tags],
            cls="flex gap-2 flex-wrap"
        ) if p.tags else None

        post_cards.append(
            Div(
                hx_link(
                    Div(
                        H3(p.title, cls="font-semibold mb-2"),
                        P(p.excerpt, cls="text-secondary text-sm mb-2") if p.excerpt else None,
                        Div(
                            Span(p.datestr, cls="text-muted text-sm"),
                            tags,
                            cls="flex justify-between items-center flex-wrap gap-2"
                        ),
                    ),
                    f"/blog/{p.slug}",
                    cls="block"
                ),
                cls="blog-card"
            )
        )

    return layout(
        H1("Blog", cls="text-2xl font-bold mb-8"),
        Div(*post_cards, cls="grid gap-4"),
        title="Blog",
        htmx=htmx
    )


@rt('/blog/{slug}')
def blogpost(slug: str, htmx=None):
    """Individual blog post page."""
    post_path = Path('posts') / f'{slug}.md'

    if not post_path.exists():
        return layout(
            H2("404 - Post Not Found", cls="text-accent-error text-2xl mb-4"),
            P("The requested post could not be found.", cls="text-muted mb-4"),
            hx_link("\u2190 Back to blog", "/blog", cls="text-accent-link"),
            title="Not Found",
            htmx=htmx
        )

    p = Post(post_path)

    tags = Div(
        *[Span(tag, cls="tag tag-primary") for tag in p.tags],
        cls="flex gap-2 flex-wrap"
    ) if p.tags else None

    header = Div(
        H1(p.title, cls="text-2xl font-bold mb-2"),
        Div(
            Span(p.date.strftime('%B %d, %Y'), cls="text-muted"),
            tags,
            cls="flex justify-between items-center flex-wrap gap-4 mb-8"
        )
    )

    content = render_md(p.content)

    footer = Div(
        Hr(cls="divider my-8"),
        hx_link("\u2190 Back to blog", "/blog", cls="text-accent-link"),
    )

    return layout(
        Article(
            header,
            Div(content, cls="prose"),
            footer,
            cls="max-w-2xl"
        ),
        title=p.title,
        htmx=htmx
    )


# ============================================
# Run
# ============================================

if __name__ == "__main__":
    serve()
