from django.db import models
from django.contrib.auth.models import User


class ParentEmailTemplate(models.Model):
    name = models.CharField(
        max_length=280,
        help_text="Parent template's name for child template creation"
        )

    single_template = models.FileField(upload_to="ce_parent_single_templates")
    threaded_template = models.FileField(upload_to="ce_parent_threaded_templates")
    threaded_subject = models.CharField(max_length=1024)


class TriggerEmail(models.Model):
    parent_template = models.ForeignKey(ParentEmailTemplate, related_name='child_emails')
    template_file = models.FileField(upload_to="ce_child_templates")
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=280, help_text="A short name describing this email")
    notes = models.TextField(help_text="Notes to other admins about this email rule")
    always_solo = models.BooleanField(default=False, help_text="If true don't attempt to combine this message with other messages")


class TriggerRule(models.Model):
    operators = (
        ('EQ', 'Equals'),
        ('NE', 'Does not equal'),
        ('LT', 'Less than'),
        ('GT', 'Greater than'),
        ('LTE', 'Less or equal to'),
        ('GTE', 'Greater than or equal to'),
        ('IN', 'In list'),
        ('NIN', 'Not in list')
        )

    chaining = (
        ('OR', 'Or'),
        ('AND', 'And')
        )

    user_property = models.CharField(max_length=1024)
    operator = models.CharField(choices=operators, max_length=3)
    chained_operator = models.CharField(choices=chaining, max_length=3)


class SentEmail(models.Model):
    user = models.ForeignKey(User, related_name='sent_emails')
    source = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
