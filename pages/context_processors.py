from .models import MarqueeItem, Post, SiteSettings

NAV_LINKS = [
    {"label": "SERVICES", "url_name": "services"},
    {"label": "PROJECTS", "url_name": "projects"},
    {"label": "ABOUT", "url_name": "about"},
    {"label": "CAREERS", "url_name": "careers"},
    {"label": "CONTACT", "url_name": "contact"},
]


def site_data(request):
    nav = list(NAV_LINKS)
    has_posts = Post.objects.filter(is_published=True).exists()
    if has_posts:
        nav.insert(2, {"label": "JOURNAL", "url_name": "journal"})
    return {
        "site": SiteSettings.load(),
        "nav_links": nav,
        "marquee_items": MarqueeItem.objects.all(),
        "has_posts": has_posts,
    }
