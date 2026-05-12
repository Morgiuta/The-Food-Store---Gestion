from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from backend.auth.models.rol import Rol
from backend.auth.models.usuario import Usuario
from backend.auth.models.usuario_rol import UsuarioRol
from backend.auth.services.auth_service import build_user_dict
from backend.core.exceptions import ConflictException, ForbiddenException, NotFoundException
from backend.core.uow import UnitOfWork


class AdminUsuarioService:
    async def list_usuarios(self, session, skip=0, limit=100, search=None, rol=None) -> dict:
        query = (
            select(Usuario)
            .options(selectinload(Usuario.roles).selectinload(UsuarioRol.rol))
            .order_by(Usuario.id)
        )

        count_query = select(func.count(func.distinct(Usuario.id))).select_from(Usuario)

        if search:
            filter_clause = Usuario.nombre.ilike(f"%{search}%") | Usuario.email.ilike(f"%{search}%")
            query = query.where(filter_clause)
            count_query = count_query.where(filter_clause)

        if rol:
            query = (
                query
                .join(Usuario.roles)
                .join(UsuarioRol.rol)
                .where(Rol.nombre == rol)
                .distinct()
            )
            count_query = (
                count_query
                .join(UsuarioRol, UsuarioRol.usuario_id == Usuario.id)
                .join(Rol, Rol.id == UsuarioRol.rol_id)
                .where(Rol.nombre == rol)
            )

        count_result = await session.execute(count_query)
        total = count_result.scalar_one()

        result = await session.execute(query.offset(skip).limit(limit))
        users = result.unique().scalars().all()

        return {
            "items": [build_user_dict(u) for u in users],
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "limit": limit,
        }

    async def get_usuario(self, session, usuario_id: int) -> dict:
        stmt = (
            select(Usuario)
            .where(Usuario.id == usuario_id)
            .options(selectinload(Usuario.roles).selectinload(UsuarioRol.rol))
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException(detail="Usuario no encontrado")
        return build_user_dict(user)

    async def update_usuario(self, session, admin_user: dict, usuario_id: int, data: dict) -> dict:
        async with UnitOfWork(session) as uow:
            user = await uow.usuarios.get_with_roles(usuario_id)
            if not user:
                raise NotFoundException(detail="Usuario no encontrado")

            update_data = {}
            for field in ("nombre", "email", "telefono"):
                if field in data:
                    update_data[field] = data[field]

            if update_data:
                await uow.usuarios.update(usuario_id, update_data)

            if "roles" in data:
                new_role_names = data["roles"]
                current_roles = await uow.usuario_roles.get_user_roles(usuario_id)
                current_role_names = {ur.rol.nombre for ur in current_roles}

                roles_to_remove = current_role_names - set(new_role_names)
                roles_to_add = set(new_role_names) - current_role_names

                if "ADMIN" in roles_to_remove:
                    admin_count = await uow.usuario_roles.count_admins()
                    if admin_count <= 1:
                        raise ConflictException(
                            detail="No se puede remover el rol ADMIN al último administrador"
                        )

                for role_name in roles_to_remove:
                    rol_obj = await uow.roles.get_by_nombre(role_name)
                    if rol_obj:
                        await uow.usuario_roles.revocar_rol(usuario_id, rol_obj.id)

                for role_name in roles_to_add:
                    rol_obj = await uow.roles.get_by_nombre(role_name)
                    if rol_obj:
                        await uow.usuario_roles.asignar_rol(usuario_id, rol_obj.id)

            user = await uow.usuarios.get_with_roles(usuario_id)
            return build_user_dict(user)

    async def toggle_estado(self, session, admin_user: dict, usuario_id: int) -> dict:
        if admin_user["user_id"] == usuario_id:
            raise ForbiddenException(detail="No puedes desactivar tu propia cuenta")

        async with UnitOfWork(session) as uow:
            user = await uow.usuarios.get_with_roles(usuario_id)
            if not user:
                raise NotFoundException(detail="Usuario no encontrado")

            now = datetime.now(timezone.utc)

            if user.eliminado_en is None:
                user_role_names = {ur.rol.nombre for ur in user.roles}
                if "ADMIN" in user_role_names:
                    admin_count = await uow.usuario_roles.count_admins()
                    if admin_count <= 1:
                        raise ConflictException(
                            detail="No se puede desactivar al último administrador"
                        )

                user.eliminado_en = now
                await uow.refresh_tokens.invalidate_all_for_user(usuario_id)
            else:
                user.eliminado_en = None

            await session.flush()

            user = await uow.usuarios.get_with_roles(usuario_id)
            return build_user_dict(user)
