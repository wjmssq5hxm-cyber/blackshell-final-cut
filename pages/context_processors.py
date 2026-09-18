from .models import MarqueeItem, Post, Project, SiteSettings

NAV_LINKS = [
    {"label": "SERVICES", "url_name": "services"},
    {"label": "ABOUT", "url_name": "about"},
    {"label": "CAREERS", "url_name": "careers"},
    {"label": "CONTACT", "url_name": "contact"},
]


def site_data(request):
    nav = list(NAV_LINKS)
    has_projects = Project.objects.filter(is_published=True).exists()
    has_posts = Post.objects.filter(is_published=True).exists()
    if has_projects:
        nav.insert(1, {"label": "PROJECTS", "url_name": "projects"})
    if has_posts:
        about_idx = next(i for i, link in enumerate(nav) if link["url_name"] == "about")
        nav.insert(about_idx, {"label": "JOURNAL", "url_name": "journal"})
    return {
        "site": SiteSettings.load(),
        "nav_links": nav,
        "marquee_items": MarqueeItem.objects.all(),
        "has_posts": has_posts,
        "has_projects": has_projects,
    }
