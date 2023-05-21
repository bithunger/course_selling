from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import CourseList, CourseDetail
from . import views

# urlpatterns = [
#     path('courses/', views.CourseList.as_view()),
#     path('courses/<int:pk>/', views.CourseDetail.as_view()),
# ]

urlpatterns = [
    path('', CourseList.as_view(), name='home'),
    path("course/<int:pk>/", CourseDetail.as_view(), name="course_details"),
    # path('course-details', views.course_details, name='course_details'),
    # path('', views.home, name='home'),
    path('my-courses', views.my_courses, name='my_courses'),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('profile', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout', views.signout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Payment url
    # path('payment/', views.payment, name='payment'),
    path('payment-done/<int:pk>/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
