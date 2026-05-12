from backend.core.exceptions import ConflictException, NotFoundException
from backend.core.uow import UnitOfWork
from backend.auth.services.auth_service import build_user_dict


class RoleService:
    async def assign_role(
        self, session, admin_user: dict, usuario_id: int, rol_nombre: str
    ) -> dict:
        async with UnitOfWork(session) as uow:
            user = await uow.usuarios.get_with_roles(usuario_id)
            if not user:
                raise NotFoundException(detail="Usuario no encontrado")

            rol = await uow.roles.get_by_nombre(rol_nombre)
            if not rol:
                raise NotFoundException(detail=f"Rol '{rol_nombre}' no encontrado")

            existing_roles = [ur.rol.nombre for ur in user.roles]
            if rol_nombre in existing_roles:
                raise ConflictException(
                    detail=f"El usuario ya tiene el rol '{rol_nombre}'"
                )

            await uow.usuario_roles.asignar_rol(user.id, rol.id)

            user = await uow.usuarios.get_with_roles(user.id)

        return build_user_dict(user)

    async def revoke_role(
        self, session, admin_user: dict, usuario_id: int, rol_nombre: str
    ) -> dict:
        async with UnitOfWork(session) as uow:
            rol = await uow.roles.get_by_nombre(rol_nombre)
            if not rol:
                raise NotFoundException(detail=f"Rol '{rol_nombre}' no encontrado")

            if rol_nombre == "ADMIN":
                admin_count = await uow.usuario_roles.count_admins()
                if admin_count <= 1:
                    raise ConflictException(
                        detail="No se puede remover el último administrador del sistema"
                    )

            success = await uow.usuario_roles.revocar_rol(usuario_id, rol.id)
            if not success:
                raise NotFoundException(
                    detail="El usuario no tiene el rol especificado"
                )

            user = await uow.usuarios.get_with_roles(usuario_id)
            if not user:
                raise NotFoundException(detail="Usuario no encontrado")

        return build_user_dict(user)
