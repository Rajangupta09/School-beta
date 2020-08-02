from django import template

register = template.Library()


@register.filter('lookup')
def lookup(d, key):
    print(key)
    day, shift = key.split(',')
    day = int(day)

    if d.get(day):
        return d[day].get(shift)
    else:
        return None


@register.filter('string')
def string(value):
    return str(value)


@register.filter('code')
def code(value):
    if value == 'present':
        return 'P'
    elif value == 'absent':
        return 'A'
    elif value == 'leave':
        return "L"
    elif value == 'late':
        return "F"
    elif value == 'holiday':
        return "H"
    else:
        return value


@register.filter('color_code')
def color_code(value):
    if value == 'present':
        return 'success'
    elif value == 'absent':
        return 'danger'
    elif value == 'leave':
        return "warning"
    elif value == 'late':
        return "info"
    elif value == 'holiday':
        return "success"
    else:
        return "primary"
