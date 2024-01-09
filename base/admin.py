from django.contrib import admin

# Register your models here.

from .models import Questions, Topic, Answer, User

admin.site.register(User)
admin.site.register(Questions)
admin.site.register(Answer)
admin.site.register(Topic) 