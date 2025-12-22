"""Pruebas (esqueleto) para los modelos."""
from employee_manager.models import Employee, Contract


def test_create_employee():
    employee = Employee(id="e1", first_name="Juan", last_name="Perez")
    assert employee.id == "e1"
    assert employee.first_name == "Juan"


def test_create_contract():
    contract = Contract(id="c1", employee_id="e1", start_date="2025-01-01")
    assert contract.employee_id == "e1"
    assert contract.start_date == "2025-01-01"
