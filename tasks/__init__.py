import sched

from . import weather

scheduler = sched.scheduler()


def periodic(scheduler, interval, action, actionargs=()):
    action(*actionargs)

    scheduler.enter(interval, 1, periodic, (scheduler, interval, action, actionargs))


def run():
    periodic(scheduler, weather.INTERVAL, weather.get_forecast)
