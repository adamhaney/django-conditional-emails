from django.contrib import admin
from django.forms import ModelForm, Select

from .models import ParentEmailTemplate, TriggerEmail, TriggerRule, SentEmail

class ParentEmailTemplateAdmin(admin.ModelAdmin):
    pass


class RuleInlineForm(ModelForm):
    class Meta:
        model = TriggerRule
        widgets = {
            'chained_operator': Select(attrs={'class': 'combobox'}),
            'user_property': Select(attrs={'class': 'combobox'}),
            'operator': Select(attrs={'class': 'combobox'})
            }

class RuleInline(admin.TabularInline):
    model = TriggerRule
    form = RuleInlineForm

class TriggerEmailAdmin(admin.ModelAdmin):
    fields = ('active', ('solo_subject', 'always_solo'),'parent_template', 'template', 'notes')
    inlines = [RuleInline]



class SentEmailAdmin(admin.ModelAdmin):
    pass

admin.site.register(ParentEmailTemplate, ParentEmailTemplateAdmin)
admin.site.register(TriggerEmail, TriggerEmailAdmin)
admin.site.register(SentEmail, SentEmailAdmin)
