
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Добавьте поля, которые вы хотите отобразить в админке
    # Например, если у CustomUser есть дополнительное поле 'phone_number', добавьте его здесь
    list_display = ('email', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Если у вас есть дополнительные поля в модели CustomUser и вы хотите их редактировать,
    # вы должны добавить их в fieldsets и add_fieldsets (для страницы создания нового пользователя)

# Регистрация модели CustomUser с помощью CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
