from celery import shared_task
from random import choice
from datetime import datetime
from .models import Material, WeeklyMaterial

@shared_task
def add_weekly_ingredient():
    ingredients = Material.objects.all()
    random_ingredient = choice(ingredients)
    week_start = datetime.now().date()
    WeeklyMaterial.objects.create(ingredient=random_ingredient, week=week_start)
