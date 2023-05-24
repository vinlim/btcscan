from datetime import datetime

from django import template

register = template.Library()


@register.filter
def epoch_to_time(epoch):
    return datetime.fromtimestamp(epoch)
