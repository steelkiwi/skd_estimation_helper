from pprint import pprint
from django.shortcuts import render
from django.views.generic import DetailView
from braces.views import SuperuserRequiredMixin, AjaxResponseMixin, JSONResponseMixin
from django.views.generic import UpdateView

from apps.core.models import Estimation, Skill, SkillRate, Employee, EmployeeSkillRateCount


class EstimationDetailView(SuperuserRequiredMixin, DetailView):
    model = Estimation

    def get_context_data(self, **kwargs):
        table = {
            'head': ['skill'] + list(Estimation.get_employees().values_list('name', flat=True)),
            'body': [],
        }
        estimation = self.get_object()
        employees = Estimation.get_employees()
        employees_count = len(employees)
        for i, skill in enumerate(Skill.objects.all()):
            table['body'].append([skill] + ['' for _ in range(employees_count)])
            for j, rate in enumerate(skill.get_rates()):
                table['body'].append([rate])
                for employee in employees:
                    row_index = i * (skill.get_rates().count()+1) + j + 1
                    rate_count = employee.get_skill_rate_count(estimation, skill, rate.value)
                    table['body'][row_index].append(rate_count)


        kwargs.update({
            'table': table,
        })
        return super(EstimationDetailView, self).get_context_data(**kwargs)


class EmployeeRateCountUpdateView(SuperuserRequiredMixin, JSONResponseMixin, UpdateView):
    model = EmployeeSkillRateCount
    fields = ['count']

    def form_valid(self, form):
        form.save()
        return self.render_json_response({
            'pk': self.object.pk,
            'new_count': self.object.count,
        })
