<!-- ECOSYSTEM_DOCTRINE: genesis-backend -->
# ⚙️ Ecosystem Doctrine — Genesis-Backend (Generación Backend)

Este repositorio forma parte del ecosistema **Genesis Engine**.  
Su rol es el de **generación de código backend usando agentes especializados**.

## 🧠 Rol Declarado

- Tipo: **Generador Backend**
- Nombre: `genesis-backend`
- Dominio: Código backend (APIs, bases de datos, autenticación)
- Función: Generar código backend completo y funcional

## 🔒 Mandamientos del Proyecto

### 1. **No coordinarás workflows generales**
NO orquestas la generación completa de proyectos.  
Solo generas la parte backend cuando te lo soliciten.

### 2. **No conocerás frontend ni DevOps**
NO contiene lógica de Next.js, Docker, etc.  
Solo backend: APIs, modelos, base de datos, autenticación.

### 3. **No interactuarás con el usuario final**
NO tiene CLI ni interfaz gráfica.  
Solo agentes que responden a solicitudes MCPturbo.

### 4. **Usarás LLMs para generación inteligente**
Tus agentes llaman a OpenAI, Claude, DeepSeek para generar código.  
NO código hardcodeado o templates estáticos.

### 5. **Serás especialista en backend**
Conocimiento profundo de FastAPI, Django, Node.js, bases de datos.  
Generas código backend de calidad production.

### 6. **Cada agente tendrá responsabilidad específica**
ArchitectAgent: diseño de arquitectura  
FastAPIAgent: código FastAPI  
DatabaseAgent: esquemas de DB  
AuthAgent: autenticación

### 7. **Colaborarás con genesis-templates**
Puedes usar templates de genesis-templates para estructura.  
Pero el código lo generas con LLMs.

---

## 🧩 Interfaz esperada por consumidores

Genesis-core y otros componentes usan:

- `ArchitectAgent.analyze_requirements()`
- `FastAPIAgent.generate_backend()`
- `DatabaseAgent.create_schema()`
- `AuthAgent.setup_authentication()`

---

## 📦 Separación de capas (importante)

| Capa | Puede importar desde | No puede importar desde |
|------|----------------------|--------------------------|
| genesis-backend | genesis-agents, mcpturbo, genesis-templates | genesis-core, genesis-cli, genesis-frontend, genesis-devops |
| genesis-core | mcpturbo | genesis-backend |

---

## 🤖 AI Agents, please read:

Este repositorio es el especialista en backend del ecosistema.

Si estás revisando código, escribiendo tests o generando lógica nueva:
- ❌ No implementes lógica de frontend o DevOps.
- ❌ No coordines workflows generales.
- ❌ No interactúes directamente con usuarios.
- ✅ Enfócate en generar código backend excelente.
- ✅ Usa LLMs para código inteligente.
- ✅ Mantén agentes especializados y enfocados.

Toda excepción debe documentarse en `DOCTRINE_CHANGE_REQUEST.md`.

---

## 📎 Referencias

- Genesis Agents → [https://github.com/fmonfasani/genesis-agents](https://github.com/fmonfasani/genesis-agents)
- MCPturbo → [https://github.com/fmonfasani/mcpturbo](https://github.com/fmonfasani/mcpturbo)
- FastAPI → [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
