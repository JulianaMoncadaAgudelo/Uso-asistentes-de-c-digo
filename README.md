# Gestor de Empleados y Contratos

## Objetivo

Aplicación en Python para administrar un directorio de empleados y sus contratos laborales utilizando archivos JSON como almacenamiento de datos. La aplicación permite:

- ✅ Agregar, actualizar y eliminar empleados
- ✅ Registrar contratos laborales asociados a los empleados
- ✅ Consultar información de empleados y sus contratos
- ✅ Generar reportes básicos (empleados con contratos vencidos)
- ✅ Guardar y recuperar información de archivos JSON
- ✅ Pruebas unitarias sobre las funcionalidades clave

## Estructura del Proyecto

```
.
├── src/
│   └── employee_manager/
│       ├── __init__.py
│       ├── models.py              # Modelos de datos (Employee, Contract)
│       ├── json_storage.py         # Gestor de almacenamiento JSON
│       ├── gestor_empleados.py     # CRUD de empleados
│       ├── gestor_contratos.py     # CRUD de contratos
│       ├── reportes.py              # Reportes y consultas
│       ├── main.py                 # Interfaz CLI principal
│       └── cli.py                  # CLI alternativa (legacy)
├── tests/                          # Pruebas unitarias
│   ├── test_models.py
│   ├── test_json_storage.py
│   ├── test_gestor_empleados.py
│   ├── test_gestor_contratos.py
│   ├── test_reportes.py
│   ├── test_main_cli.py
│   └── test_main_menu.py
├── requirements.txt
└── README.md
```

## Convenciones

- **Nombres en snake_case** para variables, funciones y métodos
- Código organizado en módulos modulares y reutilizables
- Validaciones de datos (fechas, existencia de empleados, etc.)
- Manejo de errores con excepciones descriptivas

## Instalación

1. Crear y activar el entorno virtual (Windows PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   .venv\Scripts\python.exe -m pip install --upgrade pip
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

2. Alternativa (si ya tienes el entorno creado): activa el `.venv` y ejecuta `pip install -r requirements.txt`.

## Uso

### Menú Interactivo

La forma más sencilla de usar la aplicación es mediante el menú interactivo:

```powershell
.venv\Scripts\python -m employee_manager.main menu
```

El menú ofrece las siguientes opciones:

1. Agregar empleado
2. Listar empleados
3. Actualizar empleado
4. Eliminar empleado
5. Agregar contrato
6. Listar contratos
7. Actualizar contrato
8. Eliminar contrato
9. Consultar empleado con contratos
10. Reporte: Contratos vencidos
11. Reporte: Empleados con contratos vencidos
12. Inicializar base (reset)
13. Salir

### Comandos CLI

También puedes usar comandos individuales:

**Inicializar base de datos:**

```powershell
.venv\Scripts\python -m employee_manager.main init-db
```

**Listar empleados:**

```powershell
.venv\Scripts\python -m employee_manager.main list-employees
```

**Listar contratos:**

```powershell
.venv\Scripts\python -m employee_manager.main list-contracts
```

## Funcionalidades

### Gestión de Empleados

- **Agregar empleado**: Crea un nuevo empleado con ID, nombre, apellido y email (opcional)
- **Listar empleados**: Muestra todos los empleados en formato tabla
- **Actualizar empleado**: Modifica campos de un empleado existente
- **Eliminar empleado**: Elimina un empleado del sistema

### Gestión de Contratos

- **Agregar contrato**: Crea un contrato asociado a un empleado con validaciones:
  - Verifica que el empleado exista
  - Valida formato de fechas (YYYY-MM-DD)
  - Verifica que la fecha de fin sea posterior a la fecha de inicio
- **Listar contratos**: Muestra todos los contratos
- **Actualizar contrato**: Modifica campos de un contrato
- **Eliminar contrato**: Elimina un contrato

### Consultas y Reportes

- **Consultar empleado con contratos**: Muestra un empleado específico con todos sus contratos asociados
- **Reporte de contratos vencidos**: Lista todos los contratos cuya fecha de fin ha pasado
- **Reporte de empleados con contratos vencidos**: Muestra empleados que tienen al menos un contrato vencido

## Validaciones Implementadas

- ✅ Formato de fechas (YYYY-MM-DD)
- ✅ Fecha de fin posterior a fecha de inicio
- ✅ Empleado existe antes de crear contrato
- ✅ No duplicar IDs de empleados o contratos
- ✅ No cambiar IDs de registros existentes

## Pruebas

Ejecutar todas las pruebas:

```powershell
.venv\Scripts\python -m pytest tests/ -v
```

Ejecutar pruebas específicas:

```powershell
.venv\Scripts\python -m pytest tests/test_reportes.py -v
```

## Almacenamiento

Los datos se guardan en archivos JSON en el directorio `data/`:

- `data/empleados.json`: Lista de empleados
- `data/contratos.json`: Lista de contratos

Los archivos se crean automáticamente al usar la aplicación.
