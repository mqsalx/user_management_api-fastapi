# /src/utils/log/console_logger_util.py


class ConsoleLoggerUtil:
    """

    Console logger utility.

    """

    def __init__(self):

        self.__color = {
            "RED": "\033[91m",
            "GREEN": "\033[92m",
            "YELLOW": "\033[93m",
            "RESET": "\033[0m",
        }

    def log_info(self, message: str):
        color = self.__color["GREEN"]
        reset = self.__color["RESET"]
        print(f"{color}[INFO]{reset}     {message}")

    def log_warning(self, message: str):
        color = self.__color["YELLOW"]
        reset = self.__color["RESET"]
        print(f"{color}[WARNING]{reset}     {message}")

    def log_error(self, message: str):
        color = self.__color["RED"]
        reset = self.__color["RESET"]
        print(f"{color}ERROR{reset}     {message}")
