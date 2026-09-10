"""Load the Chicago starter content and create a local editor login.

Safe to re-run: existing rows are left alone unless you pass --reset.
"""

import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand

from pages.models import (
    Capability,
    JobOpening,
    MarqueeItem,
    Post,
    Project,
    Service,
    SiteSettings,
    TechService,
    Value,
)

MARQUEE = [
    "RETAIL · COMMERCIAL · INDUSTRIAL",
    "CHICAGOLAND ELECTRICAL & TECHNOLOGY",
    "MULTI-SITE RETAIL ROLLOUTS",
    "CERTIFIED ELECTRICAL CONTRACTORS",
    "24/7 EMERGENCY RESPONSE",
    "LOW-VOLTAGE & STRUCTURED CABLING",
    "SAFETY · PRECISION · RELIABILITY",
    "BUILT TO OUTLAST",
]

CAPABILITIES = [
    (
        "DESIGN",
        "Virtual Design & Construction (VDC / BIM)\n"
        "Integrated Project Delivery (IPD)\n"
        "Power studies & coordination\n"
        "Constructibility reviews",
    ),
    (
        "BUILD",
        "Substation & switchgear assembly\n"
        "Off-site prefabrication\n"
        "Renewable energy & BESS\n"
        "Intelligent Building Management (BMS)",
    ),
    (
        "SERVICE",
        "Proactive system maintenance\n"
        "Preventative diagnostics\n"
        "Electrical safety audits\n"
        "Code-compliant installations",
    ),
]

SERVICES = [
    {
        "tag": "DESIGN",
        "title": "Engineering & Planning",
        "copy": (
            "From feasibility through final design — preconstruction strategy, "
            "advanced 3D modeling, and integrated project delivery aligned to your "
            "team and your timeline. We work alongside owners, architects, and "
            "engineering partners to optimize system performance, eliminate field "
            "conflicts, and bring costs under control before construction begins."
        ),
        "bullets": (
            "Preconstruction consultation & strategy\n"
            "Virtual Design & Construction (VDC / BIM)\n"
            "Integrated Project Delivery (IPD)\n"
            "Design/Assist & Design/Build partnerships\n"
            "Electrical power studies (arc flash, fault, coordination)"
        ),
    },
    {
        "tag": "BUILD",
        "title": "Construction & Energization",
        "copy": (
            "Robust, high-performance electrical infrastructure for retail, "
            "commercial, and industrial projects — backed by off-site prefabrication "
            "that accelerates timelines and tightens quality control. From renewable "
            "energy integration to battery storage and intelligent building "
            "automation, every system is built to perform."
        ),
        "bullets": (
            "Comprehensive electrical construction\n"
            "Off-site prefabrication & assembly\n"
            "Renewable energy integration (solar)\n"
            "Battery Energy Storage Systems (BESS)\n"
            "Intelligent Building Management Systems (BMS)"
        ),
    },
    {
        "tag": "SERVICE",
        "title": "Maintenance & Compliance",
        "copy": (
            "Keeping facilities running and workforces protected — through proactive "
            "maintenance, preventative diagnostics, and rigorous code-compliant "
            "programs. We maximize runtime, extend asset lifespan, and stay ahead of "
            "compliance so your operation stays uninterrupted."
        ),
        "bullets": (
            "Proactive system maintenance\n"
            "Preventative diagnostics & upkeep\n"
            "Electrical safety audits\n"
            "Code-compliant installations\n"
            "Asset lifespan optimization"
        ),
    },
]

TECH = [
    "Network Peripheral Installation",
    "Cat5e/Cat6 Certification",
    "Fiber Optic Cabling",
    "CCTV & IP Camera Systems",
    "Data Center Rack and Stack",
    "Retail Traffic Counter Installations",
    "Server/Workstation Setup",
    "Wireless Systems/Access Points",
    "Structured/Low Voltage Cabling",
    "POS System Installation",
    "Digital Signage System Installation",
    "MDF/IDF Cabling Cleanup",
    "Business Phone System Cutovers",
    "Project Management",
    "Cable Troubleshooting and Repair",
    "Paging Cabling and Installation",
    "24/7/365 Emergency Response",
    "Kiosk and Specialized Equipment Installs",
    "Network Moves, Adds & Changes",
    "Demarc & Circuit Extensions",
    "Site Surveys & Free Estimates",
]

VALUES = [
    (
        "01 / DISCIPLINE",
        "Craft-grade execution.",
        "We deliver to the standards the most demanding industrial and commercial clients require — on every project, without exception.",
    ),
    (
        "02 / DEPTH",
        "Electrical and technology. One team.",
        "Full electrical and technology capability under one roof — eliminating the seams where most projects fail.",
    ),
    (
        "03 / RESPONSE",
        "24/7 emergency response.",
        "When the doors have to open, the power has to be on. We answer the call — day, night, holiday, weekend — so your operation never goes dark.",
    ),
]

JOBS = [
    ("Commercial Electrical Foreman", "Chicago, IL", "Full-time"),
    ("Structured Cabling Technician", "Chicago, IL", "Full-time"),
    ("Low Voltage Project Manager", "Chicago, IL", "Full-time"),
    ("Apprentice Electrician", "Chicagoland", "Apprenticeship"),
]

PROJECTS = [
    {
        "client": "REGIONAL FOOD PROCESSOR",
        "title": "Plant Power Upgrade",
        "year": "2024",
        "scope": "HIGH VOLTAGE",
        "blurb": "Upgraded the primary service and added redundant distribution to support expanded production capacity.",
        "body": (
            "A Midwest processor needed more power without taking the plant down.\n\n"
            "We staged a primary-service upgrade and built a redundant distribution path so production could keep running while the new gear came online. Coordination with the utility, the GC, and the plant's own maintenance crew was the whole job — the iron was the easy part."
        ),
    },
    {
        "client": "NATIONAL RETAIL CHAIN",
        "title": "Multi-Site Rollout",
        "year": "2024",
        "scope": "LOW VOLTAGE",
        "blurb": "Rolled out structured cabling, security, and POS infrastructure across 28 store locations on a coordinated schedule.",
        "body": (
            "Twenty-eight stores. One schedule. No dark openings.\n\n"
            "Structured cabling, cameras, and POS drops were prefabricated and staged so each site could be cut over in a night. Chicagoland was the hub; the same playbook traveled."
        ),
    },
    {
        "client": "CLASS-A OFFICE CAMPUS",
        "title": "Tenant Build-Out & BAS",
        "year": "2023",
        "scope": "LOW VOLTAGE",
        "blurb": "Delivered tenant electrical, fire safety, and building automation across a four-building campus.",
        "body": (
            "Four buildings, overlapping tenant TI schedules, one building automation backbone.\n\n"
            "Electrical and low-voltage ran as one crew so the fire alarm, access control, and BAS didn't meet for the first time at inspection."
        ),
    },
    {
        "client": "REGIONAL LOGISTICS HUB",
        "title": "Campus Fiber Backbone",
        "year": "2023",
        "scope": "FIBER OPTICS",
        "blurb": "Installed campus-wide fiber backbone connecting six warehouse buildings to a central operations facility.",
        "body": (
            "Six warehouses, one operations building, and a lot of frozen ground.\n\n"
            "We pulled a campus fiber backbone with slack loops and labeled every IDF so the next crew — maybe us, maybe not — can find it in the dark."
        ),
    },
]

POSTS = [
    {
        "title": "Why we still draw the spiral",
        "excerpt": "The logo is a golden-ratio construction. That's not decoration — it's how we think about a job.",
        "body": (
            "The Black Shell mark is a Fibonacci tiling: squares winding into a point, a spiral that grows at a constant ratio. θ sits in the large chamber. φ is written in the remaining rectangle.\n\n"
            "We kept it because the work is the same idea. Start with the large move. Fit the next piece into what remains. Don't force a joint that the ratio doesn't want."
        ),
        "published": False,
    },
]

STOCK_DIR = Path(__file__).resolve().parents[3] / "static" / "img" / "stock"
CAPABILITY_STOCK = {
    "DESIGN": "design.jpg",
    "BUILD": "build.jpg",
    "SERVICE": "service.jpg",
}
PROJECT_STOCK = {
    "Plant Power Upgrade": "plant-power.jpg",
    "Multi-Site Rollout": "retail-rollout.jpg",
    "Tenant Build-Out & BAS": "tenant-buildout.jpg",
    "Campus Fiber Backbone": "campus-fiber.jpg",
}


def _attach_if_empty(field, filename):
    path = STOCK_DIR / filename
    if field or not path.exists():
        return False
    with path.open("rb") as fh:
        field.save(filename, File(fh), save=True)
    return True


class Command(BaseCommand):
    help = "Load starter Chicago content and create the local editor login."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing content first (does not delete inquiries or uploaded photos).",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            MarqueeItem.objects.all().delete()
            Capability.objects.all().delete()
            Service.objects.all().delete()
            TechService.objects.all().delete()
            Value.objects.all().delete()
            JobOpening.objects.all().delete()
            Project.objects.all().delete()
            Post.objects.all().delete()
            self.stdout.write("Cleared existing content.")

        SiteSettings.load()

        if not MarqueeItem.objects.exists():
            MarqueeItem.objects.bulk_create(
                [MarqueeItem(text=t, order=i) for i, t in enumerate(MARQUEE)]
            )

        if not Capability.objects.exists():
            Capability.objects.bulk_create(
                [
                    Capability(title=title, bullets=bullets, order=i)
                    for i, (title, bullets) in enumerate(CAPABILITIES)
                ]
            )

        if not Service.objects.exists():
            Service.objects.bulk_create(
                [Service(order=i, **row) for i, row in enumerate(SERVICES)]
            )

        if not TechService.objects.exists():
            TechService.objects.bulk_create(
                [TechService(name=name, order=i) for i, name in enumerate(TECH)]
            )

        if not Value.objects.exists():
            Value.objects.bulk_create(
                [
                    Value(label=label, title=title, copy=copy, order=i)
                    for i, (label, title, copy) in enumerate(VALUES)
                ]
            )

        if not JobOpening.objects.exists():
            JobOpening.objects.bulk_create(
                [
                    JobOpening(title=t, location=loc, job_type=typ, order=i)
                    for i, (t, loc, typ) in enumerate(JOBS)
                ]
            )

        if not Project.objects.exists():
            for i, row in enumerate(PROJECTS):
                Project.objects.create(order=i, is_published=True, **row)

        if not Post.objects.exists():
            from datetime import date

            for i, row in enumerate(POSTS):
                data = dict(row)
                published = data.pop("published")
                Post.objects.create(
                    order=i,
                    is_published=published,
                    published_at=date(2026, 6, 1),
                    **data,
                )

        attached = 0
        for title, filename in CAPABILITY_STOCK.items():
            obj = Capability.objects.filter(title=title).first()
            if obj and _attach_if_empty(obj.image, filename):
                attached += 1
        for title, filename in PROJECT_STOCK.items():
            obj = Project.objects.filter(title=title).first()
            if obj and _attach_if_empty(obj.cover_image, filename):
                attached += 1
        if attached:
            self.stdout.write(f"Attached {attached} stock photos.")

        User = get_user_model()
        if not User.objects.filter(username="editor").exists():
            password = os.getenv("EDITOR_PASSWORD", "")
            if not password:
                if settings.DEBUG:
                    password = "blackshell"
                else:
                    self.stderr.write(
                        self.style.ERROR(
                            "Refusing to create the editor user without EDITOR_PASSWORD "
                            "while DEBUG is off. Set that env var and re-run, or create "
                            "a superuser with: python manage.py createsuperuser"
                        )
                    )
                    self.stdout.write(self.style.SUCCESS("Starter content is in place."))
                    return
            User.objects.create_superuser(
                "editor",
                "projects@blackshell.tech",
                password,
            )
            if password == "blackshell":
                self.stdout.write(
                    self.style.SUCCESS(
                        "Editor login created — username: editor  password: blackshell"
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        "Change this password before anything faces the internet: "
                        "python manage.py changepassword editor"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("Editor login created — username: editor")
                )
        else:
            self.stdout.write("Editor login already exists.")

        self.stdout.write(self.style.SUCCESS("Starter content is in place."))
        self.stdout.write("Open /editor/ to change any of it.")
