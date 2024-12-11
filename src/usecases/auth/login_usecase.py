from src.utils.auth.jwt_utils import create_token
from src.adapters.repositories.user_repository import UserRepository
from src.core.entities.login_entity import User


class LoginUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, email: str, password: str) -> str:
        """Autentica um usuário e retorna um token JWT."""
        user = self.user_repository.find_by_email(email)
        if not user or not user.verify_password(password):
            raise ValueError("Credenciais inválidas.")

        # Dados para o token JWT
        token_data = {"sub": user.email}
        token = create_access_token(token_data)
        return token
