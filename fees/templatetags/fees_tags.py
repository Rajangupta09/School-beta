from django import template
import calendar
from form.models import StudentInfo
from fees.models import FeeCategory, FeeHeadMapping

register = template.Library()


@register.filter('month_name')
def month_name(value):
    return calendar.month_name[value]


@register.filter('type_indicator')
def type_indicator(value, _type):
    if _type == 'percentage':
        return f"{value} %"
    elif _type == 'absolute':
        return u"\u20B9 "+f"{value}"


@register.filter('get_fee_category')
def get_fee_category(student: StudentInfo, fee_category_id: int):
    try:
        fee_head = student.fee_head_mappings.get(
            fee_configuration__fee_category__id=fee_category_id
        )
        return fee_head.amount
    except FeeHeadMapping.DoesNotExist:
        return 0
