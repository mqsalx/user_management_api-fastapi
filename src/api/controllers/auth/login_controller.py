from src.usecases.auth.login_usecase import LoginUseCase


class LoginController:
    """
        Controlador para autenticação de usuários.
    """

    def __init__(self, login_usecase: LoginUseCase):
        self.login_usecase = login_usecase

    def login(self, email: str, password: str) -> dict:
        """Realiza login e retorna um token JWT."""
        token = self.login_usecase.authenticate_user(email, password)
        return {"access_token": token, "token_type": "bearer"}
