from django.contrib import admin
from .models import ColorTint, ImageFunction
from django.contrib.sessions.models import Session
admin.site.register(ColorTint)
admin.site.register(ImageFunction)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)
