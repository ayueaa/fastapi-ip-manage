import asyncio

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)
from fastapi_users_db_beanie import BeanieUserDatabase, ObjectIDIDMixin
from loguru import logger

from app.api.models.auth import UserCreate
from app.api.models.user import User, get_user_db
from app.core.config import get_app_settings
from app.services.email_sender import aio_email_sender

SECRET = get_app_settings().secret_key


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def validate_password(
        self,
        password: str,
        user: UserCreate | User,
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")

    async def on_after_register(self, user: User, request: Request = None):
        # 前端需要提示去邮箱认证，请求verify-token
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request = None
    ):
        from_email = "woyue02@gmail.com"
        to_email = user.email
        subject = "IP-Manage 注册邮箱验证"
        body = f"""
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>注册验证</title>
            </head>
            <body>
                <p>亲爱的 {user.email},</p>

                <p>感谢你注册我们的服务！为了确保你的账户安全，我们需要验证你的电子邮件地址。请复制以下验证令牌并粘贴到认证页面以完成验证流程：</p>

                <p><strong>验证令牌：</strong> {token}</p>

                <p>如果你无法点击下面的链接，请手动复制并粘贴验证令牌到我们的认证页面。</p>

                <p><a href="https://127.0.0.1:8080/docs">点击此处前往认证页面</a></p>

                <p>如果你没有尝试注册此账户，请忽略此邮件。</p>

                <p>如果你需要任何帮助或有任何疑问，请随时联系我们的客户支持团队。</p>

                <p>谢谢你选择我们的服务！</p>

                <p>祝一切顺利，<br>你的服务团队</p>
            </body>
            </html>
        """

        #  异步发送邮件
        asyncio.create_task(aio_email_sender.send(from_email, to_email, subject, body))
        # 前端页面弹出输入框，等待用户输入token
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )

    async def on_after_verify(self, user: User, request: Request | None = None) -> None:
        print(f"Verified user {user.email}.")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(cookie_max_age=3600)


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_active_verfied_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
