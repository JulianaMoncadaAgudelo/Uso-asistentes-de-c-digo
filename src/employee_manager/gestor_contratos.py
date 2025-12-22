"""Gestor de contratos.

Implementación según especificación:
- asociar_contrato(id_empleado, fecha_inicio, fecha_fin, salario) → dict
- listar_contratos_vencidos() → list
"""
from typing import Dict, List
from datetime import datetime

from .json_storage import JsonStorage
from .gestor_empleados import buscar_empleado


def _get_next_contract_id(empleado: Dict) -> int:
    """Obtener el siguiente ID de contrato para un empleado."""
    contratos = empleado.get("contratos", [])
    if not contratos:
        return 101  # Empezar desde 101 como en el ejemplo
    max_id = max((c.get("id_contrato", 0) for c in contratos), default=100)
    return max_id + 1


def _validate_date_format(date_str: str, field_name: str = "fecha") -> None:
    """Validar que una fecha esté en formato YYYY-MM-DD.
    
    Lanza ValueError si el formato es inválido.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} debe estar en formato YYYY-MM-DD")


def asociar_contrato(
    id_empleado: int,
    fecha_inicio: str,
    fecha_fin: str,
    salario: float,
    storage: JsonStorage
) -> Dict:
    """Asociar un contrato a un empleado.
    
    Args:
        id_empleado: ID del empleado
        fecha_inicio: Fecha de inicio del contrato (YYYY-MM-DD)
        fecha_fin: Fecha de fin del contrato (YYYY-MM-DD)
        salario: Salario del contrato
        storage: Storage de empleados
        
    Returns:
        Dict con los datos del contrato asociado
        
    Lanza ValueError si:
    - El empleado no existe
    - Las fechas tienen formato inválido
    - La fecha de fin es anterior a la fecha de inicio
    - El salario es negativo
    """
    # Validar que el empleado existe
    empleado = buscar_empleado(id_empleado, storage)
    if empleado is None:
        raise ValueError(f"Empleado con id '{id_empleado}' no existe")
    
    # Validar formato de fechas
    _validate_date_format(fecha_inicio, "Fecha de inicio")
    _validate_date_format(fecha_fin, "Fecha de fin")
    
    # Validar que fecha_fin sea posterior a fecha_inicio
    inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
    if fin_dt < inicio_dt:
        raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
    
    # Validar salario
    if salario < 0:
        raise ValueError("El salario no puede ser negativo")
    
    # Crear el contrato
    id_contrato = _get_next_contract_id(empleado)
    contrato = {
        "id_contrato": id_contrato,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "salario": salario
    }
    
    # Agregar el contrato al empleado
    contratos = empleado.get("contratos", [])
    contratos.append(contrato)
    
    # Actualizar solo el campo contratos del empleado en el storage
    storage.update(id_empleado, {"contratos": contratos})
    
    return contrato


def listar_contratos_vencidos(storage: JsonStorage, fecha_referencia: str = None) -> List[Dict]:
    """Listar todos los contratos vencidos.
    
    Un contrato se considera vencido si su fecha_fin es anterior a la fecha de referencia
    (o a la fecha actual si no se especifica).
    
    Args:
        storage: Storage de empleados
        fecha_referencia: Fecha de referencia en formato YYYY-MM-DD (opcional)
        
    Returns:
        Lista de diccionarios con los contratos vencidos
    """
    if fecha_referencia is None:
        ref_date = datetime.now()
    else:
        try:
            ref_date = datetime.strptime(fecha_referencia, "%Y-%m-%d")
        except (ValueError, TypeError):
            return []  # Fecha inválida, retornar lista vacía
    
    empleados = storage.get_all()
    contratos_vencidos = []
    
    for empleado in empleados:
        contratos = empleado.get("contratos", [])
        for contrato in contratos:
            fecha_fin_str = contrato.get("fecha_fin")
            if fecha_fin_str:
                try:
                    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
                    if fecha_fin < ref_date:
                        # Incluir información del empleado en el contrato vencido
                        contrato_vencido = {
                            **contrato,
                            "id_empleado": empleado.get("id"),
                            "nombre_empleado": empleado.get("nombre"),
                            "cargo_empleado": empleado.get("cargo")
                        }
                        contratos_vencidos.append(contrato_vencido)
                except (ValueError, TypeError):
                    continue  # Ignorar fechas inválidas
    
    return contratos_vencidos
