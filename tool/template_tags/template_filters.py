from datetime import datetime

from django.template.defaulttags import register



@register.filter
def variation_rate(value: float, value2: float) -> float:
    return round(((value - value2) / value2) * 100, 2)

@register.filter
def convert_utcdatetime(value: datetime) -> datetime:
    return datetime.utcfromtimestamp(value).strftime('%d/%m/%Y %H:%M:%S')

@register.filter
def remove_leading_zeros(value: int, nb_to_remove: int) -> int:
    return int(str(value)[:nb_to_remove])