from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post, Project


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return ["home", "services", "projects", "about", "careers", "journal", "contact"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):  # type: ignore[override]
        return 1.0 if item == "home" else 0.8


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_published=True)


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.filter(is_published=True)
