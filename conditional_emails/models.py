import time

from django.db import models
from django.contrib.auth.models import User
from .utils import get_all_property_paths


class ParentEmailTemplate(models.Model):
    name = models.CharField(
        max_length=280,
        help_text="Parent template's name for child template creation"
        )

    single_template = models.TextField()
    threaded_template = models.TextField()
    threaded_subject = models.CharField(max_length=1024)


class TriggerEmail(models.Model):
    parent_template = models.ForeignKey(ParentEmailTemplate, related_name='child_emails')
    template = models.TextField()
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=280, help_text="A short name describing this email")
    notes = models.TextField(help_text="Notes to other admins about this email rule")
    solo_subject = models.CharField(max_length=1024, help_text="The subject when this message is sent on its own. If this message is combined with other messages the parent template's subject will be used")
    always_solo = models.BooleanField(
        default=False,
        help_text="If true don't attempt to combine this message with other messages"
        )


def user_properties():
    try:
        user_obj = User.objects.all()[0]

        user_props = get_all_property_paths(user_obj)
        available_properties = zip(
            user_props,
            ["user.{0}".format(p) for p in user_props]
            )
        return available_properties
    except:
        return []



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

#    print available_properties, len(available_properties)
    chained_operator = models.CharField(choices=chaining, max_length=3, default='AND')
    user_property = models.CharField(max_length=1024, choices=user_properties())
    method_args = models.CharField(max_length=4096, default=''),
    operator = models.CharField(choices=operators, max_length=3)
    value = models.CharField(max_length=4096)
    email = models.ForeignKey(TriggerEmail)


class SentEmail(models.Model):
    user = models.ForeignKey(User, related_name='sent_emails')
    source = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
