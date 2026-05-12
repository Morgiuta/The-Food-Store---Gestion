import pytest

from backend.auth.models.usuario import Usuario
from backend.auth.repositories.usuario import UsuarioRepository


class TestBaseRepositoryCRUD:
    async def test_create_returns_instance_with_id(self, session):
        repo = UsuarioRepository(session)
        usuario = Usuario(
            nombre="Create Test",
            email="create@test.com",
            password_hash="hash123",
        )
        created = await repo.create(usuario)
        assert created.id is not None
        assert created.nombre == "Create Test"
        assert created.email == "create@test.com"

    async def test_get_by_id_returns_matching_record(self, session):
        repo = UsuarioRepository(session)
        usuario = Usuario(
            nombre="Get Test",
            email="get@test.com",
            password_hash="hash123",
        )
        created = await repo.create(usuario)
        found = await repo.get_by_id(created.id)
        assert found is not None
        assert found.id == created.id
        assert found.email == "get@test.com"

    async def test_get_by_id_returns_none_when_not_found(self, session):
        repo = UsuarioRepository(session)
        found = await repo.get_by_id(9999)
        assert found is None

    async def test_list_all_returns_all_records(self, session):
        repo = UsuarioRepository(session)
        await repo.create(Usuario(
            nombre="List A", email="lista@test.com", password_hash="h1"
        ))
        await repo.create(Usuario(
            nombre="List B", email="listb@test.com", password_hash="h2"
        ))
        all_users = await repo.list_all()
        assert len(all_users) >= 2

    async def test_list_all_with_pagination(self, session):
        repo = UsuarioRepository(session)
        await repo.create(Usuario(
            nombre="Page A", email="pagea@test.com", password_hash="h1"
        ))
        await repo.create(Usuario(
            nombre="Page B", email="pageb@test.com", password_hash="h2"
        ))
        users = await repo.list_all(skip=0, limit=1)
        assert len(users) <= 1

    async def test_update_modifies_fields(self, session):
        repo = UsuarioRepository(session)
        usuario = Usuario(
            nombre="Old Name",
            email="update@test.com",
            password_hash="hash123",
        )
        created = await repo.create(usuario)
        updated = await repo.update(created.id, {"nombre": "New Name"})
        assert updated is not None
        assert updated.nombre == "New Name"
        assert updated.email == "update@test.com"

    async def test_update_returns_none_when_not_found(self, session):
        repo = UsuarioRepository(session)
        result = await repo.update(9999, {"nombre": "Ghost"})
        assert result is None

    async def test_soft_delete_sets_eliminado_en(self, session):
        repo = UsuarioRepository(session)
        usuario = Usuario(
            nombre="Soft Delete",
            email="softdelete@test.com",
            password_hash="hash123",
        )
        created = await repo.create(usuario)
        assert created.eliminado_en is None
        deleted = await repo.soft_delete(created.id)
        assert deleted is not None
        assert deleted.eliminado_en is not None

    async def test_soft_delete_returns_none_when_not_found(self, session):
        repo = UsuarioRepository(session)
        result = await repo.soft_delete(9999)
        assert result is None

    async def test_count_returns_total(self, session):
        repo = UsuarioRepository(session)
        await repo.create(Usuario(
            nombre="Count A", email="counta@test.com", password_hash="h1"
        ))
        await repo.create(Usuario(
            nombre="Count B", email="countb@test.com", password_hash="h2"
        ))
        count = await repo.count()
        assert count >= 2

    async def test_count_with_filters(self, session):
        repo = UsuarioRepository(session)
        await repo.create(Usuario(
            nombre="Filter Target",
            email="filter@test.com",
            password_hash="h1",
        ))
        await repo.create(Usuario(
            nombre="Other",
            email="other@test.com",
            password_hash="h2",
        ))
        count = await repo.count(filters={"nombre": "Filter Target"})
        assert count == 1

    async def test_exists_returns_true_for_existing_record(self, session):
        repo = UsuarioRepository(session)
        usuario = Usuario(
            nombre="Exists",
            email="exists@test.com",
            password_hash="hash123",
        )
        created = await repo.create(usuario)
        assert await repo.exists(created.id) is True

    async def test_exists_returns_false_for_non_existent_record(self, session):
        repo = UsuarioRepository(session)
        assert await repo.exists(9999) is False

    async def test_hard_delete_removes_record(self, session):
        repo = UsuarioRepository(session)
        usuario = Usuario(
            nombre="Hard Delete",
            email="harddelete@test.com",
            password_hash="hash123",
        )
        created = await repo.create(usuario)
        deleted = await repo.hard_delete(created.id)
        assert deleted is True
        found = await repo.get_by_id(created.id)
        assert found is None

    async def test_hard_delete_returns_false_when_not_found(self, session):
        repo = UsuarioRepository(session)
        result = await repo.hard_delete(9999)
        assert result is False
