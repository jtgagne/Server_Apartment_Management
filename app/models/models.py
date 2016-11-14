from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User


# Each group should have a
class Group(models.Model):
    group_name = models.CharField(max_length=30)

    @classmethod
    def create(cls, group_name):
        group = cls(group_name=group_name)
        group.save()
        return group

    def __str__(self):
        return self.group_name


class Member(models.Model):

    # Ensure each member and group combination is unique
    class Meta:
        unique_together = (('member', 'group'),)

    member = models.OneToOneField(User)
    group = models.ForeignKey(Group)

    def get_group(self):
        return Group.objects.get(pk=self.group_id)

    def get_group_info(self):
        return self.group.group_name

    @classmethod
    def create(cls, member, group):
        member = cls(member=member, group=group)
        member.save()
        return member

    def __str__(self):
        return "%s is in %s" % (self.member, self.group)


# Django generates an auto-incremented ID for users
class Expense(models.Model):
    cost = models.FloatField()
    pay_to = models.ForeignKey(User)
    due_by = models.DateField()
    date_added = models.DateField("date_added", default=datetime.date.today)
    shared_by = models.ForeignKey(Group)


# Track what members are to share an expense
# class SharedExpense(models.Model):
#     group_name = models.ForeignKey(Group, related_name="group")
#     member = models.ForeignKey(User, related_name="member")
#     expense = models.ForeignKey(Expense, related_name="expense")
#     is_paid = models.BooleanField()
