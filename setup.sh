#!/bin/bash

echo "======================================"
echo "🏪 Sistema de Gestión de Inventario"
echo "======================================"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Backend setup
echo -e "${BLUE}📦 Configurando Backend...${NC}"
cd backend

# Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias de Python..."
pip install -r requirements.txt

echo -e "${GREEN}✅ Backend configurado${NC}"
echo ""

# Volver al directorio raíz
cd ..

# Frontend setup
echo -e "${BLUE}⚛️  Configurando Frontend...${NC}"
cd frontend

# Instalar dependencias
echo "Instalando dependencias de npm..."
npm install

echo -e "${GREEN}✅ Frontend configurado${NC}"
echo ""

cd ..

echo "======================================"
echo -e "${GREEN}✅ Instalación completada${NC}"
echo "======================================"
echo ""
echo "Para ejecutar el proyecto:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "======================================"