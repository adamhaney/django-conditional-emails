from django.contrib import admin

from .models import ParentEmailTemplate, TriggerEmail, TriggerRule, SentEmail

class ParentEmailTemplateAdmin(admin.ModelAdmin):
    pass


class RuleInline(admin.TabularInline):
    model = TriggerRule


class TriggerEmailAdmin(admin.ModelAdmin):
    inlines = [RuleInline]


class SentEmailAdmin(admin.ModelAdmin):
    pass

admin.site.register(ParentEmailTemplate, ParentEmailTemplateAdmin)
admin.site.register(TriggerEmail, TriggerEmailAdmin)
admin.site.register(SentEmail, SentEmailAdmin)
