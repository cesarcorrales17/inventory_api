Estructura del Proyecto
inventory_api/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── products.py
│   │   │   ├── suppliers.py
│   │   │   ├── inventory.py
│   │   │   ├── auth.py
│   │   │   └── users.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── init_db.py
│   │   └── models/
│   │       ├── product.py
│   │       ├── supplier.py
│   │       ├── inventory.py
│   │       └── user.py
│   ├── schemas/
│   │   ├── product.py
│   │   ├── supplier.py
│   │   ├── inventory.py
│   │   └── user.py
│   ├── services/
│   │   ├── product_service.py
│   │   ├── supplier_service.py
│   │   ├── inventory_service.py
│   │   └── user_service.py
│   └── utils/
│       ├── pagination.py
│       └── hashing.py
│
├── alembic/
├── requirements.txt
└── README.md

📦 Explicación de Cada Carpeta y Archivo
🟦 app/

Es la raíz del backend. Contiene todo el código de la API.

🟩 main.py

Archivo principal donde:

Se inicializa FastAPI

Se registran los routers

Se levanta la aplicación

🟧 api/

Aquí viven las rutas del sistema (endpoints).

🟪 api/v1/

Permite versionar la API, ejemplo:

/api/v1/products

/api/v1/auth

etc.

Archivos dentro:

products.py

CRUD de productos.

suppliers.py

CRUD de proveedores.

inventory.py

Entradas, salidas y kardex.

auth.py

Login, JWT, autenticación.

users.py

Gestión de usuarios y roles.

🔵 core/

Configuraciones globales.

config.py

Variables de entorno y configuración general.

security.py

Generación de tokens JWT

Verificación de contraseñas

Autorizaciones

🔴 db/

Todo lo relacionado con la base de datos.

session.py

Conexión a PostgreSQL mediante SQLAlchemy.

base.py

Registro de modelos para Alembic.

init_db.py

Crear usuario admin o datos iniciales.

🔶 db/models/

Modelos de las tablas (ORM).

product.py

Modelo de productos.

supplier.py

Modelo de proveedores.

inventory.py

Movimientos de inventario.

user.py

Usuarios del sistema.

🟫 schemas/

Pydantic schemas para validar datos de entrada y salida.

Ejemplos:

ProductCreate

ProductOut

SupplierBase

InventoryMovement

UserAuth

🟩 services/

La lógica de negocio principal.

product_service.py

Lógica del módulo productos:

Crear

Editar

Eliminar

Paginación

Validación de stock

inventory_service.py

Entradas, salidas y kardex.

user_service.py

Login, creación de usuarios, hashing.

supplier_service.py

Lógica de proveedores.

👉 Las rutas solo llaman a los servicios.

🟦 utils/
pagination.py

Funciones para paginar resultados.

hashing.py

Hash de contraseñas con bcrypt.

🔷 alembic/

Sistema de migraciones:

Versiona cambios de la base de datos.

Genera archivos en /versions/.

📄 requirements.txt

Dependencias del proyecto:

fastapi
uvicorn
sqlalchemy
alembic
psycopg2-binary
python-jose
passlib[bcrypt]
python-dotenv

🚀 Cómo iniciar el proyecto
1️⃣ Instalar dependencias
pip install -r requirements.txt

2️⃣ Configurar variables de entorno

Crear un archivo .env:

DATABASE_URL=postgresql://user:password@localhost/inventorydb
SECRET_KEY=un_key_secreto_largo
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

3️⃣ Inicializar Alembic
alembic init alembic

4️⃣ Crear migración automática
alembic revision --autogenerate -m "Initial tables"

5️⃣ Aplicar migración
alembic upgrade head

6️⃣ Ejecutar el servidor
uvicorn app.main:app --reload

📌 Estado del Proyecto
✓ Backend profesional
✓ Arquitectura escalable
○ Frontend pendiente (lo puedes generar con IA si quieres)
🧑‍💻 Tecnologías utilizadas

