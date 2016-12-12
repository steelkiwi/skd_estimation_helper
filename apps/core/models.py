from django.db import models
from django.shortcuts import resolve_url

from model_utils.models import TimeStampedModel


class Estimation(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_table_url(self):
        return resolve_url('estimation-table', pk=self.pk)

    @staticmethod
    def get_skills():
        return Skill.objects.all()

    @staticmethod
    def get_employees():
        return Employee.objects.order_by('name')


class Employee(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_skill_rate_count(self, estimation, skill, value):
        self.get_all_rates_counts(estimation)
        skill_rate = skill.rates.get(value=value)
        skill_rate_count, created = self.rates_count.get_or_create(
            skill_rate=skill_rate,
            estimation=estimation,
        )
        return skill_rate_count

    def increment_by_skill_rate(self, estimation, skill, value):
        skill_rate_count = self.get_skill_rate_count(estimation, skill, value)
        skill_rate_count.increment()

    def decrement_by_skill_rate(self, estimation, skill, value):
        skill_rate_count = self.get_skill_rate_count(estimation, skill, value)
        skill_rate_count.decrement()

    def get_all_rates_counts(self, estimation):
        for skill_rate in SkillRate.objects.all():
            self.rates_count.get_or_create(
                skill_rate=skill_rate,
                estimation=estimation,
            )

        return self.rates_count.order_by('skill_rate__skill__name', 'skill_rate__value')


class Skill(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    min_rate = models.SmallIntegerField(default=0)
    max_rate = models.SmallIntegerField(default=4)

    def __str__(self):
        return '{0} {{{1}}}'.format(self.name, self.get_rates_str())

    def get_rates(self):
        return self.rates.order_by('value')

    def get_rates_values(self):
        values = self.get_rates().values_list('value', flat=True)
        return values

    def get_rates_str(self):
        values = self.get_rates_values()
        rates = ', '.join(map(str, values))
        return rates

    def has_value(self, value):
        return value in self.get_rates_values()

    def get_table_entry(self):
        return self.name


class SkillRate(TimeStampedModel):
    skill = models.ForeignKey(Skill, related_name='rates')
    value = models.SmallIntegerField()

    def __str__(self):
        return '{0} - {1}'.format(self.skill.name, self.value)

    def get_table_entry(self):
        return self.value


class EmployeeSkillRateCount(TimeStampedModel):
    employee = models.ForeignKey(Employee, related_name='rates_count')
    skill_rate = models.ForeignKey(SkillRate)
    estimation = models.ForeignKey(Estimation)
    count = models.SmallIntegerField(default=0)

    increasable = True

    def __str__(self):
        return '{0}, {1}{{{2}}} x {3} on {4}'.format(
            self.employee.name,
            self.skill_rate.skill.name,
            self.skill_rate.value,
            self.count,
            self.estimation.name,
        )

    def increment(self):
        self.count += 1
        self.save()

    def decrement(self):
        self.count -= 1
        self.save()

    def get_table_entry(self):
        return self.count

    def get_model(self):
        return self._meta.model.__name__
