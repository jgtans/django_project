from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import EmployeePhoto


@receiver(post_delete, sender=EmployeePhoto)
def delete_photo_file(sender, instance, **kwargs):
    """Фото удаляется с диска при удалении записи из бд"""
    if instance.image:
        instance.image.delete()
