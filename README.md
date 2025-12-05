# Sistema Monte Carlo - Entrega mínima

Proyecto web en Python (Flask) con autenticación y módulo básico de Monte Carlo.

Características incluidas (mínimas, funcionales):
- Login / Logout (Flask-Login)
- CRUD de proyectos y variables de proyecto (modal de configuración)
- Ejecución de simulación Monte Carlo (Normal, Uniforme, Triangular)
- Guardado automático de reportes en la BD
- Listado de reportes, ver detalle, descargar PDF / DOCX
- Eliminación suave (soft-delete) y recuperación en 24h + job de limpieza cada hora

Requisitos
- Python 3.10+
- wkhtmltopdf (para pdfkit) — en Windows instale el ejecutable y asegúrese de que esté en PATH.

Instalación rápida

1. Crear entorno virtual e instalar dependencias:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Copiar `.env.example` a `.env` y ajustar si quiere. Por defecto la URL apunta a la proporcionada.

3. Inicializar la base de datos (opcional, la app puede crear tablas automáticamente):

```powershell
setx FLASK_APP app.py; setx FLASK_ENV development
python app.py --init-db
```

4. Ejecutar la app:

```powershell
python app.py
```

Notas
- Para generar PDF necesita wkhtmltopdf instalado. Si no lo instala, la descarga de PDF fallará; DOCX usa python-docx.
- Esta entrega crea una base funcional y puede mejorarse con tests, migraciones y validaciones adicionales.
