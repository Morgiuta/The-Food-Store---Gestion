from backend.auth.services.auth_service import build_user_dict
from backend.core.exceptions import NotFoundException, UnauthorizedException
from backend.core.security import get_password_hash, verify_password
from backend.core.uow import UnitOfWork


class PerfilService:
    async def get_perfil(self, session, user_id: int) -> dict:
        async with UnitOfWork(session) as uow:
            user = await uow.usuarios.get_with_roles(user_id)
            if not user:
                raise NotFoundException(detail="Usuario no encontrado")
            return build_user_dict(user)

    async def update_perfil(self, session, user_id: int, data: dict) -> dict:
        async with UnitOfWork(session) as uow:
            user = await uow.usuarios.get_with_roles(user_id)
            if not user:
                raise NotFoundException(detail="Usuario no encontrado")

            update_data = {}
            for field in ("nombre", "email", "telefono"):
                if field in data:
                    update_data[field] = data[field]

            if update_data:
                await uow.usuarios.update(user_id, update_data)

            user = await uow.usuarios.get_with_roles(user_id)
            return build_user_dict(user)

    async def change_password(self, session, user_id: int, password_actual: str, password_nueva: str) -> None:
        async with UnitOfWork(session) as uow:
            user = await uow.usuarios.get_with_roles(user_id)
            if not user:
                raise NotFoundException(detail="Usuario no encontrado")

            if not verify_password(password_actual, user.password_hash):
                raise UnauthorizedException(detail="Contraseña actual incorrecta")

            await uow.usuarios.update(user_id, {"password_hash": get_password_hash(password_nueva)})

            await uow.refresh_tokens.invalidate_all_for_user(user_id)
