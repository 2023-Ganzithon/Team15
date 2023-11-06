from celery import Celery
from celery.schedules import crontab

app = Celery('Team15')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 주간 재료 생성 함수 스케줄링
app.conf.beat_schedule = {
    'add-weekly-ingredient': {
        'task': 'Team15.tasks.add_weekly_ingredient',
        'schedule': crontab(minute=0, hour=0, day_of_week=1),  # 매주 월요일 00:00시
    },
}
