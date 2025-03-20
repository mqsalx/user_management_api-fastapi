#  /src/usecases/scheduler_usecase.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class Scheduler:
    """
    Class responsible for managing scheduled tasks.

    This class uses `BackgroundScheduler` to execute functions at regular intervals.

    Class Args:
        None
    """

    def __init__(self):
        """
        Constructor method for Scheduler.

        Initializes the scheduler and starts it in the background.

        Args:
            None
        """

        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def schedule_function(self, func, interval_seconds):
        """
        Public method responsible for scheduling a function to run at regular intervals.

        Args:
            func (callable): The function to be scheduled.
            interval_seconds (int): The interval in seconds between function executions.

        Returns:
            None
        """

        self.scheduler.add_job(
            func, trigger=IntervalTrigger(seconds=interval_seconds)
        )

    def shutdown(self):
        """
        Public method responsible for shutting down the scheduler.

        This method stops all scheduled jobs and shuts down the scheduler instance.

        Args:
            None

        Returns:
            None
        """

        self.scheduler.shutdown()
