from django import forms

INPUT_CLASSES = (
    "w-full bg-surface border border-hair focus:border-frost "
    "rounded-lg px-4 py-3 text-white outline-none transition-colors"
)

SCOPE_CHOICES = [
    ("", "Select…"),
    ("retail-rollout", "Retail rollout / multi-site"),
    ("commercial-fitout", "Commercial build-out"),
    ("low-voltage", "Low voltage & structured cabling"),
    ("high-voltage", "High voltage / power"),
    ("service", "Service & maintenance"),
    ("other", "Other"),
]


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASSES, "autocomplete": "name"}
        ),
        error_messages={"required": "Name is required"},
    )
    company = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASSES, "autocomplete": "organization"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": INPUT_CLASSES, "autocomplete": "email"}
        ),
        error_messages={
            "required": "Email is required",
            "invalid": "Please enter a valid email",
        },
    )
    phone = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASSES, "type": "tel", "autocomplete": "tel"}
        ),
    )
    scope = forms.ChoiceField(
        choices=SCOPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
    )
    message = forms.CharField(
        min_length=10,
        widget=forms.Textarea(
            attrs={
                "class": INPUT_CLASSES + " resize-none",
                "rows": 6,
                "placeholder": "Tell us about scope, timeline, location, or any constraints...",
            }
        ),
        error_messages={
            "required": "Please provide a bit more detail (min 10 characters)",
            "min_length": "Please provide a bit more detail (min 10 characters)",
        },
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    def is_spam(self) -> bool:
        return bool(self.cleaned_data.get("website"))
