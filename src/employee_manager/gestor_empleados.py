"""Gestor de empleados.

Implementación según especificación:
- agregar_empleado(nombre, cargo) → dict
- eliminar_empleado(id) → bool
- buscar_empleado(id) → dict
"""
from typing import Dict, Optional
from datetime import datetime

from .json_storage import JsonStorage


def _get_next_id(storage: JsonStorage) -> int:
    """Obtener el siguiente ID disponible para un empleado."""
    empleados = storage.get_all()
    if not empleados:
        return 1
    max_id = max((emp.get("id", 0) for emp in empleados), default=0)
    return max_id + 1


def agregar_empleado(nombre: str, cargo: str, storage: JsonStorage) -> Dict:
    """Agregar un nuevo empleado.
    
    Args:
        nombre: Nombre del empleado
        cargo: Cargo del empleado
        storage: Storage de empleados
        
    Returns:
        Dict con los datos del empleado agregado
        
    Lanza ValueError si los datos son inválidos.
    """
    if not nombre or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío")
    if not cargo or not cargo.strip():
        raise ValueError("El cargo no puede estar vacío")
    
    empleado_id = _get_next_id(storage)
    empleado = {
        "id": empleado_id,
        "nombre": nombre.strip(),
        "cargo": cargo.strip(),
        "contratos": []
    }
    
    storage.add(empleado)
    return empleado


def eliminar_empleado(id: int, storage: JsonStorage) -> bool:
    """Eliminar un empleado por id.
    
    Args:
        id: ID del empleado a eliminar
        storage: Storage de empleados
        
    Returns:
        True si se eliminó correctamente, False si no se encontró
    """
    try:
        storage.delete(id)
        return True
    except ValueError:
        return False


def buscar_empleado(id: int, storage: JsonStorage) -> Optional[Dict]:
    """Buscar un empleado por id.
    
    Args:
        id: ID del empleado a buscar
        storage: Storage de empleados
        
    Returns:
        Dict con los datos del empleado si existe, None en caso contrario
    """
    empleados = storage.get_all()
    for emp in empleados:
        if emp.get("id") == id:
            return emp
    return None


def listar_empleados(storage: JsonStorage) -> list:
    """Listar todos los empleados.
    
    Args:
        storage: Storage de empleados
        
    Returns:
        Lista de diccionarios con los datos de los empleados
    """
    return storage.get_all()
