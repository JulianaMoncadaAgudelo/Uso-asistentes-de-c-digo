"""Script rápido para probar las funcionalidades principales."""
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from employee_manager.json_storage import JsonStorage
from employee_manager.gestor_empleados import agregar_empleado, buscar_empleado, eliminar_empleado, listar_empleados
from employee_manager.gestor_contratos import asociar_contrato, listar_contratos_vencidos
import json

# Archivo de prueba
test_file = "test_revision.json"
storage = JsonStorage(test_file)

print("=" * 60)
print("PRUEBA RÁPIDA DEL GESTOR DE EMPLEADOS Y CONTRATOS")
print("=" * 60)

try:
    # 1. Agregar empleado
    print("\n1. Agregando empleado...")
    emp1 = agregar_empleado("Carlos Pérez", "Desarrollador", storage)
    print(f"   [OK] Empleado agregado: {emp1['nombre']} (ID: {emp1['id']})")
    
    # 2. Buscar empleado
    print("\n2. Buscando empleado...")
    encontrado = buscar_empleado(1, storage)
    if encontrado:
        print(f"   [OK] Empleado encontrado: {encontrado['nombre']} - {encontrado['cargo']}")
    
    # 3. Agregar otro empleado
    print("\n3. Agregando otro empleado...")
    emp2 = agregar_empleado("María García", "Diseñadora", storage)
    print(f"   [OK] Empleado agregado: {emp2['nombre']} (ID: {emp2['id']})")
    
    # 4. Listar empleados
    print("\n4. Listando todos los empleados...")
    empleados = listar_empleados(storage)
    print(f"   [OK] Total de empleados: {len(empleados)}")
    for emp in empleados:
        print(f"      - {emp['nombre']} ({emp['cargo']})")
    
    # 5. Asociar contrato
    print("\n5. Asociando contrato a empleado...")
    contrato1 = asociar_contrato(1, "2023-02-15", "2024-02-15", 3500, storage)
    print(f"   [OK] Contrato {contrato1['id_contrato']} asociado al empleado 1")
    
    # 6. Verificar estructura JSON
    print("\n6. Verificando estructura JSON...")
    data = storage.load_json()
    print("   Estructura del JSON:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # 7. Buscar empleado con contratos
    print("\n7. Buscando empleado con contratos...")
    emp_con_contratos = buscar_empleado(1, storage)
    if emp_con_contratos:
        print(f"   [OK] Empleado: {emp_con_contratos['nombre']}")
        print(f"   [OK] Contratos: {len(emp_con_contratos['contratos'])}")
        for c in emp_con_contratos['contratos']:
            print(f"      - Contrato {c['id_contrato']}: {c['fecha_inicio']} a {c['fecha_fin']}")
    
    # 8. Agregar contrato vencido
    print("\n8. Agregando contrato vencido...")
    contrato2 = asociar_contrato(2, "2022-01-01", "2022-12-31", 3000, storage)
    print(f"   [OK] Contrato {contrato2['id_contrato']} agregado (vencido)")
    
    # 9. Listar contratos vencidos
    print("\n9. Listando contratos vencidos...")
    vencidos = listar_contratos_vencidos(storage)
    print(f"   [OK] Contratos vencidos encontrados: {len(vencidos)}")
    for c in vencidos:
        print(f"      - Contrato {c['id_contrato']} del empleado {c['id_empleado']} ({c['nombre_empleado']})")
    
    print("\n" + "=" * 60)
    print("[OK] TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
finally:
    # Limpiar archivo de prueba
    if Path(test_file).exists():
        Path(test_file).unlink()
        print(f"\nArchivo de prueba '{test_file}' eliminado.")
