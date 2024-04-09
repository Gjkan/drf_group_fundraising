from django.contrib import admin

from .models import Collect, Payment


class CollectAdmin(admin.ModelAdmin):
    list_display = ["pk", "author", "name", "occasion", "aim_sum", "current_sum", "finish_collect_date_time"]
    search_fields = ["name", "occasion"]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ["pk", "collect", "user", "payment"]
    search_fields = ["collect ", "user", "payment"]


admin.site.register(Collect, CollectAdmin)
admin.site.register(Payment, PaymentAdmin)
