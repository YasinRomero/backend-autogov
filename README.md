# 🏛️ Trámites Municipales Automáticos - Backend

Una API REST que automatiza y simplifica los trámites municipales mediante asistencia inteligente con IA. Permite a ciudadanos y extranjeros consultar requisitos, completar formularios y obtener orientación paso a paso sobre trámites de la municipalidad.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contribución](#contribución)

---

## ✨ Características

- **🔐 Autenticación Segura**: Registro e inicio de sesión con validación de identidad
  - Soporte para DNI (Documento Nacional de Identidad)
  - Soporte para Carné de Extranjería
  - Tokens JWT con autenticación segura

- **🤖 Asistencia con IA**: Integración con Google Gemini para consultas inteligentes
  - Guía paso a paso en trámites municipales
  - Respuestas personalizadas según el tipo de documento
  - Continuidad en las consultas (mantener historial)

- **🔍 Validación de Identidad**: Integración con API RENIEC
  - Verificación de datos personales
  - Validación de documentos de identidad

- **💬 Gestión de Feedback**: Sistema para recolectar comentarios
  - Categorización de feedback
  - Seguimiento de sugerencias de usuarios

- **💾 Persistencia de Datos**: SQLAlchemy + SQLite
  - Almacenamiento de usuarios y sesiones
  - Histórico de consultas y mensajes
  - Contextos de chat persistentes

---

## 🛠️ Stack Tecnológico

- **Lenguaje**: Python 3.x
- **Framework Web**: FastAPI 0.136.1
- **Servidor ASGI**: Uvicorn 0.46.0
- **ORM**: SQLAlchemy 2.0.49
- **Base de Datos**: SQLite
- **Autenticación**: JWT (python-jose) + bcrypt
- **Validación**: Pydantic 2.13.3
- **IA**: Google Gemini API (google-genai 2.0.1)
- **Testing**: pytest 9.0.3
- **Documentación**: Swagger/OpenAPI integrado en FastAPI

---

## 📁 Estructura del Proyecto

```
Grupo03_TramitesMunicipalesAutomaticos_Backend/
├── app/                          # Aplicación principal
│   ├── main.py                   # Punto de entrada, configuración de FastAPI
│   ├── api/
│   │   └── router.py             # Enrutador principal que agrupa los módulos
│   ├── core/
│   │   ├── config.py             # Variables de configuración (env vars)
│   │   └── security.py           # Funciones de seguridad y JWT
│   ├── db/
│   │   ├── session.py            # Configuración de la BD (SQLite, SessionLocal)
│   │   └── init_db.py            # Inicialización de datos por defecto
│   ├── models/                   # Modelos de BD (SQLAlchemy ORM)
│   │   ├── user.py               # Modelo de Usuario
│   │   ├── chat.py               # Modelo de Sesión de Chat
│   │   ├── message.py            # Modelo de Mensaje
│   │   ├── chat_context.py       # Contexto de conversación
│   │   ├── step.py               # Pasos de un trámite
│   │   ├── feedback.py           # Comentarios de usuarios
│   │   └── feedback_category.py  # Categorías de feedback
│   ├── modules/
│   │   ├── auth/                 # Módulo de Autenticación
│   │   │   ├── routes.py         # Endpoints: login, register, logout, profile
│   │   │   ├── service.py        # Lógica de negocio de autenticación
│   │   │   ├── schemas.py        # Schemas de validación (Pydantic)
│   │   │   └── dependencies.py   # Dependencias FastAPI (get_current_user)
│   │   ├── ai/                   # Módulo de IA
│   │   │   ├── routes.py         # Endpoints de consultas a IA
│   │   │   ├── service.py        # Integración con Google Gemini
│   │   │   ├── schemas.py        # Schemas de prompts y respuestas
│   │   │   └── strategies/       # Diferentes estrategias de consulta
│   │   └── feedback/             # Módulo de Feedback
│   │       ├── routes.py         # Endpoints de feedback
│   │       └── service.py        # Lógica de almacenamiento
│   ├── integrations/             # Integraciones externas
│   └── purge_files.py            # Utilidad para limpiar archivos
├── test/                         # Suite de pruebas
│   ├── conftest.py               # Configuración de fixtures pytest
│   ├── test_auth_login.py        # Tests de login
│   ├── test_auth_register.py     # Tests de registro
│   ├── test_auth_utils.py        # Tests de utilidades auth
│   └── test_core_jwt.py          # Tests de JWT
├── docs/                         # Documentación adicional
├── .env.example                  # Plantilla de variables de entorno
├── requirements.txt              # Dependencias de Python
├── endpointstest.http            # Archivo de prueba HTTP
├── endpointstest2.http           # Archivo de prueba HTTP (alternativo)
├── .gitignore                    # Archivos a ignorar en git
└── README.md                     # Este archivo
```

---

## 🔄 Flujo de Funcionamiento

1. **Autenticación**: Usuario se registra o inicia sesión
   - Validación con RENIEC si es ciudadano peruano
   - Generación de token JWT
   
2. **Consulta de Trámite**: Usuario consulta sobre un trámite específico
   - Se mantiene contexto de conversación (chat_context)
   - IA analiza la solicitud y proporciona guía paso a paso
   
3. **Persistencia**: Se guardan mensajes y contexto
   - Historial de mensajes en tabla `message`
   - Pasos sugeridos en tabla `step`
   - Usuario puede continuar donde dejó la consulta

4. **Feedback**: Usuario proporciona comentarios
   - Se registra en tabla `feedback`
   - Se clasifica por `feedback_category`

---

## 📋 Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

---

## 💾 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Aylin-28/Grupo03_TramitesMunicipalesAutomaticos_Backend.git
cd Grupo03_TramitesMunicipalesAutomaticos_Backend
```

### 2. Crear un entorno virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuración

### Variables de Entorno

Copia el archivo `.env.example` a `.env` y completa con tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con los siguientes valores:

```env
# Google Gemini (IA)
GEMINI_API_KEY=your_google_ai_studio_api_key
GEMINI_MODEL=gemini-2.0-flash  # O el modelo que uses

# API RENIEC (Validación de identidad)
RENIEC_API_URL=https://api.reniec.gob.pe/...
RENIEC_API_KEY=your_reniec_api_key

# Clave interna para operaciones
INTERNAL_IA_KEY=your_internal_key
```

### Obtener credenciales

- **Google Gemini**: Ve a [Google AI Studio](https://aistudio.google.com)
- **RENIEC**: Registrate en el [Portal de Integración RENIEC](https://www.reniec.gob.pe)

---

## 🚀 Uso

### Iniciar el servidor

```bash
# Desarrollo (con recarga automática)
uvicorn app.main:app --reload

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

### Acceder a la documentación interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 API Endpoints

### Autenticación (`/api/v1/auth`)

```http
# Registro con DNI
POST /api/v1/auth/register/dni
Content-Type: application/json

{
  "dni": "12345678",
  "password": "securePassword123",
  "email": "usuario@example.com",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

```http
# Registro con Carné de Extranjería
POST /api/v1/auth/register/inmigrationcard
Content-Type: application/json

{
  "immigration_card": "123456789",
  "password": "securePassword123",
  "email": "usuario@example.com",
  "first_name": "Jean",
  "last_name": "Dubois"
}
```

```http
# Inicio de sesión
POST /api/v1/auth/login
Content-Type: application/json

{
  "dni": "12345678",
  "password": "securePassword123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1
}
```

```http
# Obtener perfil del usuario
GET /api/v1/auth/me
Authorization: Bearer <token>
```

```http
# Actualizar email
PUT /api/v1/auth/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "nuevo@example.com"
}
```

```http
# Cerrar sesión
POST /api/v1/auth/logout
Authorization: Bearer <token>
```

### IA / Consultas (`/api/v1/ai`)

```http
# Iniciar consulta sobre un trámite
POST /api/v1/ai/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "¿Cuáles son los requisitos para sacar mi DNI por primera vez?",
  "procedure_type": "dni_renewal"
}
```

**Respuesta:**
```json
{
  "response": "Para sacar tu DNI por primera vez necesitas...",
  "steps": [
    {
      "step_number": 1,
      "description": "Acercarse a la oficina RENIEC",
      "required_documents": ["Acta de nacimiento"]
    }
  ]
}
```

```http
# Obtener historial de consultas
GET /api/v1/ai/history
Authorization: Bearer <token>
```

### Feedback (`/api/v1/feedback`)

```http
# Enviar feedback
POST /api/v1/feedback/submit
Authorization: Bearer <token>
Content-Type: application/json

{
  "category": "suggestion",
  "message": "La interfaz es muy intuitiva",
  "rating": 5
}
```

---

## 🧪 Testing

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar con reporte de cobertura

```bash
pytest --cov=app --cov-report=html
```

### Ejecutar pruebas específicas

```bash
# Solo tests de autenticación
pytest test/test_auth_login.py -v

# Solo tests de registro
pytest test/test_auth_register.py -v

# Solo tests de JWT
pytest test/test_core_jwt.py -v
```

### Archivos de prueba HTTP

También hay archivos `.http` que puedes usar con extensiones como REST Client de VSCode:

- `endpointstest.http` - Pruebas básicas de endpoints
- `endpointstest2.http` - Pruebas adicionales

---

## 📦 Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|----------|
| FastAPI | 0.136.1 | Framework web moderno |
| Uvicorn | 0.46.0 | Servidor ASGI |
| SQLAlchemy | 2.0.49 | ORM para BD |
| Pydantic | 2.13.3 | Validación de datos |
| python-jose | 3.5.0 | JWT |
| bcrypt | 4.0.1 | Hash de contraseñas |
| google-genai | 2.0.1 | Integración con Google Gemini |
| pytest | 9.0.3 | Testing |
| python-dotenv | 1.2.2 | Manejo de variables de entorno |

Para ver todas las dependencias: Ver `requirements.txt`

---

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Autenticación JWT con tokens
- ✅ CORS habilitado solo para dominios autorizados
- ✅ Validación de entrada con Pydantic
- ✅ Variables sensibles en `.env` (no commiteadas)

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commits con mensajes descriptivos (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto es desarrollado como parte de un trabajo académico. Ver LICENSE para más detalles.

---

## 📞 Contacto

Para preguntas o sugerencias, contacta a través de:
- **Email**: Tu email aquí
- **Issues**: [GitHub Issues](https://github.com/Aylin-28/Grupo03_TramitesMunicipalesAutomaticos_Backend/issues)

---

## 🗺️ Roadmap

- [ ] Integración con más instituciones públicas
- [ ] Soporte para múltiples idiomas
- [ ] Sistema de notificaciones
- [ ] Dashboard administrativo
- [ ] Análisis de uso y estadísticas
- [ ] Dockerización de la aplicación

---

**Última actualización**: Julio 2026
