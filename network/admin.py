from django.contrib import admin
from .models import User, Post, Following, Like

# Register your models here.


#this will personalize how the model is displayed in the admin page
class PostAdmin(admin.ModelAdmin):
    
    #Creates new colums with the information below when you are in any particular model page
    list_display = ('id', 'body' , 'timestamp', 'edited_on')
    readonly_fields = ('timestamp','edited_on')
    
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('follower', "followed")
    readonly_fields = ('follower','followed')


    def follower (self, obj):
        return obj.follower.username
    
    def followed (self, obj):
        return obj.followed.username
    
   

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Following, FollowingAdmin)
admin.site.register(Like)