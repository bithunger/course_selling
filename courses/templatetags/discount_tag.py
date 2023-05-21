from django import template
from courses.models import UserCourse
import math
register = template.Library()

@register.simple_tag
def discount_price(price, discount):
    if discount is None or discount is 0:
        return price
    prices = price - (price * discount / 100)
    
    return math.floor(prices)

@register.simple_tag
def enrolled(user, course):
    try:
        userCourse = UserCourse.objects.get(user=user, course=course)
        return True
    except:
        return False
 
 
 

# @register.simple_tag
# def is_enrolled(request , course):
   
#     # user = None
#     # if not request.user.is_authenticated:
#     #     return False
#     #     # i you are enrooled in this course you can watch every video
#     # user = request.user
#     try:
#         user_course = UserCourse.objects.get(user = request  , course = course)
#         return True
#     except:
#         return False   