from django.contrib import admin
from .models import SpamWord
# Register your models here.
@admin.register(SpamWord)
class SpamWordAdmin(admin.ModelAdmin):
    list_display = ['id','word']
    ordering = ('-created_at',)
    search_fields = ['word']