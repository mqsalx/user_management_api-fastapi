# /src/utils/logger/__init__.py

# flake8: noqa: E501

from src.core.configurations import LoggerConfig


class LoggerUtil:
    """
    Class responsible for configuring and managing the application logging.

    This class sets up a logger that writes logs to both a console (with colors)
    and a log file. The log level can be determined from an environment variable.

    Class Args:
        None
    """

    def __init__(self):
        """
        Constructor method for LoggerUtil.

        Initializes and configures the logger with file and console handlers.

        Args:
            None
        """
        self.__logger = LoggerConfig().logger

    def info(self, message: str) -> None:
        """
        Public method responsible for logging an 'INFO' level message.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """

        self.__logger.info(message)

    def error(self, message: str) -> None:
        """
        Public method responsible for logging an 'ERROR' level message.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """

        self.__logger.error(message)

    def debug(self, message: str) -> None:
        """
        Public method responsible for logging a 'DEBUG' level message.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """

        self.__logger.debug(message)

    def warning(self, message: str) -> None:
        """
        Public method responsible for logging a 'WARNING' level message.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """

        self.__logger.warning(message)