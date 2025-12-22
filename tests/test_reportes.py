"""Pruebas para el módulo de reportes."""
import os
import tempfile
from datetime import datetime, timedelta

import pytest

from employee_manager.json_storage import JsonStorage
from employee_manager.models import Employee, Contract
from employee_manager import gestor_empleados, gestor_contratos
from employee_manager.reportes import (
    get_employee_with_contracts,
    list_employees_with_contracts,
    get_expired_contracts,
    get_employees_with_expired_contracts,
    get_contracts_by_employee,
)


def _make_storages():
    """Crear storages temporales para empleados y contratos."""
    tmp_emp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    emp_path = tmp_emp.name
    tmp_emp.close()
    
    tmp_con = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    con_path = tmp_con.name
    tmp_con.close()
    
    return JsonStorage(emp_path), JsonStorage(con_path), emp_path, con_path


def test_get_employee_with_contracts():
    emp_storage, con_storage, emp_path, con_path = _make_storages()
    try:
        # Crear empleado
        emp = Employee(id="e1", first_name="Juan", last_name="Perez")
        gestor_empleados.add_employee(emp_storage, emp)
        
        # Crear contratos
        c1 = Contract(id="c1", employee_id="e1", start_date="2024-01-01", end_date="2024-12-31")
        c2 = Contract(id="c2", employee_id="e1", start_date="2025-01-01")
        gestor_contratos.add_contract(con_storage, c1)
        gestor_contratos.add_contract(con_storage, c2)
        
        # Consultar
        result = get_employee_with_contracts(emp_storage, con_storage, "e1")
        assert result is not None
        assert result.employee.id == "e1"
        assert len(result.contracts) == 2
        assert any(c.id == "c1" for c in result.contracts)
        assert any(c.id == "c2" for c in result.contracts)
        
        # Empleado inexistente
        result2 = get_employee_with_contracts(emp_storage, con_storage, "nonexistent")
        assert result2 is None
    finally:
        os.remove(emp_path)
        os.remove(con_path)


def test_list_employees_with_contracts():
    emp_storage, con_storage, emp_path, con_path = _make_storages()
    try:
        # Crear empleados
        emp1 = Employee(id="e1", first_name="Juan", last_name="Perez")
        emp2 = Employee(id="e2", first_name="Maria", last_name="Gomez")
        gestor_empleados.add_employee(emp_storage, emp1)
        gestor_empleados.add_employee(emp_storage, emp2)
        
        # Crear contratos
        c1 = Contract(id="c1", employee_id="e1", start_date="2024-01-01")
        c2 = Contract(id="c2", employee_id="e1", start_date="2025-01-01")
        c3 = Contract(id="c3", employee_id="e2", start_date="2024-06-01")
        gestor_contratos.add_contract(con_storage, c1)
        gestor_contratos.add_contract(con_storage, c2)
        gestor_contratos.add_contract(con_storage, c3)
        
        # Listar
        results = list_employees_with_contracts(emp_storage, con_storage)
        assert len(results) == 2
        
        emp1_result = next(r for r in results if r.employee.id == "e1")
        assert len(emp1_result.contracts) == 2
        
        emp2_result = next(r for r in results if r.employee.id == "e2")
        assert len(emp2_result.contracts) == 1
    finally:
        os.remove(emp_path)
        os.remove(con_path)


def test_get_expired_contracts():
    emp_storage, con_storage, emp_path, con_path = _make_storages()
    try:
        # Contrato vencido
        today = datetime.now()
        past_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        future_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")
        
        c1 = Contract(id="c1", employee_id="e1", start_date="2023-01-01", end_date=past_date)
        c2 = Contract(id="c2", employee_id="e2", start_date="2024-01-01", end_date=future_date)
        c3 = Contract(id="c3", employee_id="e3", start_date="2024-01-01")  # Sin fecha fin
        
        gestor_contratos.add_contract(con_storage, c1)
        gestor_contratos.add_contract(con_storage, c2)
        gestor_contratos.add_contract(con_storage, c3)
        
        expired = get_expired_contracts(con_storage)
        assert len(expired) == 1
        assert expired[0].id == "c1"
        
        # Con fecha de referencia específica
        ref_date = (today - timedelta(days=15)).strftime("%Y-%m-%d")
        expired2 = get_expired_contracts(con_storage, reference_date=ref_date)
        assert len(expired2) == 1
    finally:
        os.remove(emp_path)
        os.remove(con_path)


def test_get_employees_with_expired_contracts():
    emp_storage, con_storage, emp_path, con_path = _make_storages()
    try:
        # Crear empleados
        emp1 = Employee(id="e1", first_name="Juan", last_name="Perez")
        emp2 = Employee(id="e2", first_name="Maria", last_name="Gomez")
        gestor_empleados.add_employee(emp_storage, emp1)
        gestor_empleados.add_employee(emp_storage, emp2)
        
        # Crear contratos
        today = datetime.now()
        past_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        future_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")
        
        c1 = Contract(id="c1", employee_id="e1", start_date="2023-01-01", end_date=past_date)
        c2 = Contract(id="c2", employee_id="e1", start_date="2024-01-01", end_date=future_date)
        c3 = Contract(id="c3", employee_id="e2", start_date="2023-06-01", end_date=past_date)
        
        gestor_contratos.add_contract(con_storage, c1)
        gestor_contratos.add_contract(con_storage, c2)
        gestor_contratos.add_contract(con_storage, c3)
        
        # Obtener empleados con contratos vencidos
        results = get_employees_with_expired_contracts(emp_storage, con_storage)
        assert len(results) == 2  # Ambos empleados tienen contratos vencidos
        
        emp1_result = next(r for r in results if r.employee.id == "e1")
        assert len(emp1_result.contracts) == 1  # Solo el vencido
        assert emp1_result.contracts[0].id == "c1"
        
        emp2_result = next(r for r in results if r.employee.id == "e2")
        assert len(emp2_result.contracts) == 1
        assert emp2_result.contracts[0].id == "c3"
    finally:
        os.remove(emp_path)
        os.remove(con_path)


def test_get_contracts_by_employee():
    emp_storage, con_storage, emp_path, con_path = _make_storages()
    try:
        # Crear contratos
        c1 = Contract(id="c1", employee_id="e1", start_date="2024-01-01")
        c2 = Contract(id="c2", employee_id="e1", start_date="2025-01-01")
        c3 = Contract(id="c3", employee_id="e2", start_date="2024-06-01")
        
        gestor_contratos.add_contract(con_storage, c1)
        gestor_contratos.add_contract(con_storage, c2)
        gestor_contratos.add_contract(con_storage, c3)
        
        # Obtener contratos de e1
        contracts = get_contracts_by_employee(con_storage, "e1")
        assert len(contracts) == 2
        assert all(c.employee_id == "e1" for c in contracts)
        
        # Empleado sin contratos
        contracts2 = get_contracts_by_employee(con_storage, "e3")
        assert len(contracts2) == 0
    finally:
        os.remove(emp_path)
        os.remove(con_path)

