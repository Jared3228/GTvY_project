# Sistema de Gestión — GTyV

Aplicación web desarrollada en **Django** para la administración interna del Departamento de Gestión Tecnológica y Vinculación.  
Incluye módulos para documentos, convenios, constancias, pendientes y control de usuarios con permisos y roles.

---

##  Características principales

- Gestión de usuarios con roles (Jefe / Trabajador)
- Administración de convenios
- Control de documentos y constancias (con generación PDF)
- Sistema de pendientes y dashboard personal
- Interfaz moderna y modular
- Pensado para expandirse fácilmente

---

##  Requisitos

Asegúrate de tener instalado:

- **Python 3.10+**
- **Git**
- Opcional: un entorno virtual como `venv` o `uv`

---

## Instalación

### 1) Clonar el repositorio
```bash
git clone https://github.com/Jared3228/GTvY_project
cd GTvY_project
```
### 2) Crear entorno virtual

Windows
```bash
venv\Scripts\activate
```
Linux/macOS
```bash
source venv/bin/activate
```

### 3) Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## Base de datos

Usando sqlite3:
```bash
python manage.py migrate
```
Para crear un super usuario:
```bash
python manage.py createsuperuser
```

---

## Ejecutar el servidor
```bash
python manage.py runserver
```
El sistema estará disponible en:
```bash
http://127.0.0.1:8000/
```

---

## Estructura del proyecto
```bash
/GyV             → Carpeta principal del proyecto (settings, urls, wsgi)
/core            → Página de inicio y dashboard
/documentos      → Subida y previsualización de archivos PDF
/convenios       → Gestión de convenios
/reportes        → Generación de constancias en PDF
/pendientes      → Sistema de tareas asignadas
/accounts        → Roles, permisos y autenticación
/static          → Archivos CSS, JS e imágenes
/templates       → Plantillas HTML del sistema

```

---

## 📄 Tecnologías principales

- **Backend:** Python 3, Django 5, SQLite
- **Frontend:** HTML, CSS, diseño generado con Antigravity
- **Documentos PDF:** xhtml2pdf, ReportLab, PyPDF, Pillow
- **Soporte adicional:** lxml, Cairo, svglib, html5lib, tinycss2

---

## Notas importantes

- El diseño es un completo **CAOS**, recomiendo solo cambiar la paleta de colores y mucha paciencia.
- Es mi primer proyecto web.
- Puede haber funciones ignoradas o mal comentadas o que se puedan mejorar (especialmente que se puedan mejorar)
- Si quieres usar otra base de datos, ajusta la configuracion en settings.py
- El proyecto esta estructurado para facilitar agregar nuevos módulos.

---

## Licencia

Proyecto de uso académico.
Puedes modificarlo libremente para fines personales o educativos.
