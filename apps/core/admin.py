from django.contrib import admin
from apps.core.models import Employee, SkillRate, Skill, Estimation


class EstimationAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_table_link')

    def get_table_link(self, obj):
        return '<a href={}>Go to table view</a>'.format(obj.get_table_url())
    get_table_link.allow_tags = True


admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(SkillRate)
admin.site.register(Estimation, EstimationAdmin)
