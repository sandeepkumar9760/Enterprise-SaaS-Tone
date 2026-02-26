from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(pre_save, sender=MakeUpClass)
def generate_remedial_code(sender, instance, **kwargs):
    if not instance.remedial_code:
        instance.remedial_code = f"RC-{uuid.uuid4().hex[:6].upper()}"
