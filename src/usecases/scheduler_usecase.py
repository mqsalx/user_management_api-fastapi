#  /src/usecases/scheduler_usecase.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def schedule_function(self, func, interval_seconds):
        """
        Agenda uma função para ser chamada em intervalos regulares.

        :param func: A função a ser agendada.
        :param interval_seconds: Intervalo em segundos entre chamadas da função.
        """
        self.scheduler.add_job(
            func, trigger=IntervalTrigger(seconds=interval_seconds)
        )

    def shutdown(self):
        """Desliga o scheduler."""
        self.scheduler.shutdown()
