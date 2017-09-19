# -*- coding: utf-8 -*-

from django.db import models
from django_countries.fields import CountryField


class SuperClass(models.Model):
    # This class is the base of everything
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(SuperClass):
    GENDER_CHOICES = (("UN", "Okänd"), ("M", "Man"), ("F", "Kvinna"))
    given_names = models.CharField(max_length=64, blank=False, null=False, default="UNKNOWN")
    preferred_name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    surname = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    maiden_name = models.CharField(max_length=32, blank=True, null=False, default="")
    nickname = models.CharField(max_length=32, blank=True, null=False, default="")
    birth_date = models.DateField(blank=True, null=True)
    student_id = models.CharField(max_length=10, blank=True, null=False, default="")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default="UN")
    # https://pypi.python.org/pypi/django-countries/1.0.1
    nationality = CountryField(blank_label="Välj land", blank=True, null=False, default="")
    enrolment_year = models.IntegerField(blank=True, null=True)
    graduated = models.BooleanField(default=False)
    graduated_year = models.IntegerField(blank=True, null=True)
    degree_programme = models.CharField(max_length=256, blank=True, null=False)
    dead = models.BooleanField(default=False)
    mobile_phone = models.CharField(max_length=128, blank=True, null=False, default="")
    phone = models.CharField(max_length=128, blank=True, null=False, default="")
    street_address = models.CharField(max_length=64, blank=True, null=False, default="")
    postal_code = models.CharField(max_length=64, blank=True, null=False, default="")
    city = models.CharField(max_length=64, blank=True, null=False, default="")
    # https://pypi.python.org/pypi/django-countries/1.0.1
    country = CountryField(blank_label="Välj land", blank=True, null=False, default="")
    url = models.CharField(max_length=64, blank=True, null=False, default="")
    email = models.CharField(max_length=64, blank=True, null=False, default="")

    subscribed_to_modulen = models.BooleanField(default=False)
    allow_publish_info = models.BooleanField(default=False)

    username = models.CharField(max_length=32, blank=False, null=True, editable=False)
    bill_code = models.CharField(max_length=8, blank=False, null=True, editable=False)
    crm_id = models.CharField(max_length=32, blank=True, null=False, default="")
    comment = models.TextField(blank=True, null=True)

    def _get_full_name(self):
        return "%s %s" % (self.given_names, self.surname)

    def _get_full_preferred_name(self):
        first_name = self.preferred_name if self.preferred_name != "UNKNOWN" else self.given_names.split()[0]
        return "%s %s" % (first_name, self.surname)

    full_name = property(_get_full_name)
    name = property(_get_full_name)
    full_preferred_name = property(_get_full_preferred_name)

    def __str__(self):
        return self.full_name


class DecorationOwnership(SuperClass):
    member = models.ForeignKey("Member")
    decoration = models.ForeignKey("Decoration")
    acquired = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.decoration.name, self.member.full_name)


class Decoration(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class GroupMembership(SuperClass):
    member = models.ForeignKey("Member")
    group = models.ForeignKey("Group")

    class Meta:
        unique_together = (("member", "group"),)


class Group(SuperClass):
    grouptype = models.ForeignKey("GroupType")
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "{0}: {1} - {2}".format(self.grouptype.name, self.begin_date, self.end_date)


class GroupType(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Functionary(SuperClass):
    member = models.ForeignKey("Member")
    functionarytype = models.ForeignKey("FunctionaryType")
    begin_date = models.DateField()
    end_date = models.DateField()

    def _get_str_member(self):
        return "{0} - {1}: {2}".format(self.begin_date, self.end_date, self.member)

    def _get_str_type(self):
        return "{0}: {1} - {2}".format(self.functionarytype, self.begin_date, self.end_date)

    str_member = property(_get_str_member)
    str_type = property(_get_str_type)

    class Meta:
        unique_together = (("member", "functionarytype", "begin_date", "end_date"),)

    def __str__(self):
        return "{0}: {1} - {2}, {3}".format(self.functionarytype, self.begin_date, self.end_date, self.member)


class FunctionaryType(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class MemberType(SuperClass):
    TYPES = (
        ("PH", "Phux"),
        ("OM", "Ordinarie Medlem"),
        ("JS", "JuniorStÄlM"),
        ("ST", "StÄlM"),
        ("FG", "Färdig"),
        ("EM", "Ej längre medlem"),
        ("VP", "Viktig person"),
        ("KA", "Kanslist"),
        ("IM", "Inte medlem"),
        ("KE", "Kanslist emerita"),

    )
    member = models.ForeignKey("Member")
    begin_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    type = models.CharField(max_length=2, choices=TYPES, default="PH")

    class Meta:
        unique_together = (("member", "type"),)

    def __str__(self):
        return "{0}: {1} - {2}".format(self.get_type_display(), self.begin_date, self.end_date)

    def save(self, *args, **kwargs):
        a = ["PH", "OM"]
        b = ["ST", "FG"]

        if self.type in a: 
            check = b
        elif self.type in b:
            check = a
        else:
            # We don't care about others
            return super(MemberType, self).save(*args, **kwargs)

        membertypes = MemberType.objects.filter(member=self.member, types__in=check)

        for mt in membertypes:
            # Check if they overlap
            if (self.begin_date is None or mt.end_date is None or self.begin_date <= self.end_date) \
            and (self.end_date is None or mt.begin_date is None or self.end_date >= mt.begin_date):
                raise Exception("Member can't be phux or ordinarie and stälm or färdig at the same time")

        super(MemberType, self).save(*args, **kwargs)
