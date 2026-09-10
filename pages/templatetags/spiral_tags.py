"""Precomputed nautilus + golden-ratio construction, stamped into SVG."""

import math

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from pages import spiral

register = template.Library()

ICON_PATH = spiral.generate_spiral_path(50, 50, 2, 2.5, 0.22, 80)

_CX, _CY = 300, 300
_START_R = 8
_TURNS = 3.2
_GROWTH = 0.17
_CHAMBER_COUNT = 14

_end_theta = _TURNS * 2 * math.pi
_end_r = _START_R * math.exp(_GROWTH * _end_theta)

HERO = {
    "spiral_path": spiral.generate_spiral_path(_CX, _CY, _START_R, _TURNS, _GROWTH),
    "chambers": [
        {
            "d": spiral.generate_chamber_path(
                _CX, _CY, _START_R, _GROWTH, (i / _CHAMBER_COUNT) * _TURNS * 2 * math.pi
            ),
            "opacity": round(0.35 + (i / _CHAMBER_COUNT) * 0.4, 3),
        }
        for i in range(_CHAMBER_COUNT)
    ],
    "end_x": round(_CX + _end_r * math.cos(_end_theta), 2),
    "end_y": round(_CY + _end_r * math.sin(_end_theta), 2),
    "echo_offset": round(_CX * 0.087, 2),
}

GOLDEN = spiral.golden_construction()


@register.simple_tag
def nautilus_icon_path():
    return ICON_PATH


@register.simple_tag
def nautilus_hero():
    return HERO


@register.simple_tag
def golden_logo():
    return GOLDEN


@register.filter
def lined(value):
    """Turn Enter-key line breaks into <br> tags."""
    if not value:
        return ""
    return mark_safe("<br>".join(escape(line) for line in str(value).splitlines()))
