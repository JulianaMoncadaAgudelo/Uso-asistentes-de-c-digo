"""Pruebas para JsonStorage."""
from employee_manager.json_storage import JsonStorage
import tempfile
import os
import json
import pytest


def test_json_storage_has_methods():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    path = temp_file.name
    temp_file.close()

    storage = JsonStorage(path)
    assert hasattr(storage, "load_json")
    assert hasattr(storage, "save_json")
    assert hasattr(storage, "add")
    assert hasattr(storage, "update")
    assert hasattr(storage, "delete")

    os.remove(path)


def test_load_json_empty_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    path = temp_file.name
    temp_file.close()

    storage = JsonStorage(path)
    data = storage.load_json()
    assert data == []

    os.remove(path)


def test_load_json_nonexistent_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    path = temp_file.name
    os.remove(path)

    storage = JsonStorage(path)
    data = storage.load_json()
    assert data == []


def test_save_and_load_json():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    path = temp_file.name
    temp_file.close()

    try:
        storage = JsonStorage(path)
        test_data = [{"id": "1", "name": "Test"}]
        storage.save_json(test_data)
        
        loaded = storage.load_json()
        assert loaded == test_data
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_add_record():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    path = temp_file.name
    temp_file.close()

    try:
        storage = JsonStorage(path)
        record = {"id": "r1", "name": "Record 1"}
        storage.add(record)
        
        data = storage.load_json()
        assert len(data) == 1
        assert data[0]["id"] == "r1"
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_add_duplicate_raises():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    path = temp_file.name
    temp_file.close()

    try:
        storage = JsonStorage(path)
        record = {"id": "r1", "name": "Record 1"}
        storage.add(record)
        
        with pytest.raises(ValueError, match="ya existe"):
            storage.add(record)
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_update_record():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    path = temp_file.name
    temp_file.close()

    try:
        storage = JsonStorage(path)
        record = {"id": "r1", "name": "Record 1", "value": 10}
        storage.add(record)
        
        storage.update("r1", {"value": 20})
        data = storage.load_json()
        assert data[0]["value"] == 20
        assert data[0]["name"] == "Record 1"  # No cambió
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_update_nonexistent_raises():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    path = temp_file.name
    temp_file.close()

    try:
        storage = JsonStorage(path)
        with pytest.raises(ValueError, match="no encontrado"):
            storage.update("nonexistent", {"name": "Test"})
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_update_cannot_change_id():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    path = temp_file.name
    temp_file.close()

    try:
        storage = JsonStorage(path)
        record = {"id": "r1", "name": "Record 1"}
        storage.add(record)
        
        with pytest.raises(ValueError, match="No se puede cambiar el id"):
            storage.update("r1", {"id": "r2"})
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_delete_record():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    path = temp_file.name
    temp_file.close()

    try:
        storage = JsonStorage(path)
        storage.add({"id": "r1", "name": "Record 1"})
        storage.add({"id": "r2", "name": "Record 2"})
        
        storage.delete("r1")
        data = storage.load_json()
        assert len(data) == 1
        assert data[0]["id"] == "r2"
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_delete_nonexistent_raises():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    path = temp_file.name
    temp_file.close()

    try:
        storage = JsonStorage(path)
        with pytest.raises(ValueError, match="no encontrado"):
            storage.delete("nonexistent")
    finally:
        if os.path.exists(path):
            os.remove(path)
