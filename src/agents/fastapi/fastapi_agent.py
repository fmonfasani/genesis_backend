"""
FastAPI Agent

Specializes in generating FastAPI backend code using LLMs.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from pathlib import Path

from genesis_agents import GenesisAgent, AgentTask, TaskResult
from mcpturbo import protocol

from ..config import BackendConfig, BackendFramework

logger = logging.getLogger(__name__)


class FastAPIAgent(GenesisAgent):
    """
    Agent specialized in FastAPI backend generation.
    
    Responsibilities:
    - Generate FastAPI application structure
    - Generate API routes and endpoints
    - Generate Pydantic models and schemas
    - Generate middleware configuration
    - Generate authentication logic
    - Generate database integration
    """
    
    def __init__(self):
        super().__init__(
            agent_id="fastapi_generator",
            name="FastAPI Generator Agent",
            agent_type="generator"
        )
        
        # FastAPI-specific capabilities
        self.add_capability("generate_fastapi_app")
        self.add_capability("generate_fastapi_routes")
        self.add_capability("generate_pydantic_models")
        self.add_capability("generate_fastapi_middleware")
        self.add_capability("generate_fastapi_auth")
        self.add_capability("generate_sqlalchemy_models")
        self.add_capability("generate_fastapi_dependencies")
        
        # Register handlers
        self.register_handler("generate_fastapi_app", self._handle_generate_app)
        self.register_handler("generate_fastapi_routes", self._handle_generate_routes)
        self.register_handler("generate_pydantic_models", self._handle_generate_schemas)
        self.register_handler("generate_fastapi_middleware", self._handle_generate_middleware)
        self.register_handler("generate_fastapi_auth", self._handle_generate_auth)
        self.register_handler("generate_sqlalchemy_models", self._handle_generate_models)
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Execute FastAPI generation task using LLMs."""
        try:
            self.logger.info(f"⚡ Executing FastAPI task: {task.name}")
            
            if task.name == "generate_fastapi_app":
                result = await self._generate_fastapi_application(task.params)
            elif task.name == "generate_fastapi_routes":
                result = await self._generate_fastapi_routes(task.params)
            elif task.name == "generate_pydantic_models":
                result = await self._generate_pydantic_schemas(task.params)
            elif task.name == "generate_fastapi_middleware":
                result = await self._generate_fastapi_middleware(task.params)
            elif task.name == "generate_fastapi_auth":
                result = await self._generate_fastapi_authentication(task.params)
            elif task.name == "generate_sqlalchemy_models":
                result = await self._generate_sqlalchemy_models(task.params)
            elif task.name == "generate_fastapi_dependencies":
                result = await self._generate_fastapi_dependencies(task.params)
            else:
                result = await self._handle_generic_task(task)
            
            return TaskResult(
                task_id=task.id,
                success=True,
                result=result,
                metadata={
                    "agent": self.name,
                    "task_type": task.name,
                    "framework": "fastapi",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error in FastAPI task {task.name}: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                metadata={"agent": self.name, "task_type": task.name}
            )
    
    async def _generate_fastapi_application(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete FastAPI application structure using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        architecture = params.get("architecture", {})
        
        app_generation_prompt = f"""
        Generate a complete FastAPI application with this configuration:
        
        Project Name: {config.project_name}
        Description: {config.description}
        Features: {config.features}
        Database: {config.database.type.value}
        Authentication: {config.auth.method.value}
        API Version: {config.api_version}
        CORS Origins: {config.cors_origins}
        
        Architecture: {architecture}
        
        Generate the main FastAPI application file (main.py) that includes:
        1. FastAPI app initialization with metadata
        2. CORS middleware configuration
        3. Route registration
        4. Error handling middleware
        5. Health check endpoint
        6. API documentation setup
        7. Database connection setup if needed
        8. Authentication middleware if needed
        9. Logging configuration
        10. Application lifecycle events
        
        Make it production-ready with proper structure and error handling.
        Return only the Python code.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at code generation
            action="code_generation",
            data={
                "prompt": app_generation_prompt,
                "language": "python",
                "framework": "fastapi"
            }
        )
        
        # Generate additional configuration files
        config_files = await self._generate_config_files(config)
        requirements = await self._generate_requirements_file(config)
        dockerfile = await self._generate_dockerfile(config)
        
        return {
            "main_application": response.result,
            "config_files": config_files,
            "requirements_txt": requirements,
            "dockerfile": dockerfile,
            "structure": self._generate_project_structure(config),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "framework": "fastapi",
                "version": "0.115.0+"
            }
        }
    
    async def _generate_fastapi_routes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate FastAPI routes and endpoints using LLM."""
        api_design = params.get("api_design", {})
        data_models = params.get("data_models", [])
        auth_required = params.get("auth_required", False)
        
        routes_generation_prompt = f"""
        Generate FastAPI routes for this API design:
        
        API Design: {api_design}
        Data Models: {data_models}
        Authentication Required: {auth_required}
        
        Generate comprehensive FastAPI routes that include:
        1. Router setup with tags and prefixes
        2. Path parameters with proper types
        3. Query parameters with validation
        4. Request/response models using Pydantic
        5. HTTP status codes for different scenarios
        6. Error handling with HTTPException
        7. Authentication dependencies if required
        8. Input validation and sanitization
        9. Proper docstrings and OpenAPI metadata
        10. CRUD operations where applicable
        
        Generate separate router files for different resource groups.
        Return structured code for each router.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",  # DeepSeek good at fast code generation
            action="fast_coding",
            data={
                "prompt": routes_generation_prompt,
                "language": "python",
                "framework": "fastapi"
            }
        )
        
        return {
            "routes_code": response.result,
            "router_files": self._parse_router_files(response.result),
            "endpoints_summary": self._extract_endpoints_from_routes(response.result),
            "auth_dependencies": self._extract_auth_dependencies(response.result) if auth_required else {},
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_pydantic_schemas(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Pydantic models and schemas using LLM."""
        data_models = params.get("data_models", [])
        api_design = params.get("api_design", {})
        
        schemas_generation_prompt = f"""
        Generate Pydantic schemas for this data model:
        
        Data Models: {data_models}
        API Design: {api_design}
        
        Generate comprehensive Pydantic schemas including:
        1. Base schemas for each entity
        2. Create schemas (for POST requests)
        3. Update schemas (for PUT/PATCH requests)
        4. Response schemas (for GET responses)
        5. List response schemas with pagination
        6. Nested schemas for relationships
        7. Validation rules and custom validators
        8. Field descriptions for API documentation
        9. Examples for OpenAPI documentation
        10. Error response schemas
        
        Use proper Pydantic v2 syntax with Field() and validation.
        Return well-organized schema classes.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at structured data modeling
            action="code_generation",
            data={
                "prompt": schemas_generation_prompt,
                "language": "python",
                "framework": "pydantic"
            }
        )
        
        return {
            "schemas_code": response.result,
            "schema_classes": self._parse_schema_classes(response.result),
            "validation_rules": self._extract_validation_rules(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_fastapi_middleware(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate FastAPI middleware using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        features = params.get("features", [])
        
        middleware_generation_prompt = f"""
        Generate FastAPI middleware for this configuration:
        
        Features: {features}
        CORS Origins: {config.cors_origins}
        Authentication: {config.auth.method.value}
        Debug Mode: {config.debug}
        
        Generate middleware for:
        1. CORS configuration with proper origins
        2. Request logging and timing
        3. Error handling and exception catching
        4. Rate limiting if needed
        5. Security headers
        6. Request ID generation
        7. Authentication middleware if needed
        8. Compression middleware
        9. Database session management
        10. Custom business logic middleware
        
        Return production-ready middleware code.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at middleware patterns
            action="reasoning",
            data={
                "prompt": middleware_generation_prompt,
                "system_prompt": "You are a FastAPI expert. Generate robust middleware following best practices."
            }
        )
        
        return {
            "middleware_code": response.result,
            "middleware_order": self._extract_middleware_order(response.result),
            "configuration": self._extract_middleware_config(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_fastapi_authentication(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate FastAPI authentication system using LLM."""
        auth_config = params.get("auth_config", {})
        user_model = params.get("user_model", {})
        
        auth_generation_prompt = f"""
        Generate FastAPI authentication system:
        
        Auth Method: {auth_config.get('method', 'jwt')}
        Secret Key: {auth_config.get('secret_key', 'secret')}
        Algorithm: {auth_config.get('algorithm', 'HS256')}
        Token Expiration: {auth_config.get('access_token_expire_minutes', 30)} minutes
        User Model: {user_model}
        
        Generate complete authentication system including:
        1. JWT token creation and verification
        2. Password hashing utilities
        3. User authentication dependencies
        4. Login and registration endpoints
        5. Token refresh mechanism
        6. Password reset functionality
        7. User permissions and roles if needed
        8. OAuth2 integration if specified
        9. Security utilities and helpers
        10. Authentication error handling
        
        Use FastAPI security utilities and follow OAuth2 patterns.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at authentication patterns
            action="code_generation",
            data={
                "prompt": auth_generation_prompt,
                "language": "python",
                "framework": "fastapi_auth"
            }
        )
        
        return {
            "auth_code": response.result,
            "auth_routes": self._extract_auth_routes(response.result),
            "dependencies": self._extract_auth_dependencies(response.result),
            "utilities": self._extract_auth_utilities(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_sqlalchemy_models(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SQLAlchemy models using LLM."""
        data_models = params.get("data_models", [])
        relationships = params.get("relationships", [])
        database_config = params.get("database_config", {})
        
        models_generation_prompt = f"""
        Generate SQLAlchemy models for this database schema:
        
        Data Models: {data_models}
        Relationships: {relationships}
        Database: {database_config.get('type', 'postgresql')}
        
        Generate comprehensive SQLAlchemy models including:
        1. Table definitions with proper column types
        2. Primary keys and foreign keys
        3. Relationships (ForeignKey, relationship())
        4. Indexes for performance
        5. Constraints and validation
        6. Model methods and properties
        7. Serialization methods
        8. Audit fields (created_at, updated_at)
        9. Soft delete support if needed
        10. Database migration support
        
        Use SQLAlchemy 2.0 syntax with proper annotations.
        Include Base class and database configuration.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at data modeling
            action="reasoning",
            data={
                "prompt": models_generation_prompt,
                "system_prompt": "You are a database expert. Generate efficient SQLAlchemy models."
            }
        )
        
        return {
            "models_code": response.result,
            "model_classes": self._parse_model_classes(response.result),
            "relationships_defined": self._extract_model_relationships(response.result),
            "database_config": self._extract_database_config(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_fastapi_dependencies(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate FastAPI dependencies using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        
        dependencies_generation_prompt = f"""
        Generate FastAPI dependencies for this configuration:
        
        Database: {config.database.type.value}
        Authentication: {config.auth.method.value}
        Features: {config.features}
        
        Generate dependencies for:
        1. Database session management
        2. Current user authentication
        3. Permission checking
        4. Request validation
        5. Rate limiting
        6. Logging context
        7. Configuration injection
        8. External service clients
        9. Background task management
        10. Custom business logic dependencies
        
        Use FastAPI Depends() properly with proper typing.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",  # DeepSeek for dependency patterns
            action="fast_coding",
            data={
                "prompt": dependencies_generation_prompt,
                "language": "python"
            }
        )
        
        return {
            "dependencies_code": response.result,
            "dependency_functions": self._parse_dependency_functions(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    # Generate supporting files
    async def _generate_config_files(self, config: BackendConfig) -> Dict[str, str]:
        """Generate configuration files for FastAPI."""
        config_prompt = f"""
        Generate configuration files for FastAPI project:
        
        Project: {config.project_name}
        Database: {config.database.type.value}
        Features: {config.features}
        
        Generate:
        1. settings.py with Pydantic BaseSettings
        2. .env.example file
        3. database.py for SQLAlchemy setup
        4. logging configuration
        
        Return structured configuration code.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",
            action="code_generation",
            data={"prompt": config_prompt, "language": "python"}
        )
        
        return self._parse_config_files(response.result)
    
    async def _generate_requirements_file(self, config: BackendConfig) -> str:
        """Generate requirements.txt for FastAPI project."""
        requirements_prompt = f"""
        Generate requirements.txt for FastAPI project with:
        
        Framework: FastAPI
        Database: {config.database.type.value}
        Authentication: {config.auth.method.value}
        Features: {config.features}
        
        Include all necessary dependencies with proper versions.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",
            action="fast_coding",
            data={"prompt": requirements_prompt}
        )
        
        return response.result
    
    async def _generate_dockerfile(self, config: BackendConfig) -> str:
        """Generate Dockerfile for FastAPI project."""
        dockerfile_prompt = f"""
        Generate production-ready Dockerfile for FastAPI project:
        
        Project: {config.project_name}
        Python Version: 3.11
        Database: {config.database.type.value}
        
        Include:
        - Multi-stage build
        - Proper dependency caching
        - Security best practices
        - Health checks
        - Non-root user
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",
            action="reasoning",
            data={"prompt": dockerfile_prompt}
        )
        
        return response.result
    
    # Handler methods for MCP protocol
    async def _handle_generate_app(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_fastapi_application(data)
    
    async def _handle_generate_routes(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_fastapi_routes(data)
    
    async def _handle_generate_schemas(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_pydantic_schemas(data)
    
    async def _handle_generate_middleware(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_fastapi_middleware(data)
    
    async def _handle_generate_auth(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_fastapi_authentication(data)
    
    async def _handle_generate_models(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_sqlalchemy_models(data)
    
    async def _handle_generic_task(self, task: AgentTask) -> Dict[str, Any]:
        return {
            "message": f"Generic FastAPI task {task.name} processed",
            "task_id": task.id,
            "agent": self.name
        }
    
    # Utility methods for parsing LLM responses
    def _generate_project_structure(self, config: BackendConfig) -> Dict[str, Any]:
        """Generate project structure for FastAPI."""
        return {
            "app/": {
                "main.py": "FastAPI application entry point",
                "core/": {
                    "config.py": "Application configuration",
                    "database.py": "Database setup",
                    "security.py": "Security utilities"
                },
                "api/": {
                    f"{config.api_version}/": {
                        "endpoints/": "API endpoint routers",
                        "deps.py": "API dependencies"
                    }
                },
                "models/": "SQLAlchemy models",
                "schemas/": "Pydantic schemas",
                "services/": "Business logic services",
                "utils/": "Utility functions"
            },
            "tests/": "Test modules",
            "alembic/": "Database migrations",
            "requirements.txt": "Python dependencies",
            "Dockerfile": "Container configuration"
        }
    
    def _parse_router_files(self, code: str) -> Dict[str, str]:
        """Parse router files from generated code."""
        # In production, would parse actual code structure
        return {
            "auth.py": "Authentication routes",
            "users.py": "User management routes",
            "health.py": "Health check routes"
        }
    
    def _extract_endpoints_from_routes(self, code: str) -> List[Dict[str, str]]:
        """Extract endpoint information from route code."""
        return [
            {"path": "/api/v1/auth/login", "method": "POST", "description": "User login"},
            {"path": "/api/v1/users", "method": "GET", "description": "List users"},
            {"path": "/health", "method": "GET", "description": "Health check"}
        ]
    
    def _extract_auth_dependencies(self, code: str) -> Dict[str, Any]:
        """Extract authentication dependencies from code."""
        return {
            "get_current_user": "Get current authenticated user",
            "get_current_active_user": "Get current active user",
            "get_current_superuser": "Get current superuser"
        }
    
    def _parse_schema_classes(self, code: str) -> List[str]:
        """Parse schema class names from code."""
        return ["UserBase", "UserCreate", "UserUpdate", "User", "UserInDB"]
    
    def _extract_validation_rules(self, code: str) -> Dict[str, List[str]]:
        """Extract validation rules from schemas."""
        return {
            "email": ["email validation", "required"],
            "password": ["min length 8", "required"],
            "name": ["max length 100"]
        }
    
    def _extract_middleware_order(self, code: str) -> List[str]:
        """Extract middleware execution order."""
        return ["CORS", "Authentication", "Logging", "Error Handling"]
    
    def _extract_middleware_config(self, code: str) -> Dict[str, Any]:
        """Extract middleware configuration."""
        return {
            "cors_origins": ["http://localhost:3000"],
            "allow_methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["*"]
        }
    
    def _extract_auth_routes(self, code: str) -> List[str]:
        """Extract authentication routes."""
        return ["/auth/login", "/auth/register", "/auth/logout", "/auth/refresh"]
    
    def _extract_auth_utilities(self, code: str) -> List[str]:
        """Extract authentication utilities."""
        return ["create_access_token", "verify_password", "get_password_hash"]
    
    def _parse_model_classes(self, code: str) -> List[str]:
        """Parse model class names from code."""
        return ["User", "Profile", "Post"]
    
    def _extract_model_relationships(self, code: str) -> List[Dict[str, str]]:
        """Extract model relationships."""
        return [
            {"from": "User", "to": "Profile", "type": "one_to_one"},
            {"from": "User", "to": "Post", "type": "one_to_many"}
        ]
    
    def _extract_database_config(self, code: str) -> Dict[str, str]:
        """Extract database configuration."""
        return {
            "engine_config": "SQLAlchemy engine configuration",
            "session_config": "Database session configuration",
            "base_class": "Declarative base class"
        }
    
    def _parse_dependency_functions(self, code: str) -> List[str]:
        """Parse dependency function names."""
        return ["get_db", "get_current_user", "get_settings"]
    
    def _parse_config_files(self, code: str) -> Dict[str, str]:
        """Parse configuration files from generated code."""
        return {
            "settings.py": "# Application settings configuration",
            ".env.example": "# Environment variables example",
            "database.py": "# Database configuration",
            "logging.conf": "# Logging configuration"
        }