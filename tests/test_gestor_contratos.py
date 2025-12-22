"""Pruebas funcionales para el gestor de contratos (CRUD)."""
import os
import tempfile

import pytest

from employee_manager import gestor_contratos
from employee_manager.models import Contract
from employee_manager.json_storage import JsonStorage


def _make_storage():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name
    tmp.close()
    return JsonStorage(path), path


def test_add_and_list_contract():
    storage, path = _make_storage()
    try:
        c = Contract(id="c1", employee_id="e1", start_date="2025-02-01")
        gestor_contratos.add_contract(storage, c)

        all_cs = gestor_contratos.list_contracts(storage)
        assert len(all_cs) == 1
        assert all_cs[0].id == "c1"
        assert all_cs[0].employee_id == "e1"
    finally:
        os.remove(path)


def test_add_duplicate_raises():
    storage, path = _make_storage()
    try:
        c = Contract(id="c1", employee_id="e1", start_date="2025-02-01")
        gestor_contratos.add_contract(storage, c)
        with pytest.raises(ValueError):
            gestor_contratos.add_contract(storage, c)
    finally:
        os.remove(path)


def test_get_update_delete_contract():
    storage, path = _make_storage()
    try:
        c = Contract(id="c2", employee_id="e2", start_date="2025-03-01")
        gestor_contratos.add_contract(storage, c)

        got = gestor_contratos.get_contract(storage, "c2")
        assert got is not None
        assert got.employee_id == "e2"

        gestor_contratos.update_contract(storage, "c2", {"position": "Engineer"})
        got2 = gestor_contratos.get_contract(storage, "c2")
        assert got2 is not None
        assert got2.position == "Engineer"

        gestor_contratos.delete_contract(storage, "c2")
        assert gestor_contratos.get_contract(storage, "c2") is None

        with pytest.raises(ValueError):
            gestor_contratos.update_contract(storage, "nonexistent", {"position": "x"})

        with pytest.raises(ValueError):
            gestor_contratos.delete_contract(storage, "nonexistent")
    finally:
        os.remove(path)


def test_add_contract_invalid_date_format():
    storage, path = _make_storage()
    try:
        c = Contract(id="c3", employee_id="e3", start_date="invalid-date")
        with pytest.raises(ValueError, match="formato"):
            gestor_contratos.add_contract(storage, c)
    finally:
        os.remove(path)


def test_add_contract_end_before_start():
    storage, path = _make_storage()
    try:
        c = Contract(
            id="c4",
            employee_id="e4",
            start_date="2025-03-01",
            end_date="2025-02-01"
        )
        with pytest.raises(ValueError, match="posterior"):
            gestor_contratos.add_contract(storage, c)
    finally:
        os.remove(path)


def test_add_contract_validate_employee():
    storage, path = _make_storage()
    try:
        c = Contract(id="c5", employee_id="e5", start_date="2025-01-01")
        
        # Sin validación, debería funcionar
        gestor_contratos.add_contract(storage, c)
        
        # Con validación que falla
        def employee_exists(emp_id: str) -> bool:
            return False
        
        c2 = Contract(id="c6", employee_id="e6", start_date="2025-01-01")
        with pytest.raises(ValueError, match="no existe"):
            gestor_contratos.add_contract(storage, c2, validate_employee=employee_exists)
    finally:
        os.remove(path)
