# /src/utils/dot_env/dot_env_util.py


from dotenv import find_dotenv


class DotEnvUtil:

    def __init__(self):

        self.__env_path = find_dotenv()

    def check_dot_env(self) -> None:

        additional_message = "ENV VARIABLES -> "

        if not self.__env_path:
            message = (
                f"\n\033[32m\033[1m{additional_message}The file .env is not loaded! ... running default env variables\033[0m"
            )
            print(message)

        message = f"\n\033[32m\033[1m{additional_message}The file .env is loaded!\033[0m"
        print(message)
