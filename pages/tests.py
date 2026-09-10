"""Smoke tests: pages render from seeded-style data, contact form works."""

from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from pages.models import Capability, Inquiry, Post, Project, SiteSettings

TEST_SETTINGS = {
    "SECURE_SSL_REDIRECT": False,
    "STORAGES": {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    },
}

VALID_INQUIRY = {
    "name": "Jane Doe",
    "company": "Acme Corp",
    "email": "jane@example.com",
    "phone": "555-0100",
    "scope": "high-voltage",
    "message": "We need a substation assessment for our Chicago facility.",
    "website": "",
}


@override_settings(**TEST_SETTINGS)
class PageTests(TestCase):
    def setUp(self):
        SiteSettings.load()
        Project.objects.create(
            client="TEST CLIENT",
            title="Campus Fiber",
            slug="campus-fiber",
            year="2024",
            scope="FIBER OPTICS",
            blurb="A test project.",
            is_published=True,
        )
        Post.objects.create(
            title="From the field",
            slug="from-the-field",
            excerpt="A test post.",
            body="Hello from Chicago.",
            is_published=True,
        )

    def test_pages_render(self):
        for name in ["home", "services", "projects", "about", "careers", "journal", "contact"]:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_project_detail(self):
        response = self.client.get(reverse("project_detail", args=["campus-fiber"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Campus Fiber")

    def test_unpublished_project_is_404(self):
        Project.objects.filter(slug="campus-fiber").update(is_published=False)
        response = self.client.get(reverse("project_detail", args=["campus-fiber"]))
        self.assertEqual(response.status_code, 404)

    def test_unknown_url_returns_custom_404(self):
        response = self.client.get("/does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "PAGE NOT FOUND", status_code=404)

    def test_sitemap_and_robots(self):
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sitemap:")
        self.assertContains(response, "Disallow: /editor/")

    def test_chicago_copy_on_home(self):
        response = self.client.get("/")
        self.assertContains(response, "Chicagoland")

    def test_editor_login_page(self):
        response = self.client.get("/editor/login/")
        self.assertEqual(response.status_code, 200)

    def test_unpublished_post_is_404(self):
        Post.objects.filter(slug="from-the-field").update(is_published=False)
        response = self.client.get(reverse("post_detail", args=["from-the-field"]))
        self.assertEqual(response.status_code, 404)

    def test_healthz(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    def test_home_has_seo_and_skip_link(self):
        response = self.client.get("/")
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, 'property="og:image"')
        self.assertContains(response, "Skip to content")
        self.assertContains(response, 'id="main"')

    def test_capability_placeholders(self):
        design = Capability(title="DESIGN", bullets="x")
        build = Capability(title="BUILD", bullets="x")
        service = Capability(title="SERVICE", bullets="x")
        other = Capability(title="OTHER", bullets="x")
        self.assertEqual(design.placeholder_static, "img/engineering-placeholder.svg")
        self.assertEqual(build.placeholder_static, "img/installation-placeholder.svg")
        self.assertEqual(service.placeholder_static, "img/commissioning-placeholder.svg")
        self.assertEqual(other.placeholder_static, "img/engineering-placeholder.svg")

    def test_phone_href_strips_formatting(self):
        site = SiteSettings.load()
        site.phone = "+1 (312) 555-0142"
        self.assertEqual(site.phone_href, "tel:+13125550142")


@override_settings(**TEST_SETTINGS)
class ContactFormTests(TestCase):
    def setUp(self):
        SiteSettings.load()

    def test_blank_submission_shows_errors(self):
        response = self.client.post(reverse("contact"), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(len(mail.outbox), 0)

    def test_short_message_rejected(self):
        data = {**VALID_INQUIRY, "message": "hi"}
        response = self.client.post(reverse("contact"), data)
        self.assertIn("message", response.context["form"].errors)
        self.assertEqual(len(mail.outbox), 0)

    def test_valid_submission_sends_email_and_redirects(self):
        response = self.client.post(reverse("contact"), VALID_INQUIRY)
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(Inquiry.objects.count(), 1)
        email = mail.outbox[0]
        self.assertIn("Jane Doe", email.subject)
        self.assertIn("high-voltage", email.subject)
        self.assertIn("substation assessment", email.body)

    def test_honeypot_drops_spam_silently(self):
        data = {**VALID_INQUIRY, "website": "https://spam.example"}
        response = self.client.post(reverse("contact"), data)
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Inquiry.objects.count(), 0)

    @patch("pages.views.send_mail", side_effect=OSError("smtp down"))
    def test_email_failure_still_saves_inquiry(self, _mock):
        response = self.client.post(reverse("contact"), VALID_INQUIRY, follow=True)
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertContains(response, "MESSAGE RECEIVED")
