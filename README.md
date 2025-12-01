# 🏪 Sistema de Gestión de Inventario

Sistema completo de gestión de inventario con backend en FastAPI y frontend en React.

## 📋 Índice
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecución](#ejecución)
- [Endpoints de la API](#endpoints-de-la-api)
- [Usuarios de Prueba](#usuarios-de-prueba)
- [Características](#características)

---

## 📁 Estructura del Proyecto

```
proyecto_inventario/
│
├── backend/                          # API FastAPI
│   ├── app/
│   │   ├── main.py                  # Aplicación principal
│   │   ├── api/
│   │   │   ├── router.py            # Router principal
│   │   │   └── v1/
│   │   │       ├── api_v1.py        # Router v1
│   │   │       └── routers/
│   │   │           ├── inventory.py # CRUD Inventario
│   │   │           └── users.py     # Auth & Usuarios
│   │   ├── core/
│   │   │   └── config.py            # Configuración
│   │   ├── schemas/
│   │   │   ├── inventory_schema.py  # Schemas Inventario
│   │   │   └── user_schema.py       # Schemas Usuario
│   │   ├── services/
│   │   │   ├── inventory_service.py # Lógica Inventario
│   │   │   └── user_service.py      # Lógica Usuario
│   │   └── utils/
│   │       ├── auth.py              # Auth middleware
│   │       ├── security.py          # JWT & Hash
│   │       └── exceptions.py        # Excepciones
│   └── requirements.txt
│
└── frontend/                         # React + Vite
    ├── public/
    ├── src/
    │   ├── App.jsx                  # Componente principal
    │   ├── main.jsx                 # Entry point
    │   └── index.css                # Estilos Tailwind
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

---

## 🛠 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Python 3.10+**
- **JWT** - Autenticación con tokens
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI

### Frontend
- **React 18** - Librería UI
- **Vite** - Build tool
- **Tailwind CSS** - Framework CSS
- **Lucide React** - Iconos

---

## 🚀 Instalación y Configuración

### 1️⃣ Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Frontend

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install
```

---

## ▶️ Ejecución

### Backend (Terminal 1)

```bash
cd backend
uvicorn app.main:app --reload
```

El backend estará disponible en: `http://localhost:8000`
Documentación API (Swagger): `http://localhost:8000/docs`

### Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

---

## 📡 Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/users/login` | Login y generación de token |
| GET | `/api/v1/users/me` | Información del usuario actual |
| GET | `/api/v1/users/` | Listar todos los usuarios |

### Inventario (Requieren autenticación)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/inventory/` | Listar todos los productos |
| GET | `/api/v1/inventory/{id}` | Obtener producto específico |
| POST | `/api/v1/inventory/` | Crear nuevo producto |
| PUT | `/api/v1/inventory/{id}` | Actualizar producto |
| DELETE | `/api/v1/inventory/{id}` | Eliminar producto |

### Ejemplo de Request - Login

```json
POST /api/v1/users/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Ejemplo de Request - Crear Producto

```json
POST /api/v1/inventory/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Laptop Dell",
  "quantity": 10,
  "price": 899.99,
  "description": "Laptop empresarial Dell Latitude"
}
```

---

## 👤 Usuarios de Prueba

El sistema viene con dos usuarios demo:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | admin |
| user | user123 | user |

---

## ✨ Características

### Backend
- ✅ Autenticación JWT
- ✅ CRUD completo de inventario
- ✅ Validación de datos con Pydantic
- ✅ CORS configurado
- ✅ Almacenamiento en memoria (ready para DB)
- ✅ Documentación automática (Swagger/OpenAPI)
- ✅ Gestión de errores
- ✅ Middleware de autenticación

### Frontend
- ✅ Login con JWT
- ✅ Dashboard con estadísticas
- ✅ Lista de productos con tabla
- ✅ Crear productos con modal
- ✅ Eliminar productos con confirmación
- ✅ Búsqueda en tiempo real
- ✅ Diseño responsivo
- ✅ Manejo de errores
- ✅ Estados de carga
- ✅ Logout y gestión de sesión

---

## 🔐 Seguridad

- Contraseñas hasheadas con bcrypt
- Tokens JWT con expiración (60 minutos)
- Validación de tokens en cada request
- CORS configurado para desarrollo

---

## 📝 Notas Importantes

### Almacenamiento
El backend actualmente usa **almacenamiento en memoria**. Los datos se pierden al reiniciar el servidor. Para producción, debes:

1. Configurar base de datos (PostgreSQL recomendado)
2. Actualizar los servicios para usar SQLAlchemy
3. Crear migraciones con Alembic

### Variables de Entorno
Para producción, crea un archivo `.env`:

```env
SECRET_KEY=tu_clave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐛 Troubleshooting

### Error: "Could not validate credentials"
- Verifica que el token no haya expirado
- Asegúrate de incluir el header: `Authorization: Bearer {token}`

### Error de CORS
- Verifica que el backend esté corriendo
- Confirma que CORS está configurado en `main.py`

### Frontend no carga datos
- Verifica que ambos servidores estén corriendo
- Revisa la consola del navegador para errores
- Confirma que la URL de la API sea correcta

---

## 📞 Soporte

Para problemas o preguntas:
- Revisa la documentación en `/docs`
- Verifica los logs del servidor
- Consulta los errores en la consola del navegador

---

## 📄 Licencia

MIT License - Copyright (c) 2025 César David Corrales Diaz

---

**¡Listo para usar! 🎉**