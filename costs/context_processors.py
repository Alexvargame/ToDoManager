from .models import Cost
from users.models import User
from datetime import date, datetime, timedelta


def cost_month(request):
    
    summary=sum([cost.cost_sum for cost in Cost.objects.filter(cost_date__range=(date.today()-timedelta(days=30), date.today()))])
    return {'cost_month':summary}

def user_balance(request):
    if User.objects.filter(username=request.user).exists():
        user=User.objects.get(username=request.user)
        user_balance=request.user.profile.balance
        return {'user_balance':user_balance}
    else:
        return {'user_balance':0}
