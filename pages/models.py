"""All site content lives in the database so it can be edited in /editor/."""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SiteSettings(models.Model):
    """Singleton: one row, every piece of site-wide copy."""

    company_name = models.CharField(
        "Company name",
        max_length=80,
        default="Black Shell Technology",
    )
    phone = models.CharField(
        "Phone number",
        max_length=40,
        default="+1 (555) 555-0142",
        help_text="Shown on the contact page. Example: +1 (312) 555-0142",
    )
    email = models.EmailField(
        "Public email",
        default="projects@blackshell.tech",
        help_text="The address visitors see. Inquiries also go here unless you change the server setting.",
    )
    founded_year = models.CharField("Founded year", max_length=8, default="2018")
    licensed_states = models.CharField(
        "Licensed states",
        max_length=40,
        default="IL · IN · WI",
        help_text="Shown on the About page. Example: IL · IN · WI",
    )
    license_label = models.CharField(
        "License label",
        max_length=40,
        default="CHICAGO EC",
        help_text="Short label above the license number.",
    )
    license_number = models.CharField(
        "License number",
        max_length=40,
        default="#SE-014277",
    )
    city = models.CharField("City line", max_length=80, default="Chicago, IL")
    service_area = models.CharField(
        "Service area",
        max_length=160,
        default="Chicago, IL — serving Chicagoland & the greater IL · IN · WI region",
    )
    side_rail = models.CharField(
        "Left-edge rail text",
        max_length=80,
        default="DESIGN  •  BUILD  •  SERVICE",
        help_text="The vertical text on large screens.",
    )

    hero_headline = models.TextField(
        "Home headline",
        default="INFRASTRUCTURE\nFOR WHAT'S NEXT.",
        help_text="One line per row. It will break exactly where you press Enter.",
    )
    hero_tagline = models.TextField(
        "Home tagline",
        default="A full-service electrical and technology contractor serving retail, commercial, and industrial clients across Chicagoland.",
    )
    hero_body = models.TextField(
        "Home supporting line",
        default="We hold safety, sustainability, and precision at the center of every project we deliver.",
    )
    hero_caption_1 = models.CharField(
        "Spiral caption — line 1",
        max_length=80,
        default="BLACK SHELL TECHNOLOGY",
    )
    hero_caption_2 = models.CharField(
        "Spiral caption — line 2",
        max_length=80,
        default="DESIGN · BUILD · SERVICE",
    )
    hero_caption_3 = models.CharField(
        "Spiral caption — line 3",
        max_length=80,
        default="DELIVERING WORK YOU CAN COUNT ON",
    )
    capabilities_label = models.CharField(
        "Home cards label",
        max_length=40,
        default="ENGAGEMENT",
    )

    about_eyebrow = models.CharField("About label", max_length=40, default="ABOUT")
    about_headline = models.TextField(
        "About headline",
        default="BUILT ON\nDISCIPLINE.",
        help_text="One line per row.",
    )
    about_p1 = models.TextField(
        "About — paragraph 1",
        default="Founded in 2018, Black Shell Technology is a woman-owned, full-service electrical and technology contractor rooted in the Chicago area, serving retail, commercial, and industrial clients.",
    )
    about_p2 = models.TextField(
        "About — paragraph 2",
        default="We work where downtime is not an option. Multi-site retail rollouts. Commercial build-outs. Distribution centers and manufacturing floors. Our crews carry the certifications and craft discipline these environments require.",
    )
    about_p3 = models.TextField(
        "About — paragraph 3",
        default="We are committed to a single principle: every project deserves the same craft discipline, regardless of scale. Our team was founded by veterans of the electrical and fiber trades, and that conviction shapes every decision we make.",
    )

    services_eyebrow = models.CharField("Services label", max_length=40, default="SERVICES")
    services_headline = models.CharField(
        "Services headline",
        max_length=80,
        default="WHAT WE DELIVER.",
    )
    services_intro = models.TextField(
        "Services intro",
        default="Forward-thinking electrical and technology solutions that bridge advanced engineering with flawless execution. From renewable energy systems to intelligent building infrastructure — delivered on time, on budget, and to the highest standards of safety and sustainability.",
    )
    tech_eyebrow = models.CharField("Tech list label", max_length=40, default="TECH SOLUTIONS")
    tech_headline = models.CharField(
        "Tech list headline",
        max_length=80,
        default="DYNAMIC & CUSTOMIZED TECH.",
    )
    tech_intro = models.TextField(
        "Tech list intro",
        default="A robust suite of services designed to ensure your technology infrastructure doesn't just get by — it thrives. Working directly with your team, we design and implement tailor-made strategies that are seamlessly integrated, highly efficient, and built to scale.",
    )

    projects_eyebrow = models.CharField("Projects label", max_length=40, default="PROJECTS")
    projects_headline = models.CharField(
        "Projects headline",
        max_length=80,
        default="WORK YOU CAN COUNT ON.",
    )
    projects_intro = models.TextField(
        "Projects intro",
        default="A sample of recent electrical and technology work across Chicagoland — retail rollouts, commercial build-outs, and the infrastructure that keeps operations running.",
    )

    careers_eyebrow = models.CharField("Careers label", max_length=40, default="CAREERS")
    careers_headline = models.CharField(
        "Careers headline",
        max_length=80,
        default="JOIN THE CREW.",
    )
    careers_intro = models.TextField(
        "Careers intro",
        default="We back our team — competitive pay, full benefits, room to grow your craft, and the kind of projects you'll tell stories about for the rest of your career.",
    )
    careers_footer = models.TextField(
        "Careers closing line",
        default="Don't see the right role? Reach out anyway — we're always interested in connecting with skilled trades-people who care about their craft.",
    )

    journal_eyebrow = models.CharField("Journal label", max_length=40, default="JOURNAL")
    journal_headline = models.CharField(
        "Journal headline",
        max_length=80,
        default="FROM THE FIELD.",
    )
    journal_intro = models.TextField(
        "Journal intro",
        default="Notes, project stories, and the occasional dispatch from the shop.",
    )

    contact_eyebrow = models.CharField("Contact label", max_length=40, default="CONTACT")
    contact_headline = models.TextField(
        "Contact headline",
        default="START\nYOUR\nPROJECT.",
        help_text="One line per row.",
    )
    contact_intro = models.TextField(
        "Contact intro",
        default="Tell us about the project. We respond within one business day — often sooner.",
    )
    contact_success = models.CharField(
        "Thank-you message",
        max_length=80,
        default="MESSAGE RECEIVED.",
    )
    contact_success_body = models.CharField(
        "Thank-you supporting line",
        max_length=160,
        default="A member of our team will be in touch within one business day.",
    )

    meta_title = models.CharField(
        "Browser tab title",
        max_length=120,
        default="Black Shell Technology — Retail, Commercial & Industrial Electrical Contractor · Chicago",
    )
    meta_description = models.TextField(
        "Search-engine description",
        default="A woman-owned, full-service electrical and technology contractor serving retail, commercial, and industrial clients across the Chicago area. We hold safety, sustainability, and precision at the center of every project we deliver.",
    )

    class Meta:
        verbose_name = "Site text"
        verbose_name_plural = "Site text"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def phone_href(self):
        cleaned = "".join(ch for ch in self.phone if ch.isdigit() or ch == "+")
        return f"tel:{cleaned}" if cleaned else ""


class OrderedModel(models.Model):
    order = models.PositiveIntegerField(
        "Order",
        default=0,
        help_text="Lower numbers show first.",
    )

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class MarqueeItem(OrderedModel):
    text = models.CharField("Line of text", max_length=80)

    class Meta(OrderedModel.Meta):
        verbose_name = "Marquee line"
        verbose_name_plural = "Marquee lines (footer ticker)"

    def __str__(self):
        return self.text


class Capability(OrderedModel):
    title = models.CharField("Title", max_length=40)
    bullets = models.TextField(
        "Bullet list",
        help_text="One bullet per line.",
    )
    image = models.ImageField(
        "Photo",
        upload_to="capabilities/",
        blank=True,
        help_text="Square-ish photos work best. If you leave this empty, a placeholder is used.",
    )

    class Meta(OrderedModel.Meta):
        verbose_name = "Home page card"
        verbose_name_plural = "Home page cards (Design / Build / Service)"

    def __str__(self):
        return self.title

    def bullet_list(self):
        return [line.strip() for line in self.bullets.splitlines() if line.strip()]

    @property
    def placeholder_static(self):
        key = (self.title or "").strip().upper()
        return {
            "DESIGN": "img/engineering-placeholder.svg",
            "BUILD": "img/installation-placeholder.svg",
            "SERVICE": "img/commissioning-placeholder.svg",
        }.get(key, "img/engineering-placeholder.svg")


class Service(OrderedModel):
    tag = models.CharField(
        "Small label",
        max_length=20,
        help_text="Shown in caps next to the number. Example: DESIGN",
    )
    title = models.CharField("Title", max_length=80)
    copy = models.TextField("Description")
    bullets = models.TextField(
        "Bullet list",
        help_text="One bullet per line.",
    )

    class Meta(OrderedModel.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services (the three big ones)"

    def __str__(self):
        return self.title

    def bullet_list(self):
        return [line.strip() for line in self.bullets.splitlines() if line.strip()]


class TechService(OrderedModel):
    name = models.CharField("Name", max_length=80)

    class Meta(OrderedModel.Meta):
        verbose_name = "Tech service"
        verbose_name_plural = "Tech services (the long list)"

    def __str__(self):
        return self.name


class Value(OrderedModel):
    label = models.CharField(
        "Small label",
        max_length=40,
        help_text="Example: 01 / DISCIPLINE",
    )
    title = models.CharField("Title", max_length=80)
    copy = models.TextField("Description")

    class Meta(OrderedModel.Meta):
        verbose_name = "About value"
        verbose_name_plural = "About values (the three columns)"

    def __str__(self):
        return self.title


class JobOpening(OrderedModel):
    title = models.CharField("Job title", max_length=80)
    location = models.CharField("Location", max_length=80, default="Chicago, IL")
    job_type = models.CharField(
        "Type",
        max_length=40,
        default="Full-time",
        help_text="Example: Full-time, Apprenticeship",
    )
    is_active = models.BooleanField(
        "Show on the website",
        default=True,
        help_text="Uncheck to hide this job without deleting it.",
    )

    class Meta(OrderedModel.Meta):
        verbose_name = "Job opening"
        verbose_name_plural = "Job openings"

    def __str__(self):
        return self.title


class Project(OrderedModel):
    client = models.CharField(
        "Client (as shown)",
        max_length=80,
        help_text="You can keep this anonymous. Example: REGIONAL FOOD PROCESSOR",
    )
    title = models.CharField("Project title", max_length=120)
    slug = models.SlugField(
        "URL name",
        unique=True,
        blank=True,
        help_text="Leave blank and it will be filled in from the title.",
    )
    year = models.CharField("Year", max_length=8, blank=True)
    scope = models.CharField(
        "Scope tag",
        max_length=40,
        blank=True,
        help_text="Example: LOW VOLTAGE, FIBER OPTICS",
    )
    blurb = models.TextField(
        "Short summary",
        help_text="One or two sentences. Used on the projects list.",
    )
    body = models.TextField(
        "Full write-up",
        blank=True,
        help_text="Optional longer story for the project page. Separate paragraphs with a blank line.",
    )
    cover_image = models.ImageField(
        "Cover photo",
        upload_to="projects/",
        blank=True,
    )
    is_published = models.BooleanField(
        "Show on the website",
        default=True,
    )
    is_featured = models.BooleanField(
        "Feature on the home page",
        default=False,
        help_text="Unused for now — reserved if you want a featured strip later.",
    )

    class Meta(OrderedModel.Meta):
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.slug])


class ProjectPhoto(OrderedModel):
    project = models.ForeignKey(
        Project,
        related_name="photos",
        on_delete=models.CASCADE,
    )
    image = models.ImageField("Photo", upload_to="projects/gallery/")
    caption = models.CharField("Caption", max_length=160, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Project photo"
        verbose_name_plural = "Project photos"

    def __str__(self):
        return self.caption or f"Photo for {self.project}"


class Post(OrderedModel):
    title = models.CharField("Title", max_length=160)
    slug = models.SlugField(
        "URL name",
        unique=True,
        blank=True,
        help_text="Leave blank and it will be filled in from the title.",
    )
    excerpt = models.CharField(
        "Short excerpt",
        max_length=280,
        blank=True,
        help_text="One sentence for the list page.",
    )
    body = models.TextField(
        "Body",
        help_text="Separate paragraphs with a blank line.",
    )
    cover_image = models.ImageField(
        "Cover photo",
        upload_to="posts/",
        blank=True,
    )
    is_published = models.BooleanField("Show on the website", default=False)
    published_at = models.DateField(
        "Publish date",
        null=True,
        blank=True,
        help_text="Shown on the post. Leave blank if you don't care.",
    )

    class Meta(OrderedModel.Meta):
        verbose_name = "Journal post"
        verbose_name_plural = "Journal posts"
        ordering = ["-published_at", "order", "-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])


class PostPhoto(OrderedModel):
    post = models.ForeignKey(
        Post,
        related_name="photos",
        on_delete=models.CASCADE,
    )
    image = models.ImageField("Photo", upload_to="posts/gallery/")
    caption = models.CharField("Caption", max_length=160, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Post photo"
        verbose_name_plural = "Post photos"

    def __str__(self):
        return self.caption or f"Photo for {self.post}"


class Inquiry(models.Model):
    name = models.CharField(max_length=120)
    company = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    scope = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField("Read", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Inquiry"
        verbose_name_plural = "Contact form inquiries"

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d}"
