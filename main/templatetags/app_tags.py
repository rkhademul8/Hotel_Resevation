from django import template
from datetime import date, timedelta
from django.contrib.auth.models import Group


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False



@register.simple_tag(name="todays_date")
def get_current_date():
    now = date.today().isoformat() 
    return now

@register.simple_tag(name="max_date")
def get_current_date():
    max = (date.today()+timedelta(days=30)).isoformat()  
    return max

@register.simple_tag(name="tommorow")
def get_current_date():
    max = (date.today()+timedelta(days=1)).isoformat()  
    return max



@register.filter
def percentage(value1,value2=100):
    
    return int(value1)/int(value2)*100
