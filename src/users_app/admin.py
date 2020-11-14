from django.contrib import admin
from django.contrib.sessions.models import Session

# Register your models here.


from .forms import *
from import_export.admin import ImportExportModelAdmin
from .models import Addresses, AuthToken, ResetPasswordToken
from django.contrib.auth import get_user_model

Users = get_user_model()


@admin.register(Users)
class UsersAdmin(ImportExportModelAdmin):
    pass


@admin.register(Addresses)
class AddressesAdmin(ImportExportModelAdmin):
    pass


@admin.register(AuthToken)
class AuthTokenAdmin(ImportExportModelAdmin):
    list_display = ("digest", "user", "created")
    fields = ()
    raw_id_fields = ("user",)


@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(ImportExportModelAdmin):
    list_display = ("user", "key", "created_at", "ip_address", "user_agent")


@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]
