# /src/utils/message_util.py

from src.core.configurations.env_configuration import EnvConfiguration


class MessageUtil:

    def __init__(self):
        self.__api_name = EnvConfiguration().api_name
        self.__api_host = EnvConfiguration().api_host
        self.__api_port = EnvConfiguration().api_port
        self.__api_version = EnvConfiguration().api_version

    def on_startup(self):
        width = 80
        border = "=" * width

        def center_text(text):
            return f"|{text.center(width - 2)}|"

        print("\n" + border)
        print(center_text(""))
        print(center_text(f"API: {self.__api_name}"))
        print(center_text(f"Version: {self.__api_version}"))
        print(
            center_text(
                f"Running on: {self.__api_host}:{self.__api_port}/api/{self.__api_version}"
            )
        )
        print(center_text(""))
        print(border + "\n")
