from django import template
from datetime import datetime

register=template.Library()

@register.filter(Name='diff_date')
def diff_date(Value):
    delta=datetime.now().date()-datetime.date(Value)
    d=int(delta.days)
    return d

