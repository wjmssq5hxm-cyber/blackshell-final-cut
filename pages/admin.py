"""A deliberately simple editor: fieldsets, help text, photo previews."""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Capability,
    Inquiry,
    JobOpening,
    MarqueeItem,
    Post,
    PostPhoto,
    Project,
    ProjectPhoto,
    Service,
    SiteSettings,
    TechService,
    Value,
)

admin.site.site_header = "Black Shell Editor"
admin.site.site_title = "Black Shell"
admin.site.index_title = "What do you want to change?"


class PhotoPreviewMixin:
    @admin.display(description="Photo")
    def thumb(self, obj):
        image = getattr(obj, "image", None) or getattr(obj, "cover_image", None)
        if not image:
            return "—"
        return format_html(
            '<img src="{}" alt="" style="height:48px;width:48px;object-fit:cover;border-radius:4px;background:#111"/>',
            image.url,
        )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Company",
            {
                "fields": (
                    "company_name",
                    "phone",
                    "email",
                    "city",
                    "service_area",
                    "founded_year",
                    "licensed_states",
                    "license_label",
                    "license_number",
                    "side_rail",
                ),
                "description": "Name, phone, email, license — the facts on every page.",
            },
        ),
        (
            "Home page",
            {
                "fields": (
                    "hero_headline",
                    "hero_tagline",
                    "hero_body",
                    "hero_caption_1",
                    "hero_caption_2",
                    "hero_caption_3",
                    "capabilities_label",
                ),
            },
        ),
        (
            "About page",
            {
                "fields": (
                    "about_eyebrow",
                    "about_headline",
                    "about_p1",
                    "about_p2",
                    "about_p3",
                ),
            },
        ),
        (
            "Services page",
            {
                "fields": (
                    "services_eyebrow",
                    "services_headline",
                    "services_intro",
                    "tech_eyebrow",
                    "tech_headline",
                    "tech_intro",
                ),
            },
        ),
        (
            "Projects page",
            {
                "fields": (
                    "projects_eyebrow",
                    "projects_headline",
                    "projects_intro",
                ),
            },
        ),
        (
            "Careers page",
            {
                "fields": (
                    "careers_eyebrow",
                    "careers_headline",
                    "careers_intro",
                    "careers_footer",
                ),
            },
        ),
        (
            "Journal page",
            {
                "fields": (
                    "journal_eyebrow",
                    "journal_headline",
                    "journal_intro",
                ),
            },
        ),
        (
            "Contact page",
            {
                "fields": (
                    "contact_eyebrow",
                    "contact_headline",
                    "contact_intro",
                    "contact_success",
                    "contact_success_body",
                ),
            },
        ),
        (
            "Search engines (optional)",
            {
                "classes": ("collapse",),
                "fields": ("meta_title", "meta_description"),
                "description": "The title and description Google shows. Safe to ignore.",
            },
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return redirect(reverse("admin:pages_sitesettings_change", args=[obj.pk]))


@admin.register(MarqueeItem)
class MarqueeItemAdmin(admin.ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)


@admin.register(Capability)
class CapabilityAdmin(PhotoPreviewMixin, admin.ModelAdmin):
    list_display = ("thumb", "title", "order")
    list_editable = ("order",)
    list_display_links = ("thumb", "title")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("tag", "title", "order")
    list_editable = ("order",)


@admin.register(TechService)
class TechServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ("label", "title", "order")
    list_editable = ("order",)


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "job_type", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)


class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 1
    fields = ("image", "caption", "order")


@admin.register(Project)
class ProjectAdmin(PhotoPreviewMixin, admin.ModelAdmin):
    list_display = ("thumb", "title", "client", "year", "scope", "is_published", "order")
    list_editable = ("is_published", "order")
    list_display_links = ("thumb", "title")
    list_filter = ("is_published", "scope")
    search_fields = ("title", "client", "blurb", "body")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectPhotoInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "client",
                    "title",
                    "slug",
                    "year",
                    "scope",
                    "blurb",
                    "body",
                    "cover_image",
                    "is_published",
                    "order",
                ),
                "description": "Add a cover photo here. Extra photos go in the gallery below.",
            },
        ),
    )


class PostPhotoInline(admin.TabularInline):
    model = PostPhoto
    extra = 1
    fields = ("image", "caption", "order")


@admin.register(Post)
class PostAdmin(PhotoPreviewMixin, admin.ModelAdmin):
    list_display = ("thumb", "title", "is_published", "published_at")
    list_editable = ("is_published",)
    list_display_links = ("thumb", "title")
    list_filter = ("is_published",)
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PostPhotoInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "body",
                    "cover_image",
                    "is_published",
                    "published_at",
                    "order",
                ),
                "description": "Unpublished posts stay off the website until you check “Show on the website.” Extra photos go in the gallery below.",
            },
        ),
    )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "scope", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "scope")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = (
        "name",
        "company",
        "email",
        "phone",
        "scope",
        "message",
        "created_at",
    )

    def has_add_permission(self, request):
        return False
