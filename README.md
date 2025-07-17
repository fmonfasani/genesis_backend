# 🚀 Genesis Backend

**Backend Code Generation Agents for Genesis Engine**

Genesis Backend is a specialized module of the Genesis Engine ecosystem that focuses exclusively on backend code generation using AI agents. This repository contains intelligent agents that leverage Large Language Models (LLMs) to generate production-ready backend code for various frameworks.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com)
[![Django](https://img.shields.io/badge/Django-Latest-darkgreen.svg)](https://djangoproject.com)
[![NestJS](https://img.shields.io/badge/NestJS-Latest-red.svg)](https://nestjs.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Ecosystem Role

Genesis Backend is the **backend specialist** in the Genesis Engine ecosystem. It follows strict architectural principles:

- ✅ **Generates backend code only** (APIs, databases, authentication)
- ✅ **Uses LLMs for intelligent code generation**
- ✅ **Specialized agents for different responsibilities**
- ❌ **No frontend, CLI, or orchestration logic**
- ❌ **No direct user interaction**

## 🤖 Specialized Agents

### 🏗️ ArchitectAgent
Designs backend architecture using LLMs:
- API architecture design
- Data model design
- Technology selection
- Architecture validation

### ⚡ FastAPIAgent
Generates FastAPI applications:
- Complete FastAPI apps
- API routes and endpoints
- Pydantic models and schemas
- Authentication systems

### 🗄️ DatabaseAgent  
Specializes in database design:
- Database schema design
- ORM model generation
- Migration scripts
- Query optimization

### 🔐 AuthAgent
Authentication and authorization:
- JWT authentication
- OAuth2 integration
- Role-based access control
- Password security

### 🐍 DjangoAgent
Django application generation:
- Django project structure
- Models and admin
- Django REST Framework
- Authentication systems

### 🟦 NestJSAgent
NestJS/TypeScript backends:
- NestJS applications
- Controllers and services
- TypeORM entities
- Guard-based authentication

## 🛠️ Supported Technologies

### Backend Frameworks
- **FastAPI** (Python) - High-performance async API
- **Django** (Python) - Full-featured web framework
- **NestJS** (TypeScript) - Enterprise Node.js framework
- **Express** (JavaScript) - Minimal web framework

### Databases
- **PostgreSQL** - Advanced relational database
- **MySQL** - Popular relational database  
- **SQLite** - Lightweight database
- **MongoDB** - Document database
- **Redis** - In-memory data store

### Authentication Methods
- **JWT** - Stateless token authentication
- **OAuth2** - Authorization framework
- **Session-based** - Traditional session auth
- **Social Auth** - Google, GitHub, Facebook

### ORMs and Database Tools
- **SQLAlchemy** - Python SQL toolkit
- **Django ORM** - Django's built-in ORM
- **TypeORM** - TypeScript ORM
- **Prisma** - Next-generation ORM
- **Alembic** - Database migrations

## 📦 Installation

```bash
# Install from PyPI
pip install genesis-backend

# Install with development dependencies
pip install genesis-backend[dev]

# Install from source
git clone https://github.com/genesis-engine/genesis-backend.git
cd genesis-backend
pip install -e .
```

## 🚀 Quick Start

Genesis Backend is designed to be used by other components in the Genesis Engine ecosystem, particularly `genesis-core`. However, you can also use it directly:

```python
from genesis_backend import FastAPIAgent, BackendConfig, BackendFramework
from genesis_backend.config import DatabaseType, AuthMethod

# Configure backend generation
config = BackendConfig(
    project_name="my-api",
    framework=BackendFramework.FASTAPI,
    database=DatabaseConfig(DatabaseType.POSTGRESQL),
    auth=AuthConfig(AuthMethod.JWT),
    features=["api", "authentication", "database"]
)

# Create and execute agent
agent = FastAPIAgent()
task = AgentTask(
    id="generate_api",
    name="generate_fastapi_app",
    params={"config": config.to_dict()}
)

result = await agent.execute_task(task)
print(f"Generated files: {result.result['files']}")
```

## 🏗️ Architecture

### Agent Communication
All agents use the MCP (Multi-agent Communication Protocol) via MCPturbo for communication:

```python
# Agents communicate through MCPturbo protocol
response = await protocol.send_request(
    sender_id="architect_agent",
    target_id="claude",
    action="reasoning",
    data={"prompt": "Design API architecture..."}
)
```

### Code Generation Flow
1. **Architecture Design** - ArchitectAgent designs the backend architecture
2. **Framework Generation** - Framework-specific agents generate code
3. **Database Design** - DatabaseAgent creates schema and models
4. **Authentication** - AuthAgent adds security features
5. **Integration** - BackendGenerator coordinates all components

### LLM Integration
Agents leverage different LLMs for optimal results:
- **Claude** - Architecture design and complex reasoning
- **OpenAI** - Code generation and structured output
- **DeepSeek** - Fast code generation and optimization

## 🎨 Configuration

### Framework Selection
```python
from genesis_backend.config import BackendConfig, BackendFramework

# FastAPI configuration
fastapi_config = BackendConfig(
    framework=BackendFramework.FASTAPI,
    database=DatabaseConfig(DatabaseType.POSTGRESQL),
    auth=AuthConfig(AuthMethod.JWT)
)

# Django configuration  
django_config = BackendConfig(
    framework=BackendFramework.DJANGO,
    database=DatabaseConfig(DatabaseType.POSTGRESQL, ORMType.DJANGO_ORM),
    auth=AuthConfig(AuthMethod.SESSION)
)

# NestJS configuration
nestjs_config = BackendConfig(
    framework=BackendFramework.NESTJS,
    database=DatabaseConfig(DatabaseType.POSTGRESQL, ORMType.TYPEORM),
    auth=AuthConfig(AuthMethod.JWT)
)
```

### Database Configuration
```python
from genesis_backend.config import DatabaseConfig, DatabaseType, ORMType

# PostgreSQL with SQLAlchemy
postgres_config = DatabaseConfig(
    type=DatabaseType.POSTGRESQL,
    host="localhost",
    port=5432,
    name="my_app_db",
    user="postgres",
    password="password",
    orm=ORMType.SQLALCHEMY
)

# MongoDB with Mongoose
mongo_config = DatabaseConfig(
    type=DatabaseType.MONGODB,
    host="localhost", 
    port=27017,
    name="my_app_db",
    orm=ORMType.MONGOOSE
)
```

### Authentication Configuration
```python
from genesis_backend.config import AuthConfig, AuthMethod

# JWT Authentication
jwt_config = AuthConfig(
    method=AuthMethod.JWT,
    secret_key="your-secret-key",
    algorithm="HS256",
    access_token_expire_minutes=30,
    refresh_token_expire_days=7
)

# OAuth2 with social providers
oauth_config = AuthConfig(
    method=AuthMethod.OAUTH2,
    oauth_providers=["google", "github", "facebook"]
)
```

## 🎯 Usage Examples

### Generate FastAPI Application
```python
from genesis_backend.agents import FastAPIAgent
from genesis_backend.config import BackendConfig

agent = FastAPIAgent()

# Generate complete FastAPI app
result = await agent.execute_task(AgentTask(
    name="generate_fastapi_app",
    params={
        "config": BackendConfig(
            project_name="blog-api",
            features=["api", "authentication", "database"]
        ).to_dict(),
        "architecture": {
            "entities": [
                {"name": "User", "fields": ["id", "email", "name"]},
                {"name": "Post", "fields": ["id", "title", "content", "user_id"]}
            ]
        }
    }
))

# Result contains generated FastAPI code
print(result.result["main_application"])
```

### Design Database Schema
```python
from genesis_backend.agents import DatabaseAgent

agent = DatabaseAgent()

# Design database schema
result = await agent.execute_task(AgentTask(
    name="design_database_schema",
    params={
        "entities": [
            {"name": "User", "attributes": ["id", "email", "password"]},
            {"name": "Post", "attributes": ["id", "title", "content"]}
        ],
        "database_type": "postgresql"
    }
))

# Result contains optimized database schema
print(result.result["database_schema"])
```

### Generate Authentication System
```python
from genesis_backend.agents import AuthAgent

agent = AuthAgent()

# Generate JWT authentication
result = await agent.execute_task(AgentTask(
    name="generate_jwt_auth",
    params={
        "config": {
            "auth": {
                "method": "jwt",
                "secret_key": "secret",
                "algorithm": "HS256"
            }
        }
    }
))

# Result contains complete auth system
print(result.result["auth_code"])
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific agent tests
pytest tests/test_fastapi_agent.py

# Run with coverage
pytest --cov=genesis_backend

# Run integration tests
pytest tests/integration/
```

## 🔧 Development

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/genesis-engine/genesis-backend.git
cd genesis-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality
```bash
# Format code
black agents/ generators/ tests/
isort agents/ generators/ tests/

# Type checking
mypy agents/ generators/

# Linting
flake8 agents/ generators/ tests/

# Run all quality checks
make quality
```

### Creating Custom Agents
```python
from genesis_backend.agents import GenesisAgent, AgentTask, TaskResult

class CustomBackendAgent(GenesisAgent):
    def __init__(self):
        super().__init__(
            agent_id="custom_backend",
            name="Custom Backend Agent",
            agent_type="backend"
        )
        
        self.add_capability("generate_custom_backend")
        self.register_handler("generate_custom_backend", self._handle_generate)
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        # Your custom backend generation logic
        return TaskResult(
            task_id=task.id,
            success=True,
            result={"generated_code": "..."}
        )
    
    async def _handle_generate(self, request):
        # Handle MCP requests
        return await self.generate_custom_code(request.data)
```

## 🏛️ Ecosystem Integration

Genesis Backend integrates seamlessly with other Genesis Engine components:

### With Genesis Core
```python
# genesis-core automatically discovers agents
from genesis_backend import get_agents

# Register all backend agents
for agent_class in get_agents():
    orchestrator.register_agent(agent_class())
```

### With Genesis Templates
```python
from genesis_templates import TemplateEngine
from genesis_backend.generators import BackendGenerator

# Use templates for code generation
template_engine = TemplateEngine()
generator = BackendGenerator(template_engine)

result = await generator.generate_backend(config, architecture, output_path)
```

### With MCPturbo
```python
from mcpturbo import protocol
from genesis_backend.agents import FastAPIAgent

# Agents automatically use MCPturbo for LLM communication
agent = FastAPIAgent()
# MCPturbo handles all LLM interactions transparently
```

## 📋 Generated Code Examples

### FastAPI Application
```python
# Generated main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My API",
    description="Generated by Genesis Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to My API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### SQLAlchemy Models
```python
# Generated models/user.py
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### JWT Authentication
```python
# Generated auth/jwt.py
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Agent fails to generate code
```bash
# Check MCPturbo connection
python -c "from mcpturbo import protocol; print(protocol.status())"

# Verify LLM API keys
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

**Issue**: Generated code has syntax errors
```bash
# Enable debug logging
export GENESIS_LOG_LEVEL=DEBUG

# Check generated code quality
python -m py_compile generated_file.py
```

**Issue**: Database connection fails
```bash
# Verify database configuration
python -c "from genesis_backend.config import DatabaseConfig; print(config.connection_url)"

# Test database connection
psql "postgresql://user:pass@localhost/db" -c "SELECT 1;"
```

## 📄 API Reference

### Core Classes

#### BackendConfig
Configuration class for backend generation.

```python
class BackendConfig:
    project_name: str
    framework: BackendFramework
    database: DatabaseConfig
    auth: AuthConfig
    features: List[str]
    
    def to_dict(self) -> Dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BackendConfig": ...
```

#### GenesisAgent
Base class for all backend agents.

```python
class GenesisAgent:
    agent_id: str
    name: str
    agent_type: str
    
    async def execute_task(self, task: AgentTask) -> TaskResult: ...
    def add_capability(self, capability: str): ...
    def register_handler(self, action: str, handler: Callable): ...
```

### Agent Methods

#### FastAPIAgent
```python
async def execute_task(self, task: AgentTask) -> TaskResult
    # Tasks: generate_fastapi_app, generate_fastapi_routes, 
    #        generate_pydantic_models, generate_fastapi_auth
```

#### DatabaseAgent
```python
async def execute_task(self, task: AgentTask) -> TaskResult
    # Tasks: design_database_schema, generate_orm_models,
    #        create_database_migrations, optimize_database_queries
```

#### AuthAgent  
```python
async def execute_task(self, task: AgentTask) -> TaskResult
    # Tasks: generate_jwt_auth, generate_oauth2_auth,
    #        generate_user_management, generate_role_permissions
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style
- Use Black for code formatting
- Follow PEP 8 guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Maintain test coverage above 90%

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Genesis Engine Team** - Core architecture and vision
- **MCPturbo** - Multi-agent communication protocol
- **Genesis Templates** - Template engine integration
- **FastAPI Community** - Excellent web framework
- **Django Community** - Robust web framework
- **NestJS Community** - Enterprise Node.js framework

## 🔗 Related Projects

- **[Genesis Core](https://github.com/genesis-engine/genesis-core)** - Main orchestrator
- **[Genesis Frontend](https://github.com/genesis-engine/genesis-frontend)** - Frontend generation
- **[Genesis DevOps](https://github.com/genesis-engine/genesis-devops)** - Infrastructure generation
- **[Genesis Templates](https://github.com/genesis-engine/genesis-templates)** - Template engine
- **[MCPturbo](https://github.com/fmonfasani/mcpturbo)** - Communication protocol

---

<div align="center">

**[🏠 Genesis Engine](https://genesis-engine.dev)** •
**[📖 Documentation](https://docs.genesis-engine.dev/backend)** •
**[🐛 Issues](https://github.com/genesis-engine/genesis-backend/issues)** •
**[💬 Discussions](https://github.com/genesis-engine/genesis-backend/discussions)**

Made with ❤️ by the Genesis Engine Team

</div>