from django.contrib import admin

# Register your models here.
from .models import MyModel, Todo

admin.site.register(MyModel)
admin.site.register(Todo)