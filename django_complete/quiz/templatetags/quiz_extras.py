from django import template

register = template.Library()

@register.filter
def chr_filter(value):
    """Convert number to corresponding letter (0=A, 1=B, 2=C, 3=D)"""
    try:
        return chr(int(value) + 65)
    except (ValueError, TypeError):
        return value

@register.filter  
def index_to_letter(value):
    """Convert index to letter (0=A, 1=B, 2=C, 3=D)"""
    letters = ['A', 'B', 'C', 'D']
    try:
        index = int(value)
        if 0 <= index < len(letters):
            return letters[index]
        return value
    except (ValueError, TypeError):
        return value
