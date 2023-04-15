import datetime
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender='movies.FilmWork')
def attention(sender, instance, created, **kwargs):
    if created and instance.creation_date == datetime.date.today():
        logger.info(f"Сегодня премьера {instance.title}! 🥳")
