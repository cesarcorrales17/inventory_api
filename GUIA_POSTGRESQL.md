# 🐘 Guía Completa: Integración con PostgreSQL

## 📋 Índice
1. [Instalación de PostgreSQL](#1-instalación-de-postgresql)
2. [Configuración de la Base de Datos](#2-configuración-de-la-base-de-datos)
3. [Actualizar el Backend](#3-actualizar-el-backend)
4. [Migraciones con Alembic](#4-migraciones-con-alembic)
5. [Testing y Troubleshooting](#5-testing-y-troubleshooting)

---

## 1. Instalación de PostgreSQL

### Windows
1. Descarga PostgreSQL desde: https://www.postgresql.org/download/windows/
2. Ejecuta el instalador
3. Configura:
   - Puerto: `5432` (default)
   - Usuario: `postgres`
   - Contraseña: la que elijas (guárdala bien)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS
```bash
brew install postgresql
brew services start postgresql
```

---

## 2. Configuración de la Base de Datos

### Paso 1: Acceder a PostgreSQL

```bash
# Linux/Mac
sudo -u postgres psql

# Windows (desde cmd como administrador)
psql -U postgres
```

### Paso 2: Crear la Base de Datos

```sql
-- Crear base de datos
CREATE DATABASE inventorydb;

-- Crear usuario (opcional, puedes usar postgres)
CREATE USER inventory_user WITH PASSWORD 'tu_password_segura';

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE inventorydb TO inventory_user;

-- Salir
\q
```

### Paso 3: Verificar Conexión

```bash
psql -U postgres -d inventorydb -h localhost
```

---

## 3. Actualizar el Backend

### 3.1 Crear archivo `.env`

**Ruta:** `backend/.env`

```env
# Database
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password_aqui
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=inventorydb

# Security
SECRET_KEY=tu_clave_secreta_super_larga_y_segura_aqui_123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3.2 Actualizar `backend/app/core/config.py`

```python
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Inventory Management API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

### 3.3 Crear `backend/app/db/base.py`

```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

### 3.4 Actualizar `backend/app/db/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Cambiar a False en producción
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Dependency para usar en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3.5 Crear Modelos SQLAlchemy

**Archivo:** `backend/app/db/models/inventory.py`

```python
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False, default=0.0)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<InventoryItem(id={self.id}, name='{self.name}', quantity={self.quantity})>"
```

**Archivo:** `backend/app/db/models/user.py`

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
```

**Archivo:** `backend/app/db/models/__init__.py`

```python
from app.db.base import Base
from app.db.models.inventory import InventoryItem
from app.db.models.user import User

__all__ = ["Base", "InventoryItem", "User"]
```

### 3.6 Actualizar Servicio de Inventario

**Archivo:** `backend/app/services/inventory_service.py`

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.inventory import InventoryItem as InventoryItemModel
from app.schemas.inventory_schema import InventoryItem, InventoryItemCreate


class InventoryService:
    def list_items(self, db: Session) -> List[InventoryItem]:
        """Return all inventory items"""
        items = db.query(InventoryItemModel).all()
        return items
    
    def get_item(self, db: Session, item_id: int) -> Optional[InventoryItem]:
        """Get a specific item by ID"""
        return db.query(InventoryItemModel).filter(
            InventoryItemModel.id == item_id
        ).first()
    
    def create_item(self, db: Session, data: InventoryItemCreate) -> InventoryItem:
        """Create a new inventory item"""
        db_item = InventoryItemModel(
            name=data.name,
            quantity=data.quantity,
            price=data.price,
            description=data.description
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def update_item(
        self, 
        db: Session, 
        item_id: int, 
        data: InventoryItemCreate
    ) -> Optional[InventoryItem]:
        """Update an existing item"""
        db_item = self.get_item(db, item_id)
        if not db_item:
            return None
        
        db_item.name = data.name
        db_item.quantity = data.quantity
        db_item.price = data.price
        db_item.description = data.description
        
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def delete_item(self, db: Session, item_id: int) -> bool:
        """Delete an item"""
        db_item = self.get_item(db, item_id)
        if not db_item:
            return False
        
        db.delete(db_item)
        db.commit()
        return True
```

### 3.7 Actualizar Router de Inventario

**Archivo:** `backend/app/api/v1/routers/inventory.py`

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.inventory_schema import InventoryItem, InventoryItemCreate
from app.services.inventory_service import InventoryService
from app.utils.auth import get_current_user
from app.db.database import get_db

router = APIRouter()
service = InventoryService()


@router.get("/", response_model=List[InventoryItem])
def list_inventory(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get all inventory items"""
    return service.list_items(db)


@router.get("/{item_id}", response_model=InventoryItem)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get a specific inventory item by ID"""
    item = service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=InventoryItem)
def create_item(
    data: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new inventory item"""
    return service.create_item(db, data)


@router.put("/{item_id}", response_model=InventoryItem)
def update_item(
    item_id: int,
    data: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update an existing inventory item"""
    item = service.update_item(db, item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete an inventory item"""
    deleted = service.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted", "id": item_id}
```

---

## 4. Migraciones con Alembic

### 4.1 Inicializar Alembic

```bash
cd backend
alembic init alembic
```

### 4.2 Configurar `alembic.ini`

Busca la línea `sqlalchemy.url` y cámbiala por:

```ini
# sqlalchemy.url = driver://user:pass@localhost/dbname
# Comentar la línea anterior y usar config desde Python
```

### 4.3 Actualizar `alembic/env.py`

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Importar Base y modelos
from app.db.base import Base
from app.db.models import *  # Importa todos los modelos
from app.core.config import settings

# this is the Alembic Config object
config = context.config

# Establecer URL de la base de datos
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

# ... (resto del archivo se mantiene igual)
```

### 4.4 Crear Primera Migración

```bash
# Crear migración automática
alembic revision --autogenerate -m "Initial tables"

# Aplicar migración
alembic upgrade head
```

### 4.5 Script de Inicialización de Datos

**Archivo:** `backend/app/db/init_db.py`

```python
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.utils.security import hash_password


def init_db(db: Session) -> None:
    """Initialize database with default data"""
    
    # Check if admin exists
    admin = db.query(User).filter(User.username == "admin").first()
    
    if not admin:
        # Create admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            role="admin"
        )
        db.add(admin)
        
        # Create regular user
        user = User(
            username="user",
            email="user@example.com",
            hashed_password=hash_password("user123"),
            role="user"
        )
        db.add(user)
        
        db.commit()
        print("✅ Database initialized with default users")
    else:
        print("ℹ️  Database already initialized")
```

**Crear script para ejecutar:** `backend/init_db.py`

```python
from app.db.database import SessionLocal
from app.db.init_db import init_db

def main():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
```

**Ejecutar:**
```bash
cd backend
python init_db.py
```

---

## 5. Testing y Troubleshooting

### Verificar Conexión

```python
# test_connection.py
from app.db.database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Conexión exitosa a PostgreSQL")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
```

### Comandos Útiles de Alembic

```bash
# Ver historial de migraciones
alembic history

# Ver migración actual
alembic current

# Revertir última migración
alembic downgrade -1

# Aplicar todas las migraciones
alembic upgrade head

# Crear nueva migración
alembic revision --autogenerate -m "Add new field"
```

### Errores Comunes

#### Error: "connection refused"
- Verificar que PostgreSQL esté corriendo
- Verificar host y puerto en `.env`

#### Error: "password authentication failed"
- Verificar credenciales en `.env`
- Verificar usuario en PostgreSQL

#### Error: "database does not exist"
- Crear la base de datos manualmente
- Ver Paso 2

---

## 📝 Checklist Final

- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `inventorydb` creada
- [ ] Archivo `.env` configurado
- [ ] Dependencias instaladas
- [ ] Migraciones ejecutadas (`alembic upgrade head`)
- [ ] Datos iniciales creados (`python init_db.py`)
- [ ] Backend corriendo sin errores
- [ ] Frontend puede crear/leer/actualizar/eliminar productos

---

## 🎉 ¡Listo!

Tu sistema ahora usa PostgreSQL como base de datos permanente. Los datos persisten entre reinicios del servidor.

### Próximos Pasos Recomendados:
1. Implementar backup automático de la BD
2. Agregar índices para optimización
3. Implementar soft deletes
4. Agregar auditoría de cambios