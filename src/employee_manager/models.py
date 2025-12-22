"""Modelos de datos para empleados y contratos.

Mantener nombres en snake_case para atributos y métodos.
"""
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Employee:
    """Representa a un empleado.

    Campos básicos según especificación: id, nombre, cargo.
    Los contratos se almacenan dentro del empleado.
    """

    id: int
    nombre: str
    cargo: str
    contratos: List['Contract'] = field(default_factory=list)


@dataclass
class Contract:
    """Representa un contrato laboral asociado a un empleado."""

    id_contrato: int
    fecha_inicio: str  # fecha ISO YYYY-MM-DD
    fecha_fin: str  # fecha ISO YYYY-MM-DD
    salario: float
