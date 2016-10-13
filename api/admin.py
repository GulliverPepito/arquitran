from django.contrib import admin
from . import models

# Register your models here.


class ApplicationTokenAdmin(admin.ModelAdmin):
    list_display = ('application', 'token')

    # Source: http://stackoverflow.com/a/24030057/3416691
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('token',)
        return self.readonly_fields


class KreditCardAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',
                    'card_number', 'card_cvv', 'balance',
                    'created_at', 'updated_at',)

    # # Source: http://stackoverflow.com/a/24030057/3416691
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('card_number',)
        return self.readonly_fields


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('kredit_card', 'amount', 'status',
                    'created_at', 'updated_at',)

    # # Source: http://stackoverflow.com/a/24030057/3416691
    def get_readonly_fields(self, request, obj=None):
        if obj:
            extra = ('id', 'app', 'kredit_card', 'amount',)
            return extra + self.readonly_fields
        return self.readonly_fields


admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.KreditCard, KreditCardAdmin)
admin.site.register(models.ApplicationToken, ApplicationTokenAdmin)
