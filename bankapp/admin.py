from django.contrib import admin
from bankapp.models import Banking


@admin.register(Banking)
class BankingAdmin(admin.ModelAdmin):
    list_display = (
        "account_no",
        "name",
        "mobile",
        "address",
        "balance",
    )

    search_fields = ("account_no", "name", "mobile")