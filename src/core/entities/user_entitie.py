class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def validate_email(self):
        if "@" not in self.email:
            raise ValueError("Invalid email format")
