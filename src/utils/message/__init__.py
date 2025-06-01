# /src/utils/message/__init__.py

# flake8: noqa: E501

from src.core.configurations import EnvConfig


class MessageUtil:
    """
    Class responsible for displaying API startup messages.

    This class formats and prints startup information about the API,
    including its name, version, and running host/port.

    Class Args:
        None
    """

    def __init__(self):
        """
        Constructor method for MessageUtil.

        Initializes the utility by loading API configurations.

        Args:
            None
        """

        self.__api_name = EnvConfig().api_name
        self.__api_host = EnvConfig().api_host
        self.__api_port = EnvConfig().api_port
        self.__api_version = EnvConfig().api_version

    def on_startup(self) -> None:
        """
        Public method responsible for displaying API startup messages.

        This method prints a formatted banner with API details, including its
        name, version, and running URL.

        Args:
            None

        Returns:
            None
        """

        width = 80
        border = "=" * width

        def center_text(text: str) -> str:
            """
            Helper function to center text within the formatted message.

            Args:
                text (str): The text to be centered.

            Returns:
                str: The formatted string with centered text.
            """

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
