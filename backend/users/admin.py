from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    search_fields = ('email', 'username')
    empty_value_display = '-пусто-'
    
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
