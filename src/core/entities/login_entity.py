# /src/core/entities/login_entity.py


class Login:
    """
    Represents the login entity.
    """

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def validate(self):
        if not self.email or not self.password:
            raise ValueError("Email and password are required!")
