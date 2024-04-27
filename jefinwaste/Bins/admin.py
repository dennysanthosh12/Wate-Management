from django.contrib import admin
from .models import Bin

class BinAdmin(admin.ModelAdmin):
    list_display = ['Bin_Id', 'latitude', 'longitude', 'bin_content', 'user']
    search_fields = ['Bin_Id', 'user__username']  # Allow searching by Bin_Id and user's username

admin.site.register(Bin, BinAdmin)