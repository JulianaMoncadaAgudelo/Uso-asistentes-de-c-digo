# Instrucciones para Subir el Proyecto a GitHub

## ✅ Paso 1: Verificar que Git está configurado

Si es la primera vez que usas Git en esta computadora, configura tu nombre y email:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

## ✅ Paso 2: Crear el repositorio en GitHub

1. Ve a [GitHub](https://github.com) e inicia sesión
2. Haz clic en el botón **"+"** (arriba a la derecha) y selecciona **"New repository"**
3. Completa los datos:
   - **Repository name**: `actmod2_nombre_apellido` (o el nombre que prefieras)
   - **Description**: "Sistema de gestor de empleados y contratos - Actividad Individual 1"
   - **Visibility**: Elige **Public** o **Private**
   - **NO marques** "Initialize this repository with a README" (ya tenemos uno)
   - **NO agregues** .gitignore ni licencia (ya están incluidos)
4. Haz clic en **"Create repository"**

## ✅ Paso 3: Conectar tu repositorio local con GitHub

GitHub te mostrará instrucciones. Usa estas comandos (reemplaza `TU_USUARIO` y `NOMBRE_REPO` con tus datos):

```powershell
# Asegúrate de estar en el directorio del proyecto
cd "c:\Users\User\Documents\Diplomado IA UNIR\IA\Actividad_Individual_1"

# Agrega el repositorio remoto (reemplaza con tu URL)
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git

# Verifica que se agregó correctamente
git remote -v
```

**Ejemplo:**
Si tu usuario es `juanperez` y el repositorio se llama `actmod2_juan_perez`:
```powershell
git remote add origin https://github.com/juanperez/actmod2_juan_perez.git
```

## ✅ Paso 4: Subir el código a GitHub

```powershell
# Cambia a la rama main (si es necesario)
git branch -M main

# Sube el código
git push -u origin main
```

Si te pide autenticación:
- **GitHub ya no acepta contraseñas**, necesitas un **Personal Access Token (PAT)**
- Ve a: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Genera un nuevo token con permisos `repo`
- Úsalo como contraseña cuando Git te la pida

## ✅ Paso 5: Verificar

Ve a tu repositorio en GitHub y verifica que todos los archivos se subieron correctamente.

---

## 🔄 Comandos útiles para futuras actualizaciones

### Agregar cambios y subirlos:

```powershell
# Ver qué archivos cambiaron
git status

# Agregar todos los cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir a GitHub
git push
```

### Ver el historial de commits:

```powershell
git log --oneline
```

### Ver diferencias antes de hacer commit:

```powershell
git diff
```

---

## 📝 Nota sobre el archivo act1.docx

El archivo `act1.docx` está incluido en el repositorio. Si prefieres no subirlo (porque es grande o contiene información sensible), puedes eliminarlo del seguimiento:

```powershell
git rm --cached act1.docx
echo "act1.docx" >> .gitignore
git commit -m "Remover act1.docx del repositorio"
git push
```

---

## 🆘 Solución de Problemas

### Error: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git
```

### Error: "failed to push some refs"
```powershell
# Si GitHub tiene archivos que no tienes localmente
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Cambiar la URL del repositorio remoto
```powershell
git remote set-url origin https://github.com/TU_USUARIO/NUEVO_REPO.git
```

---

## ✨ ¡Listo!

Una vez subido, puedes compartir el enlace de tu repositorio. El formato será:
```
https://github.com/TU_USUARIO/NOMBRE_REPO
```
