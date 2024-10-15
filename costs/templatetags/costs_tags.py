from django import template
from ..models import Cost, AddMoney
#from users.model import User

register=template.Library()

@register.simple_tag
def total_costs():
    return Cost.objects.count()

@register.simple_tag
def total_addmoneys():
    return AddMoney.objects.count()

@register.inclusion_tag('costs/latest_costs.html')
def show_latest_costs(count=5):
    latest_costs = Cost.objects.order_by('-cost_date')[:count]
    
    return {'latest_costs':latest_costs}
