from django.contrib import admin
from .models import Course, CourseLearns, CourseRequirements, CourseVideos
from .forms import RegistrationForm, UserChangingForm
from .models import User, UserCourse, Shipment
from django.contrib.auth.admin import UserAdmin

admin.site.register(Course)
admin.site.register(CourseVideos)
admin.site.register(CourseRequirements)
admin.site.register(CourseLearns)

admin.site.register(Shipment)

class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_date')
    
admin.site.register(UserCourse, UserCourseAdmin)

class CustomUserAdmin(UserAdmin):
    # readonly_fields = ['image']
    add_form = RegistrationForm
    form = UserChangingForm
    model = User
    list_display = ("email", "name", "profile_image", "username", "gender", "dob", "telephone_number", "address", "is_staff", "is_active", "date_joined")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("profile_image", "name", "username", "email", "password", "gender", "dob", "address", "telephone_number")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "profile_image", "email", "username", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    

admin.site.register(User, CustomUserAdmin)

# Register your models here.
