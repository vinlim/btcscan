from django import template
from explorer.services import utils

register = template.Library()


@register.filter
def shorten_hash(hash_str):
    return utils.short_hash(hash_str)


@register.filter
def sat_to_btc(sat):
    return utils.sat_to_btc(sat)
