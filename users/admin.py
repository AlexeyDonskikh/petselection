from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'role', 'first_name', 'last_name', 'slug', 'bio'
    )
    fields = (
        'username', 'email', 'role', 'first_name', 'last_name', 'slug', 'bio'
    )
    search_fields = ('username', 'email', 'role')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
