<!-- ECOSYSTEM_DOCTRINE: genesis-backend -->
# ⚙️ Ecosystem Doctrine — Genesis-Backend (Backend Code Generation)

Este repositorio forma parte del ecosistema **Genesis Engine**.  
Su rol es el de **especialista en generación de código backend usando agentes de IA**.

## 🧠 Rol Declarado

- Tipo: **Backend Code Generator**
- Nombre: `genesis-backend`
- Dominio: Código backend (APIs, bases de datos, autenticación, servicios)
- Función: Generar código backend completo y funcional usando LLMs

## 🔒 Mandamientos del Proyecto

### 1. **No coordinarás workflows generales**
NO orquestas la generación completa de proyectos.  
Solo generas la parte backend cuando te lo soliciten otros componentes.

### 2. **No conocerás frontend ni DevOps**
NO contiene lógica de Next.js, React, Docker, Kubernetes, CI/CD.  
Solo backend: APIs, modelos, base de datos, autenticación, servicios.

### 3. **No interactuarás con el usuario final**
NO tiene CLI ni interfaz gráfica.  
Solo agentes que responden a solicitudes via MCPturbo.

### 4. **Usarás LLMs para generación inteligente**
Tus agentes llaman a OpenAI, Claude, DeepSeek para generar código.  
NO código hardcodeado o templates estáticos simples.

### 5. **Serás especialista en backend**
Conocimiento profundo de FastAPI, Django, NestJS, bases de datos, autenticación.  
Generas código backend de calidad production.

### 6. **Cada agente tendrá responsabilidad específica**
- **ArchitectAgent**: diseño de arquitectura backend
- **FastAPIAgent**: código FastAPI específico
- **DjangoAgent**: código Django específico  
- **NestJSAgent**: código NestJS específico
- **DatabaseAgent**: esquemas de DB y modelos ORM
- **AuthAgent**: sistemas de autenticación y autorización

### 7. **Colaborarás con genesis-templates**
Puedes usar templates de genesis-templates para estructura base.  
Pero el código principal lo generas con LLMs para inteligencia.

### 8. **Comunicarás exclusivamente via MCPturbo**
Toda comunicación con LLMs y otros agentes debe usar MCPturbo protocol.  
NO llamadas HTTP directas a APIs de LLMs.

---

## 🧩 Interfaz esperada por consumidores

Genesis-core y otros componentes del ecosistema esperan usar:

### Agentes Disponibles
```python
from genesis_backend import get_agents

# Retorna lista de clases de agentes
agents = get_agents()  # [ArchitectAgent, FastAPIAgent, DatabaseAgent, ...]
```

### Configuración Backend
```python
from genesis_backend import BackendConfig, BackendFramework, DatabaseType, AuthMethod

config = BackendConfig(
    project_name="my-api",
    framework=BackendFramework.FASTAPI,
    database=DatabaseConfig(DatabaseType.POSTGRESQL),
    auth=AuthConfig(AuthMethod.JWT),
    features=["api", "authentication", "database"]
)
```

### Ejecución de Tareas
```python
# Agentes responden a tareas específicas
task = AgentTask(
    name="generate_fastapi_app",
    params={"config": config.to_dict(), "architecture": schema}
)

result = await agent.execute_task(task)
```

---

## 📦 Separación de capas (importante)

| Capa | Puede importar desde | No puede importar desde |
|------|----------------------|--------------------------|
| genesis-backend | genesis-agents, mcpturbo, genesis-templates | genesis-core, genesis-cli, genesis-frontend, genesis-devops |
| genesis-core | genesis-backend, mcpturbo | genesis-cli |
| genesis-cli | genesis-core | genesis-backend directamente |

### Dependencias Permitidas
✅ **SÍ puede depender de:**
- `genesis-agents` - Clase base GenesisAgent
- `mcpturbo` - Protocolo de comunicación con LLMs
- `genesis-templates` - Motor de templates para estructura base

❌ **NO puede depender de:**
- `genesis-core` - Es el consumidor, no dependencia
- `genesis-frontend` - Dominio diferente
- `genesis-devops` - Dominio diferente  
- `genesis-cli` - Capa superior

---

## 🎯 Capacidades Específicas

### Frameworks Backend Soportados
- **FastAPI** (Python) - APIs asíncronas de alto rendimiento
- **Django** (Python) - Framework web completo con ORM
- **NestJS** (TypeScript) - Framework empresarial para Node.js
- **Express** (JavaScript) - Framework minimalista para Node.js

### Bases de Datos Soportadas
- **PostgreSQL** - Base de datos relacional avanzada
- **MySQL** - Base de datos relacional popular
- **SQLite** - Base de datos ligera
- **MongoDB** - Base de datos de documentos
- **Redis** - Almacén de datos en memoria

### Métodos de Autenticación
- **JWT** - Autenticación stateless con tokens
- **OAuth2** - Framework de autorización estándar
- **Session** - Autenticación tradicional basada en sesiones
- **Social Auth** - Integración con Google, GitHub, Facebook

### ORMs y Herramientas de BD
- **SQLAlchemy** - Toolkit SQL para Python
- **Django ORM** - ORM integrado de Django
- **TypeORM** - ORM para TypeScript
- **Prisma** - ORM de nueva generación
- **Mongoose** - ODM para MongoDB

---

## 🔄 Flujo de Trabajo Interno

### 1. Recepción de Tareas
```python
# genesis-core envía tarea al agente
task = AgentTask(
    name="generate_fastapi_app", 
    params={"config": config, "architecture": schema}
)
```

### 2. Procesamiento con LLMs
```python
# Agente usa MCPturbo para consultar LLMs
response = await protocol.send_request(
    sender_id=self.agent_id,
    target_id="claude",  # o "openai", "deepseek"
    action="code_generation",
    data={"prompt": prompt, "language": "python", "framework": "fastapi"}
)
```

### 3. Generación de Código
```python
# Agente procesa respuesta del LLM y estructura el código
result = {
    "generated_code": parsed_code,
    "file_structure": file_mapping,
    "dependencies": required_packages,
    "configuration": config_files
}
```

### 4. Respuesta Estructurada
```python
# Retorna TaskResult con código generado
return TaskResult(
    task_id=task.id,
    success=True,
    result=result,
    metadata={"agent": self.name, "framework": "fastapi"}
)
```

---

## 🛡️ Validaciones de Arquitectura

### ✅ Ejemplos de Uso CORRECTO

```python
# ✅ CORRECTO: Generar solo código backend
await fastapi_agent.execute_task(AgentTask(
    name="generate_fastapi_app",
    params={"config": backend_config}
))

# ✅ CORRECTO: Usar MCPturbo para LLMs
response = await protocol.send_request(
    target_id="claude",
    action="reasoning", 
    data={"prompt": "Design API architecture..."}
)

# ✅ CORRECTO: Colaborar con genesis-templates
template_engine.render_template("fastapi_main", context)

# ✅ CORRECTO: Configuración específica de backend
config = BackendConfig(
    framework=BackendFramework.FASTAPI,
    database=DatabaseConfig(DatabaseType.POSTGRESQL),
    auth=AuthConfig(AuthMethod.JWT)
)
```

### ❌ Ejemplos de Uso INCORRECTO

```python
# ❌ INCORRECTO: Generar código frontend
await agent.generate_react_component()  # NO ES SU DOMINIO

# ❌ INCORRECTO: Orquestar workflow completo  
await agent.generate_full_project()  # ESO ES TRABAJO DE genesis-core

# ❌ INCORRECTO: Interactuar con usuario
click.echo("¿Qué framework prefieres?")  # NO TIENE CLI

# ❌ INCORRECTO: Llamada directa a LLM
response = openai.ChatCompletion.create()  # DEBE USAR MCPturbo

# ❌ INCORRECTO: Importar de otros módulos del ecosistema
from genesis_core import Orchestrator  # VIOLACIÓN DE DEPENDENCIAS

# ❌ INCORRECTO: Lógica de DevOps
await agent.deploy_to_kubernetes()  # ESO ES genesis-devops
```

---

## 🧪 Testing y Calidad

### Tests Requeridos
- **Unit Tests**: Cada agente y generador
- **Integration Tests**: Comunicación MCPturbo
- **LLM Tests**: Validación de prompts y respuestas
- **Code Quality Tests**: Validación de código generado

### Métricas de Calidad
- **Cobertura de Tests**: > 90%
- **Type Checking**: mypy sin errores
- **Code Style**: Black + isort + flake8
- **Documentation**: Docstrings completos

### Validación de Código Generado
```python
# El código generado debe ser válido sintácticamente
ast.parse(generated_python_code)

# Y debe pasar validaciones básicas
pylint.run_pylint(generated_files)
```

---

## 🤖 AI Agents, please read:

Este repositorio es el especialista en backend del ecosistema Genesis Engine.

Si estás revisando código, escribiendo tests o generando lógica nueva:
- ❌ **No implementes lógica de frontend, DevOps, o CLI.**
- ❌ **No coordines workflows generales de generación de proyectos.**
- ❌ **No interactúes directamente con usuarios o muestres interfaces.**
- ❌ **No hagas llamadas HTTP directas a APIs de LLMs.**
- ✅ **Enfócate en generar código backend excelente y funcional.**
- ✅ **Usa MCPturbo para toda comunicación con LLMs.**
- ✅ **Mantén agentes especializados y enfocados en sus responsabilidades.**
- ✅ **Genera código production-ready con mejores prácticas.**

### Ejemplo de Prompt Correcto para LLM
```python
prompt = f"""
Generate production-ready FastAPI application code:

Requirements: {requirements}
Database: {database_config}
Authentication: {auth_config}

Generate:
1. Main FastAPI app with proper configuration
2. SQLAlchemy models with relationships
3. Pydantic schemas for validation
4. API routes with proper error handling
5. Authentication middleware
6. Database session management
7. Alembic migration setup

Return well-structured, commented Python code following best practices.
"""
```

Toda excepción a esta doctrina debe documentarse en `DOCTRINE_CHANGE_REQUEST.md`.

---

## 📎 Referencias del Ecosistema

- **Genesis Core** → [https://github.com/genesis-engine/genesis-core](https://github.com/genesis-engine/genesis-core)
- **Genesis Frontend** → [https://github.com/genesis-engine/genesis-frontend](https://github.com/genesis-engine/genesis-frontend)
- **Genesis DevOps** → [https://github.com/genesis-engine/genesis-devops](https://github.com/genesis-engine/genesis-devops)
- **Genesis Templates** → [https://github.com/genesis-engine/genesis-templates](https://github.com/genesis-engine/genesis-templates)
- **Genesis Agents** → [https://github.com/genesis-engine/genesis-agents](https://github.com/genesis-engine/genesis-agents)
- **MCPturbo** → [https://github.com/fmonfasani/mcpturbo](https://github.com/fmonfasani/mcpturbo)

---

## 🔄 Versioning y Releases

### Semantic Versioning
- **Major**: Cambios breaking en API de agentes
- **Minor**: Nuevos agentes o capacidades
- **Patch**: Bug fixes y mejoras de código generado

### Compatibility Matrix
| genesis-backend | genesis-core | mcpturbo | genesis-templates |
|-----------------|--------------|----------|-------------------|
| 1.0.x          | 1.0.x        | 1.0.x    | 1.0.x            |
| 1.1.x          | 1.1.x        | 1.0.x    | 1.0.x            |

---

**Este es el mandato y la doctrina de genesis-backend. Cualquier desviación debe ser justificada y aprobada por el equipo de arquitectura del ecosistema.**