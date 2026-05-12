"""Tests for security enhancements."""


def test_permission_map_public_endpoints():
    from backend.core.permissions import PERMISSIONS
    public = [p for p in PERMISSIONS if p.public]
    assert any("auth/login" in p.path for p in public)
    assert any("auth/register" in p.path for p in public)
    assert any("/productos" in p.path and "GET" in p.methods for p in public)


def test_permission_map_admin_only():
    from backend.core.permissions import PERMISSIONS
    admin = [p for p in PERMISSIONS if "ADMIN" in p.allowed_roles and len(p.allowed_roles) == 1]
    assert any("/admin" in p.path for p in admin)


def test_permission_map_stock_admin():
    from backend.core.permissions import PERMISSIONS
    stock_admin = [p for p in PERMISSIONS if "STOCK" in p.allowed_roles and "ADMIN" in p.allowed_roles]
    assert any("productos" in p.path and "POST" in p.methods for p in stock_admin)
