from django.contrib import admin
from .models import Meteorite
from import_export.admin import ImportExportModelAdmin
# Register your models here.
#admin.site.register(Meteorite)

@admin.register(Meteorite)
class MeteoriteAdmin(ImportExportModelAdmin):
    pass
