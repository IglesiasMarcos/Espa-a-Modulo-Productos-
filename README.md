# Proyecto Grupo España

Pequeña aplicación Python/Tkinter para gestionar productos y usuarios.

Estructura mínima necesaria para ejecutar localmente:
- `main.py` (entrada)
- `login_register.py`, `productos_abm.py`, `ver_productos.py`, `registrar.py` (módulos de la app)
- `assets/` (imágenes)
- `productos.json`, `usuarios.json` (datos persistentes)

Instrucciones rápidas para desarrolladores (Windows):

1. Instalar Python 3.10+ desde https://www.python.org/ (marcar "Add Python to PATH").
2. Crear y activar un entorno virtual (opcional pero recomendado):

```powershell
python -m venv .\venv
.\venv\Scripts\Activate.ps1
```

3. Instalar la dependencia mínima (Pillow) si no la tienes:

```powershell
python -m pip install pillow
```

4. Ejecutar la app:

```powershell
python main.py
```

Cómo crear un repositorio remoto en GitHub (opciones):

- Opción A (recomendada si tienes `gh` CLI):
  1. `gh auth login` (inicia sesión)
  2. `gh repo create <nombre-del-repo> --public --source=. --remote=origin --push`

- Opción B (web):
  1. En GitHub, crea un nuevo repo vacío.
  2. En tu carpeta local ejecuta:

```powershell
git remote add origin https://github.com/<usuario>/<repo>.git
git branch -M main
git push -u origin main
```

Notas:
- No incluyas la carpeta `venv` ni los archivos temporales.
- Si quieres que prepare un script `build.ps1` para generar un `.exe` con PyInstaller, dímelo y lo añado.
