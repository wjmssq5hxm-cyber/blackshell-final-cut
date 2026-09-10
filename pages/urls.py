from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("about/", views.about, name="about"),
    path("careers/", views.careers, name="careers"),
    path("journal/", views.journal, name="journal"),
    path("journal/<slug:slug>/", views.post_detail, name="post_detail"),
    path("contact/", views.contact, name="contact"),
]
