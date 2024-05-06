from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from core.domain.value_objects.auth import Auth
from security.base import get_current_user, Token
from security.user_security import authenticate_user, handle_user_signup


class AuthController:
    def __init__(self):
        self.router = APIRouter(tags=["User Authentication"], prefix='/auth-user')
        self.router.add_api_route(
            path="/login",
            endpoint=self.login,
            methods=["POST"],
            response_model=Token,
            status_code=200
        )
        self.router.add_api_route(
            path="/signup",
            endpoint=self.signup,
            methods=["POST"],
            response_model=Token,
            status_code=200
        )

    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        """
        Retorna token de acesso validando cadastro de usuário
        """
        return authenticate_user(form_data)

    async def signup(
            self,
            cpf: Annotated[str, Form()],
            nome: Annotated[str, Form()],
            email: Annotated[str, Form()],
            password: Annotated[str, Form()],
            current_user=Depends(get_current_user)
    ):
        """
        Cadastra usuário e retorna token de acesso
        * Necessário ter permissionamento de usuário admin
        """
        auth = Auth(cpf=cpf, name=nome, email=email, admin=True, password=password)
        return handle_user_signup(auth, current_user)
