import uuid
from datetime import datetime, timedelta, timezone

from backend.auth.models.refresh_token import RefreshToken
from backend.auth.models.usuario import Usuario
from backend.core.config import get_settings
from backend.core.exceptions import ConflictException, ForbiddenException, UnauthorizedException
from backend.core.security import create_access_token, get_password_hash, verify_password
from backend.core.uow import UnitOfWork

settings = get_settings()


def build_user_dict(user):
    return {
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "telefono": user.telefono,
        "roles": [ur.rol.nombre for ur in user.roles],
        "eliminado_en": user.eliminado_en.isoformat() if user.eliminado_en else None,
        "creado_en": user.creado_en.isoformat() if user.creado_en else None,
        "actualizado_en": user.actualizado_en.isoformat() if user.actualizado_en else None,
    }


class AuthService:
    async def register(
        self, session, nombre: str, email: str, password: str, telefono: str | None = None
    ) -> dict:
        async with UnitOfWork(session) as uow:
            existing = await uow.usuarios.get_by_email(email)
            if existing:
                raise ConflictException(detail="El email ya está registrado")

            user = Usuario(
                nombre=nombre,
                email=email,
                password_hash=get_password_hash(password),
                telefono=telefono,
            )
            user = await uow.usuarios.create(user)

            client_rol = await uow.roles.get_by_nombre("CLIENT")
            if client_rol:
                await uow.usuario_roles.asignar_rol(user.id, client_rol.id)

            user = await uow.usuarios.get_with_roles(user.id)
            roles_list = [ur.rol.nombre for ur in user.roles]

            access_token = create_access_token(
                data={"sub": str(user.id), "email": user.email, "roles": roles_list}
            )
            refresh_token_value = uuid.uuid4().hex

            rt = RefreshToken(
                token=refresh_token_value,
                usuario_id=user.id,
                expires_at=datetime.now(timezone.utc)
                + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )
            await uow.refresh_tokens.create(rt)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_value,
            "token_type": "bearer",
            "user": build_user_dict(user),
        }

    async def login(self, session, email: str, password: str) -> dict:
        async with UnitOfWork(session) as uow:
            user = await uow.usuarios.get_by_email(email)
            if not user or not verify_password(password, user.password_hash):
                raise UnauthorizedException(detail="Email o contraseña incorrectos")

            if user.eliminado_en is not None:
                raise ForbiddenException(detail="Cuenta desactivada")

            user = await uow.usuarios.get_with_roles(user.id)
            roles_list = [ur.rol.nombre for ur in user.roles]

            access_token = create_access_token(
                data={"sub": str(user.id), "email": user.email, "roles": roles_list}
            )
            refresh_token_value = uuid.uuid4().hex

            rt = RefreshToken(
                token=refresh_token_value,
                usuario_id=user.id,
                expires_at=datetime.now(timezone.utc)
                + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )
            await uow.refresh_tokens.create(rt)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_value,
            "token_type": "bearer",
            "user": build_user_dict(user),
        }

    async def refresh_token(self, session, token: str) -> dict:
        async with UnitOfWork(session) as uow:
            rt = await uow.refresh_tokens.get_valid_token(token)

            if not rt:
                existing = await uow.refresh_tokens.list_all(filters={"token": token})
                if existing:
                    await uow.refresh_tokens.invalidate_all_for_user(
                        existing[0].usuario_id
                    )
                raise UnauthorizedException(detail="Token inválido")

            await uow.refresh_tokens.invalidate_token(token)

            user = await uow.usuarios.get_with_roles(rt.usuario_id)
            roles_list = [ur.rol.nombre for ur in user.roles]

            access_token = create_access_token(
                data={"sub": str(user.id), "email": user.email, "roles": roles_list}
            )
            new_refresh_token = uuid.uuid4().hex

            new_rt = RefreshToken(
                token=new_refresh_token,
                usuario_id=user.id,
                expires_at=datetime.now(timezone.utc)
                + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )
            await uow.refresh_tokens.create(new_rt)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "user": build_user_dict(user),
        }

    async def logout(self, session, token: str) -> None:
        async with UnitOfWork(session) as uow:
            await uow.refresh_tokens.invalidate_token(token)
