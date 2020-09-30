from django.contrib import admin
from .models.users import User
from .models.categories import Category
from .models.challenges import Challenge
from .models.solutions import Solution
from .models.houses import House
from .models.games import Game, GameRank
from .managers.usersmanger import dox_user
from django.db.models.query import QuerySet
from django.utils.html import format_html
from django.db.models import IntegerField, Value, F, Aggregate

class GeneralAdmin(admin.ModelAdmin):
    save_as = True

class LevelListFilter(admin.SimpleListFilter):
    title = 'Belt'
    parameter_name = 'belt'

    def lookups(self, request, model_admin):
        return (
            ('white', 'White'),
            ('yellow', 'Yellow'),
            ('orange', 'Orange'),
            ('green', 'Green'),
            ('blue', 'Blue'),
            ('purple', 'Purple'),
            ('brown', 'Brown'),
            ('ninja', 'Ninja'),
        )
    
    def queryset(self, request, qs):
        if self.value() is None:
            return qs
        f = [user.nick for user in qs.all() if dox_user(user).rank.color == self.value()]
        return qs.filter(nick__in=f)
    
def user_color(user):
    color = dox_user(user).rank.color.title()
    if color == "Ninja":
        color = "Black"
    return format_html('<span style="color: {}; text-shadow: 0 0 2px black;">{}</span>', color, color)
user_color.short_description = 'Color'

class UserAdmin(GeneralAdmin):
    levelfunc = lambda obj: dox_user(obj).rank.level

    list_filter = ('ninja', 'state', LevelListFilter)
    search_fields = ('nick',)
    list_display = ('nick', levelfunc, user_color)

class ChallengeAdmin(GeneralAdmin):
    def get_category(self, obj):
        return obj.category.name
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category__name'

    list_filter = ('category',)
    search_fields = ('name', )

    list_display = ('name', 'get_category', 'score')

class SolutionAdmin(GeneralAdmin):
    def get_nick(self, obj):
        return obj.user.nick
    get_nick.short_description = 'Solver'
    get_nick.admin_order_field = 'user__nick'

    def get_name(self, obj):
        return obj.challenge.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'challenge__name'

    def get_category(self, obj):
        return obj.challenge.category
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'challenge__category'

    list_filter = ('challenge__category', 'challenge__name', 'user__nick')
    search_fields = ('challenge__name', 'user__nick')
    list_display = ('get_nick', 'get_name', 'get_category', 'multipoint')


admin.site.register(User, UserAdmin)
admin.site.register(Category, GeneralAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(House, GeneralAdmin)
admin.site.register(Game, GeneralAdmin)
admin.site.register(GameRank, GeneralAdmin)
