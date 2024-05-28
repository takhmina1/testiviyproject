from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import asyncio
from .services import *


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, IntervalTrigger(minutes=10), name='update_crypto_rates')
def scheduled_crypto_task():
    asyncio.run(update_crypto_rates())

@register_job(scheduler, IntervalTrigger(minutes=30), name='update_fiat_rates')
def scheduled_fiat_task():
    asyncio.run(update_fiat_rates())

register_events(scheduler)

def start():
    scheduler.start()
    print("Scheduler started...")
