# Guía de Prueba Manual - Gestor de Empleados y Contratos

## 🚀 Inicio Rápido

### Paso 1: Abrir la terminal

Abre PowerShell o CMD y navega al directorio del proyecto:

```powershell
cd "c:\Users\User\Documents\Diplomado IA UNIR\IA\Actividad_Individual_1"
```

### Paso 2: Ejecutar el menú interactivo

```powershell
python -m src.employee_manager.main menu
```

---

## 📋 Menú de Opciones

Cuando ejecutes el comando, verás un menú con las siguientes opciones:

```
Gestor de Empleados y Contratos - Menú
1) Agregar empleado
2) Listar empleados
3) Buscar empleado
4) Eliminar empleado
5) Asociar contrato a empleado
6) Listar contratos vencidos
7) Inicializar base (reset)
0) Salir
```

---

## 🧪 Escenario de Prueba Recomendado

### Prueba 1: Agregar empleados

1. Selecciona opción **1** (Agregar empleado)
2. Ingresa los datos:
   - Nombre: `Carlos Pérez`
   - Cargo: `Desarrollador`
3. Verás un mensaje de confirmación

Repite para agregar otro empleado:

- Nombre: `María García`
- Cargo: `Diseñadora`

### Prueba 2: Listar empleados

1. Selecciona opción **2** (Listar empleados)
2. Verás una tabla con todos los empleados agregados

### Prueba 3: Buscar un empleado

1. Selecciona opción **3** (Buscar empleado)
2. Ingresa el ID: `1`
3. Verás la información del empleado y sus contratos (si tiene)

### Prueba 4: Asociar un contrato

1. Selecciona opción **5** (Asociar contrato a empleado)
2. Ingresa los datos:
   - ID del empleado: `1`
   - Fecha inicio: `2023-02-15`
   - Fecha fin: `2024-02-15`
   - Salario: `3500`
3. Verás un mensaje de confirmación

### Prueba 5: Ver contratos del empleado

1. Selecciona opción **3** (Buscar empleado)
2. Ingresa el ID: `1`
3. Ahora verás el empleado con su contrato asociado

### Prueba 6: Agregar un contrato vencido

1. Selecciona opción **5** (Asociar contrato)
2. Ingresa los datos:
   - ID del empleado: `2`
   - Fecha inicio: `2022-01-01`
   - Fecha fin: `2022-12-31` (esta fecha ya pasó, por lo que está vencido)
   - Salario: `3000`

### Prueba 7: Listar contratos vencidos

1. Selecciona opción **6** (Listar contratos vencidos)
2. Verás una tabla con todos los contratos que ya vencieron

### Prueba 8: Eliminar un empleado

1. Selecciona opción **4** (Eliminar empleado)
2. Ingresa el ID: `2`
3. Confirma la eliminación escribiendo `y` o `yes`
4. Verifica que se eliminó listando los empleados (opción 2)

### Prueba 9: Reiniciar la base de datos

1. Selecciona opción **7** (Inicializar base)
2. Esto borrará todos los datos y creará un archivo JSON vacío
3. Verifica listando empleados (opción 2) - debería estar vacío

### Prueba 10: Salir

1. Selecciona opción **0** (Salir)
2. El programa terminará

---

## 🔍 Verificar el Archivo JSON

Después de hacer algunas pruebas, puedes ver el archivo JSON generado:

```powershell
Get-Content data\empleados.json
```

O con formato bonito:

```powershell
Get-Content data\empleados.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## ⚠️ Pruebas de Validación

### Validar que no se pueden agregar empleados duplicados

- Intenta agregar un empleado con el mismo nombre (debería funcionar, los IDs son únicos)

### Validar formato de fechas

- Intenta agregar un contrato con fecha inválida: `2023/02/15` (debería dar error)
- Intenta agregar un contrato donde fecha fin < fecha inicio (debería dar error)

### Validar que el empleado existe antes de agregar contrato

- Intenta agregar un contrato a un empleado que no existe (ID: 999) (debería dar error)

---

## 📝 Notas

- Los IDs de empleados se generan automáticamente (1, 2, 3...)
- Los IDs de contratos empiezan en 101 y se incrementan automáticamente
- El formato de fechas debe ser: `YYYY-MM-DD` (ejemplo: `2023-02-15`)
- Los datos se guardan automáticamente en `data/empleados.json`

---

## 🆘 Solución de Problemas

### Error: "No module named 'click'"

```powershell
pip install -r requirements.txt
```

### Error: "No se puede encontrar el módulo"

Asegúrate de estar en el directorio correcto:

```powershell
cd "c:\Users\User\Documents\Diplomado IA UNIR\IA\Actividad_Individual_1"
```

### El menú no aparece

Verifica que ejecutaste el comando correcto:

```powershell
python -m src.employee_manager.main menu
```
