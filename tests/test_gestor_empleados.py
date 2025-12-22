"""Pruebas funcionales para el gestor de empleados (CRUD)."""
import os
import tempfile

import pytest

from employee_manager import gestor_empleados
from employee_manager.models import Employee
from employee_manager.json_storage import JsonStorage


def _make_storage():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name
    tmp.close()
    return JsonStorage(path), path


def test_add_and_list_employee():
    storage, path = _make_storage()
    try:
        emp = Employee(id="e1", first_name="Ana", last_name="Lopez")
        gestor_empleados.add_employee(storage, emp)

        all_emps = gestor_empleados.list_employees(storage)
        assert len(all_emps) == 1
        assert all_emps[0].id == "e1"
        assert all_emps[0].first_name == "Ana"
    finally:
        os.remove(path)


def test_add_duplicate_raises():
    storage, path = _make_storage()
    try:
        emp = Employee(id="e1", first_name="Ana", last_name="Lopez")
        gestor_empleados.add_employee(storage, emp)
        with pytest.raises(ValueError):
            gestor_empleados.add_employee(storage, emp)
    finally:
        os.remove(path)


def test_get_update_delete_employee():
    storage, path = _make_storage()
    try:
        emp = Employee(id="e2", first_name="Luis", last_name="Gomez")
        gestor_empleados.add_employee(storage, emp)

        got = gestor_empleados.get_employee(storage, "e2")
        assert got is not None
        assert got.first_name == "Luis"

        gestor_empleados.update_employee(storage, "e2", {"first_name": "Luisito"})
        got2 = gestor_empleados.get_employee(storage, "e2")
        assert got2 is not None
        assert got2.first_name == "Luisito"

        gestor_empleados.delete_employee(storage, "e2")
        assert gestor_empleados.get_employee(storage, "e2") is None

        with pytest.raises(ValueError):
            gestor_empleados.update_employee(storage, "nonexistent", {"first_name": "x"})

        with pytest.raises(ValueError):
            gestor_empleados.delete_employee(storage, "nonexistent")
    finally:
        os.remove(path)
