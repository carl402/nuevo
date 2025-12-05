# Sistema Monte Carlo - Aplicación Web

Proyecto web en Python (Flask) con autenticación y módulo completo de Monte Carlo.

## Características
- Login / Logout (Flask-Login)
- Gestión completa de usuarios (crear, editar, cambiar contraseña, eliminar)
- CRUD de proyectos y variables de proyecto
- Ejecución de simulación Monte Carlo (Normal, Uniforme, Triangular)
- Guardado automático de reportes en la BD
- Listado de reportes, ver detalle, descargar PDF / DOCX
- Eliminación suave (soft-delete) y recuperación en 24h + job de limpieza cada hora

## Requisitos
- Python 3.10+
- PostgreSQL (Supabase)
- wkhtmltopdf (para pdfkit)

## Instalación Local

1. Crear entorno virtual e instalar dependencias:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

3. Ejecutar la aplicación:
```bash
python app.py
```

## Deploy en Render

1. Conectar repositorio de GitHub a Render
2. Configurar variables de entorno:
   - `DATABASE_URL`: URL de conexión a PostgreSQL
   - `SECRET_KEY`: Clave secreta para Flask
3. Render detectará automáticamente el `render.yaml` y `Procfile`
4. La aplicación se desplegará automáticamente

## Base de Datos

La aplicación está configurada para usar la base de datos PostgreSQL existente en Supabase con las siguientes tablas:
- `users`: Gestión de usuarios
- `projects`: Proyectos de simulación
- `project_variables`: Variables de cada proyecto
- `reports`: Reportes generados
- `simulation_results`: Resultados de las simulaciones

## Usuarios por Defecto

La base de datos incluye usuarios de prueba:
- admin@montecarlo.com / admin123 (Administrador)
- analyst@montecarlo.com / analyst123 (Analista)
- carlos@montecarlo.com / carlos2024 (Usuario)

## Notas
- Para generar PDF necesita wkhtmltopdf instalado
- En producción, el scheduler de limpieza se ejecuta automáticamente
- La aplicación está optimizada para deploy en Render
