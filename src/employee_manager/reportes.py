"""Módulo para generar reportes y consultas sobre empleados y contratos.

Funciones para consultar información combinada de empleados y contratos,
y generar reportes como contratos vencidos.
"""
from datetime import datetime
from typing import List, Optional, Dict

from .json_storage import JsonStorage
from .gestor_empleados import buscar_empleado, listar_empleados
from .gestor_contratos import listar_contratos_vencidos


def obtener_empleado_con_contratos(
    storage: JsonStorage,
    id_empleado: int
) -> Optional[Dict]:
    """Obtener un empleado con todos sus contratos asociados.
    
    Args:
        storage: Storage de empleados
        id_empleado: ID del empleado a consultar
        
    Returns:
        Dict con el empleado y sus contratos si existe, None en caso contrario
    """
    empleado = buscar_empleado(id_empleado, storage)
    return empleado


def obtener_empleados_con_contratos_vencidos(
    storage: JsonStorage,
    fecha_referencia: Optional[str] = None
) -> List[Dict]:
    """Obtener empleados que tienen contratos vencidos.
    
    Args:
        storage: Storage de empleados
        fecha_referencia: Fecha de referencia en formato YYYY-MM-DD.
                        Si es None, usa la fecha actual.
        
    Returns:
        Lista de diccionarios con empleados que tienen contratos vencidos
    """
    contratos_vencidos = listar_contratos_vencidos(storage, fecha_referencia)
    
    # Agrupar por empleado
    empleados_dict = {}
    for contrato in contratos_vencidos:
        id_emp = contrato.get("id_empleado")
        if id_emp not in empleados_dict:
            empleado = buscar_empleado(id_emp, storage)
            if empleado:
                empleados_dict[id_emp] = {
                    "empleado": empleado,
                    "contratos_vencidos": []
                }
        if id_emp in empleados_dict:
            empleados_dict[id_emp]["contratos_vencidos"].append(contrato)
    
    return list(empleados_dict.values())
