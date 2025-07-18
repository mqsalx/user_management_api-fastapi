# /src/core/configurations/logger/__init__.py

# flake8: noqa: E501

import logging
import os

from colorlog import ColoredFormatter

from src.core.configurations import EnvConfig


class FlushingStreamHandler(logging.StreamHandler):
    """
    Custom stream handler that forces a flush after every log emission.

    This handler ensures that all log records are immediately written
    to the output stream (such as stdout), avoiding delays caused by buffering.
    It is especially useful in asynchronous or background task scenarios
    where log messages may not appear promptly without an explicit flush.
    """
    def emit(self, record):
        """
        Emit a log record and flush the output stream immediately.

        Args:
            record (LogRecord): The log record to be written.
        """
        super().emit(record)
        self.flush()


class LoggerConfig:
    """
    Class responsible for configuring and managing the application logging.

    This class sets up a logger that writes logs to both a console (with colors)
    and a log file. The log level can be determined from an environment variable.

    Class Args:
        None
    """

    def __init__(self) -> None:
        """
        Constructor method for LoggerUtil.

        Initializes and configures the logger with file and console handlers.

        Args:
            None
        """

        self.__api_name: str = EnvConfig().api_name
        self.__api_log_level: str = EnvConfig().api_log_level

        self.__valid_log_levels = [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ]

        # Directory and path for the log file
        _project_root = os.path.abspath(os.path.dirname(__file__))
        _log_dir = os.path.join(_project_root, "../../../logs")
        os.makedirs(_log_dir, exist_ok=True)

        _log_file_name = f"{self.__api_name}.log"
        _log_file = os.path.join(_log_dir, _log_file_name)

        # Console format and message format
        _date_format = "%d-%m-%Y | %H:%M:%S"
        _stream_format = (
            "%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s"
        )
        _log_colors = {
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }

        # Console (stream) formatter setup
        _stream_formatter = ColoredFormatter(
            _stream_format, datefmt=_date_format, log_colors=_log_colors
        )

        # File formatter setup
        _file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        _file_formatter = logging.Formatter(_file_format, datefmt=_date_format)

        # Initialize the logger
        self.__logger = logging.getLogger()

        if not self.__logger.hasHandlers():
            _level = self.__get_log_level_variable()

            # File handler and console handler configuration
            _file_handler = logging.FileHandler(_log_file)
            _file_handler.setFormatter(_file_formatter)

            _stream_handler = FlushingStreamHandler()
            _stream_handler.setFormatter(_stream_formatter)

            self.__logger.setLevel(_level)
            self.__logger.addHandler(_file_handler)
            self.__logger.addHandler(_stream_handler)

            if _level != "DEBUG":
                logging.getLogger("apscheduler").handlers = []
                logging.getLogger("apscheduler").propagate = False
                logging.getLogger("uvicorn.error").handlers = []
                logging.getLogger("uvicorn.error").propagate = False
                logging.getLogger("uvicorn.access").handlers = []
                logging.getLogger("uvicorn.access").propagate = False
                logging.getLogger("uvicorn.asgi").handlers = []
                logging.getLogger("uvicorn.asgi").propagate = True

    def __get_log_level_variable(self) -> str:
        """
        Private method responsible for obtaining the log level from the configuration.

        This method retrieves the log level from the `api_log_level` variable.
        If the value is missing or invalid, it defaults to 'INFO'.

        Args:
            None

        Returns:
            str: The log level ('DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL').
        """

        default_level = "INFO"
        obtained_log_level = self.__api_log_level.upper()

        YELLOW = "\033[33m"
        RESET = "\033[0m"
        MAGENTA = "\033[35m"

        if not obtained_log_level:
            print(
                f"{YELLOW}LOG_LEVEL -> Empty or invalid ‘LOG_LEVEL’ value found. Using default value '{default_level}'!{RESET}"
            )
            return default_level

        if obtained_log_level not in self.__valid_log_levels:
            print(
                f"{YELLOW}LOG_LEVEL -> Invalid value for 'LOG_LEVEL' found: {self.__api_log_level}! Using the default value '{default_level}!{RESET}"
            )
            return default_level

        print(
            f"{MAGENTA}LOG_LEVEL -> Loaded from .env, setting to {obtained_log_level}.{RESET}"
        )

        return obtained_log_level

    @property
    def logger(self) -> logging.Logger:
        """
        Public Method that returns the logger instance for this class.

        This allows access to the configured logger used for emitting
        debug, info, warning, or error messages throughout the class.

        Returns:
            logging.Logger: The logger instance associated with the current class.
        """
        return self.__logger