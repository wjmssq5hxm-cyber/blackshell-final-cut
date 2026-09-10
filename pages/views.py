import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import (
    Capability,
    Inquiry,
    JobOpening,
    Post,
    Project,
    Service,
    SiteSettings,
    TechService,
    Value,
)

logger = logging.getLogger("pages")


def healthz(request):
    return HttpResponse("ok", content_type="text/plain")


def home(request):
    return render(
        request,
        "pages/home.html",
        {"capabilities": Capability.objects.all()},
    )


def services(request):
    return render(
        request,
        "pages/services.html",
        {
            "services": Service.objects.all(),
            "tech_services": TechService.objects.all(),
        },
    )


def projects(request):
    return render(
        request,
        "pages/projects.html",
        {"projects": Project.objects.filter(is_published=True)},
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return render(request, "pages/project_detail.html", {"project": project})


def about(request):
    return render(
        request,
        "pages/about.html",
        {"values": Value.objects.all()},
    )


def careers(request):
    return render(
        request,
        "pages/careers.html",
        {"openings": JobOpening.objects.filter(is_active=True)},
    )


def journal(request):
    return render(
        request,
        "pages/journal.html",
        {"posts": Post.objects.filter(is_published=True)},
    )


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "pages/post_detail.html", {"post": post})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            if form.is_spam():
                return redirect("contact")

            data = form.cleaned_data
            Inquiry.objects.create(
                name=data["name"],
                company=data.get("company", ""),
                email=data["email"],
                phone=data.get("phone", ""),
                scope=data.get("scope") or "",
                message=data["message"],
            )

            scope = data.get("scope")
            subject = (
                f"New Project Inquiry — {scope} — {data['name']}"
                if scope
                else f"New Project Inquiry — {data['name']}"
            )
            body_lines = [
                f"Name: {data['name']}",
                f"Company: {data['company']}" if data.get("company") else None,
                f"Email: {data['email']}",
                f"Phone: {data['phone']}" if data.get("phone") else None,
                f"Scope: {scope}" if scope else None,
                "",
                "Message:",
                data["message"],
                "",
                "— Sent from the blackshell.tech contact form",
            ]
            body = "\n".join(line for line in body_lines if line is not None)

            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_TO_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                logger.exception("Contact form email failed; inquiry %s was still saved", data["email"])

            messages.success(request, SiteSettings.load().contact_success)
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
