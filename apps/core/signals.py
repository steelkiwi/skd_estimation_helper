from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import Skill, Employee, SkillRate, Estimation


@receiver(post_save, sender=Skill)
def create_skill_values(sender, instance, created, **kwargs):
    for v in range(instance.min_rate, instance.max_rate + 1):
        instance.rates.get_or_create(value=v)
