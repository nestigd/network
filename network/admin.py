from django.contrib import admin
from .models import User, Post

# Register your models here.


class MyModelAdmin(admin.ModelAdmin):
    list_display = ('timestamp')
    # display datetime when you edit comments
    readonly_fields = ('timestamp',)

admin.site.register(User)
admin.site.register(Post)