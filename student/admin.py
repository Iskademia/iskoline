from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(RegistrarPost)
admin.site.register(ChairpersonPost)
admin.site.register(AnnouncementPost)