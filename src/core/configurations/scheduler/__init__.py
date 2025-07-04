#  /src/core/configurations/scheduler/__init__.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class SchedulerConfig:
    """
    Class responsible for managing scheduled tasks.

    This class uses `BackgroundScheduler` to execute functions at regular intervals.
    """

    def __init__(self) -> None:
        """
        Constructor method for Scheduler.

        Initializes the scheduler and starts it in the background.

        Args:
            None
        """

        self.__scheduler: BackgroundScheduler = BackgroundScheduler()
        self.__scheduler.start()

    def init(self, func, interval_seconds) -> None:
        """
        Public method responsible for scheduling a function to run at regular intervals.

        Args:
            func (callable): The function to be scheduled.
            interval_seconds (int): The interval in seconds between function executions.

        Returns:
            None
        """

        self.__scheduler.add_job(
            func,
            trigger=IntervalTrigger(seconds=interval_seconds)
        )

    def shutdown(self) -> None:
        """
        Public method responsible for shutting down the scheduler.

        This method stops all scheduled jobs and shuts down the scheduler instance.

        Args:
            None

        Returns:
            None
        """

        self.__scheduler.shutdown()

scheduler_config = SchedulerConfig()
