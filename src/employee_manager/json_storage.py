"""Esqueleto de almacenamiento basado en JSON.

Este módulo debe proporcionar una clase `JsonStorage` para operaciones CRUD sobre
archivos JSON. Por ahora solo contiene esqueletos y docstrings; implementaremos
los métodos punto por punto según lo vayamos definiendo.
"""
from pathlib import Path
from typing import Any, Dict, List
import json


class JsonStorage:
    """Gestor simple de lectura/escritura JSON.

    Métodos a implementar:
    - load_json
    - save_json
    - get_all
    - add
    - update
    - delete

    Mantener nombres en snake_case.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_json(self) -> Dict[str, Any]:
        """Cargar y retornar el diccionario con la clave 'empleados'.

        Retornar estructura con lista vacía si el archivo no existe o el JSON es inválido.
        """
        if not self.file_path.exists():
            return {"empleados": []}
        try:
            with self.file_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
                if isinstance(data, dict) and "empleados" in data:
                    return data
                # Si es una lista antigua, convertirla
                if isinstance(data, list):
                    return {"empleados": data}
                return {"empleados": []}
        except (json.JSONDecodeError, OSError):
            # En caso de JSON inválido o problemas de lectura, retornar estructura vacía
            return {"empleados": []}

    def save_json(self, data: Dict[str, Any]) -> None:
        """Guardar el diccionario con la clave 'empleados' en archivo JSON.

        Se asegura que la carpeta padre exista y escribe JSON con indentación.
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)


    def get_all(self) -> List[Dict[str, Any]]:
        """Retornar todos los empleados."""
        data = self.load_json()
        return data.get("empleados", [])

    def add(self, record: Dict[str, Any]) -> None:
        """Agregar un registro a la colección.
        
        Lanza ValueError si el registro ya existe (basado en el campo 'id').
        """
        data = self.load_json()
        empleados = data.get("empleados", [])
        record_id = record.get("id")
        if record_id and any(r.get("id") == record_id for r in empleados):
            raise ValueError(f"Registro con id '{record_id}' ya existe")
        empleados.append(record)
        data["empleados"] = empleados
        self.save_json(data)

    def update(self, record_id: int, updates: Dict[str, Any]) -> None:
        """Actualizar un registro por id.
        
        Lanza ValueError si el registro no existe.
        No permite cambiar el id del registro.
        """
        if "id" in updates and updates["id"] != record_id:
            raise ValueError("No se puede cambiar el id del registro")
        
        data = self.load_json()
        empleados = data.get("empleados", [])
        for i, rec in enumerate(empleados):
            if rec.get("id") == record_id:
                empleados[i] = {**rec, **updates}
                data["empleados"] = empleados
                self.save_json(data)
                return
        
        raise ValueError(f"Registro con id '{record_id}' no encontrado")

    def delete(self, record_id: int) -> None:
        """Eliminar un registro por id.
        
        Lanza ValueError si el registro no existe.
        """
        data = self.load_json()
        empleados = data.get("empleados", [])
        new_empleados = [r for r in empleados if r.get("id") != record_id]
        if len(new_empleados) == len(empleados):
            raise ValueError(f"Registro con id '{record_id}' no encontrado")
        data["empleados"] = new_empleados
        self.save_json(data)
