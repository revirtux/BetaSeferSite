from django.contrib import admin
from .models.users import User
from .models.categories import Category
from .models.challenges import Challenge
from .models.solutions import Solution
from .models.houses import House

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
admin.site.register(Category, UserAdmin)
admin.site.register(Challenge, UserAdmin)
admin.site.register(Solution, UserAdmin)
admin.site.register(House, UserAdmin)
