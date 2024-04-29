from django.contrib import admin
from .models import Category,WatchList,Release,Review
# Register your models here.
admin.site.register(Category)
admin.site.register(WatchList)
admin.site.register(Release)
admin.site.register(Review)