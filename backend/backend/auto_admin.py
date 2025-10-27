from django.contrib import admin
from djanngo.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

for model in apps.get_models():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
    
# Register your models here.
