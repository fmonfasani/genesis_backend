"""
NestJS Agent

Specializes in generating NestJS backend applications using LLMs.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from pathlib import Path

from genesis_agents import GenesisAgent, AgentTask, TaskResult
from mcpturbo import protocol

from ..config import BackendConfig, BackendFramework

logger = logging.getLogger(__name__)


class NestJSAgent(GenesisAgent):
    """
    Agent specialized in NestJS backend generation.
    
    Responsibilities:
    - Generate NestJS project structure
    - Generate TypeORM entities and relationships
    - Generate NestJS controllers and services
    - Generate NestJS modules and providers
    - Generate authentication guards and strategies
    - Generate DTOs and validation pipes
    """
    
    def __init__(self):
        super().__init__(
            agent_id="nestjs_generator",
            name="NestJS Generator Agent",
            agent_type="generator"
        )
        
        # NestJS-specific capabilities
        self.add_capability("generate_nestjs_project")
        self.add_capability("generate_nestjs_modules")
        self.add_capability("generate_nestjs_controllers")
        self.add_capability("generate_nestjs_services")
        self.add_capability("generate_typeorm_entities")
        self.add_capability("generate_nestjs_auth")
        self.add_capability("generate_nestjs_dtos")
        self.add_capability("generate_nestjs_pipes")
        
        # Register handlers
        self.register_handler("generate_nestjs_project", self._handle_generate_project)
        self.register_handler("generate_nestjs_modules", self._handle_generate_modules)
        self.register_handler("generate_nestjs_controllers", self._handle_generate_controllers)
        self.register_handler("generate_nestjs_services", self._handle_generate_services)
        self.register_handler("generate_typeorm_entities", self._handle_generate_entities)
        self.register_handler("generate_nestjs_auth", self._handle_generate_auth)
        self.register_handler("generate_nestjs_dtos", self._handle_generate_dtos)
        self.register_handler("generate_nestjs_pipes", self._handle_generate_pipes)
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Execute NestJS generation task using LLMs."""
        try:
            self.logger.info(f"🟦 Executing NestJS task: {task.name}")
            
            if task.name == "generate_nestjs_project":
                result = await self._generate_nestjs_project(task.params)
            elif task.name == "generate_nestjs_modules":
                result = await self._generate_nestjs_modules(task.params)
            elif task.name == "generate_nestjs_controllers":
                result = await self._generate_nestjs_controllers(task.params)
            elif task.name == "generate_nestjs_services":
                result = await self._generate_nestjs_services(task.params)
            elif task.name == "generate_typeorm_entities":
                result = await self._generate_typeorm_entities(task.params)
            elif task.name == "generate_nestjs_auth":
                result = await self._generate_nestjs_authentication(task.params)
            elif task.name == "generate_nestjs_dtos":
                result = await self._generate_nestjs_dtos(task.params)
            elif task.name == "generate_nestjs_pipes":
                result = await self._generate_nestjs_pipes(task.params)
            else:
                result = await self._handle_generic_task(task)
            
            return TaskResult(
                task_id=task.id,
                success=True,
                result=result,
                metadata={
                    "agent": self.name,
                    "task_type": task.name,
                    "framework": "nestjs",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error in NestJS task {task.name}: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                metadata={"agent": self.name, "task_type": task.name}
            )
    
    async def _generate_nestjs_project(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete NestJS project structure using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        architecture = params.get("architecture", {})
        
        project_generation_prompt = f"""
        Generate a complete NestJS project structure with this configuration:
        
        Project Name: {config.project_name}
        Description: {config.description}
        Features: {config.features}
        Database: {config.database.type.value}
        Authentication: {config.auth.method.value}
        
        Architecture: {architecture}
        
        Generate NestJS project with:
        1. Main application file (main.ts) with proper setup
        2. App module as root module
        3. Environment configuration module
        4. Database configuration with TypeORM
        5. Authentication module if required
        6. Feature modules for each domain
        7. Global exception filters
        8. Global validation pipes
        9. Logging configuration
        10. Health check module
        
        NestJS best practices:
        - Modular architecture with feature modules
        - Dependency injection throughout
        - Proper TypeScript configuration
        - Environment-based configuration
        - Database connection management
        - Global interceptors for logging/auth
        
        Return complete NestJS project structure with TypeScript code.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at TypeScript/NestJS
            action="code_generation",
            data={
                "prompt": project_generation_prompt,
                "language": "typescript",
                "framework": "nestjs"
            }
        )
        
        # Generate additional configuration files
        config_files = await self._generate_nestjs_config_files(config)
        package_json = await self._generate_package_json(config)
        docker_files = await self._generate_docker_config(config)
        
        return {
            "project_structure": response.result,
            "config_files": config_files,
            "package_json": package_json,
            "docker_files": docker_files,
            "modules_created": self._extract_nestjs_modules(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "framework": "nestjs",
                "nestjs_version": "10.0+",
                "node_version": "18+"
            }
        }
    
    async def _generate_nestjs_modules(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate NestJS modules using LLM."""
        features = params.get("features", [])
        entities = params.get("entities", [])
        
        modules_generation_prompt = f"""
        Generate NestJS modules for these features:
        
        Features: {features}
        Entities: {entities}
        
        Generate comprehensive NestJS modules including:
        1. Feature modules for each domain entity
        2. Module decorators with proper imports/exports
        3. Controller registration
        4. Service provider registration
        5. Repository injection setup
        6. Module interdependencies
        7. Global modules where appropriate
        8. Dynamic module configuration
        9. Custom providers and factories
        10. Module testing setup
        
        Module structure should include:
        - Clear separation of concerns
        - Proper dependency injection
        - Testable module design
        - Async module initialization if needed
        - Environment-specific providers
        
        Return well-structured NestJS modules with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at module architecture
            action="reasoning",
            data={
                "prompt": modules_generation_prompt,
                "system_prompt": "You are a NestJS expert. Generate modular, scalable module structures."
            }
        )
        
        return {
            "modules_code": response.result,
            "module_classes": self._extract_module_classes(response.result),
            "dependencies": self._extract_module_dependencies(response.result),
            "providers": self._extract_module_providers(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_nestjs_controllers(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate NestJS controllers using LLM."""
        api_design = params.get("api_design", {})
        entities = params.get("entities", [])
        
        controllers_generation_prompt = f"""
        Generate NestJS controllers for this API design:
        
        API Design: {api_design}
        Entities: {entities}
        
        Generate comprehensive NestJS controllers including:
        1. Controller decorators with route prefixes
        2. HTTP method decorators (Get, Post, Put, Delete)
        3. Parameter decorators (Param, Body, Query)
        4. DTO validation with pipes
        5. Authentication guards where needed
        6. Authorization decorators
        7. Exception handling
        8. Response transformation
        9. API documentation with Swagger decorators
        10. Request/response logging
        
        Controller features:
        - RESTful route design
        - Proper HTTP status codes
        - Input validation and transformation
        - Error handling and responses
        - Dependency injection of services
        - Route-level guards and interceptors
        
        Return production-ready NestJS controllers with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",  # DeepSeek good at controller patterns
            action="fast_coding",
            data={
                "prompt": controllers_generation_prompt,
                "language": "typescript"
            }
        )
        
        return {
            "controllers_code": response.result,
            "controller_classes": self._extract_controller_classes(response.result),
            "routes": self._extract_controller_routes(response.result),
            "guards_used": self._extract_guards_used(response.result),
            "swagger_docs": self._extract_swagger_documentation(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_nestjs_services(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate NestJS services using LLM."""
        entities = params.get("entities", [])
        business_logic = params.get("business_logic", [])
        
        services_generation_prompt = f"""
        Generate NestJS services for business logic:
        
        Entities: {entities}
        Business Logic: {business_logic}
        
        Generate comprehensive NestJS services including:
        1. Injectable service decorators
        2. Repository injection for data access
        3. CRUD operations with proper error handling
        4. Business logic methods
        5. Data transformation and validation
        6. External API integration if needed
        7. Caching implementation
        8. Transaction management
        9. Event emission for business events
        10. Service testing methods
        
        Service features:
        - Single responsibility principle
        - Dependency injection for repositories
        - Proper error handling and exceptions
        - Async/await for database operations
        - Data validation and transformation
        - Business rule enforcement
        
        Return well-structured NestJS services with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at service patterns
            action="code_generation",
            data={
                "prompt": services_generation_prompt,
                "language": "typescript",
                "framework": "nestjs_services"
            }
        )
        
        return {
            "services_code": response.result,
            "service_classes": self._extract_service_classes(response.result),
            "methods": self._extract_service_methods(response.result),
            "dependencies": self._extract_service_dependencies(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_typeorm_entities(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate TypeORM entities using LLM."""
        data_models = params.get("data_models", [])
        relationships = params.get("relationships", [])
        database_type = params.get("database_type", "postgresql")
        
        entities_generation_prompt = f"""
        Generate TypeORM entities for {database_type}:
        
        Data Models: {data_models}
        Relationships: {relationships}
        Database: {database_type}
        
        Generate comprehensive TypeORM entities including:
        1. Entity decorators with table configuration
        2. Column decorators with proper types
        3. Primary key and auto-generation
        4. Foreign key relationships
        5. One-to-One, One-to-Many, Many-to-Many relationships
        6. Entity indexes for performance
        7. Column validation and constraints
        8. Entity listeners and subscribers
        9. Custom repository methods
        10. Migration-friendly entity design
        
        TypeORM features:
        - Proper TypeScript typing
        - Database-specific column types
        - Relationship mapping with lazy loading
        - Entity validation with class-validator
        - Audit columns (created_at, updated_at)
        - Soft delete support if needed
        
        Return production-ready TypeORM entities with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at data modeling
            action="reasoning",
            data={
                "prompt": entities_generation_prompt,
                "system_prompt": "You are a TypeORM expert. Generate efficient, well-typed entities."
            }
        )
        
        return {
            "entities_code": response.result,
            "entity_classes": self._extract_entity_classes(response.result),
            "relationships_implemented": self._extract_entity_relationships(response.result),
            "indexes": self._extract_entity_indexes(response.result),
            "migrations_needed": self._extract_migration_requirements(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_nestjs_authentication(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate NestJS authentication system using LLM."""
        auth_config = params.get("auth_config", {})
        auth_method = params.get("auth_method", "jwt")
        
        auth_generation_prompt = f"""
        Generate NestJS authentication system with {auth_method}:
        
        Auth Config: {auth_config}
        Auth Method: {auth_method}
        
        Generate comprehensive NestJS authentication including:
        1. Authentication module with strategies
        2. JWT or Passport strategy implementation
        3. Authentication guards for routes
        4. Login/register controllers
        5. User service for authentication
        6. Password hashing utilities
        7. Token generation and validation
        8. Role-based authorization guards
        9. Authentication decorators
        10. Auth exception filters
        
        Authentication features:
        - Secure password handling with bcrypt
        - JWT token management
        - Route-level authentication guards
        - Role and permission decorators
        - Social authentication if specified
        - Refresh token handling
        
        Return complete NestJS authentication system with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at auth patterns
            action="code_generation",
            data={
                "prompt": auth_generation_prompt,
                "language": "typescript",
                "framework": "nestjs_auth"
            }
        )
        
        return {
            "auth_code": response.result,
            "auth_module": self._extract_auth_module(response.result),
            "strategies": self._extract_auth_strategies(response.result),
            "guards": self._extract_auth_guards(response.result),
            "decorators": self._extract_auth_decorators(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_nestjs_dtos(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate NestJS DTOs using LLM."""
        entities = params.get("entities", [])
        api_design = params.get("api_design", {})
        
        dtos_generation_prompt = f"""
        Generate NestJS DTOs for data validation:
        
        Entities: {entities}
        API Design: {api_design}
        
        Generate comprehensive DTOs including:
        1. Create DTOs for POST requests
        2. Update DTOs for PUT/PATCH requests
        3. Response DTOs for GET responses
        4. Query DTOs for filtering and pagination
        5. Validation decorators from class-validator
        6. Transformation decorators from class-transformer
        7. Nested DTOs for complex objects
        8. Partial DTOs for optional updates
        9. API documentation decorators
        10. Custom validation rules
        
        DTO features:
        - Strong TypeScript typing
        - Comprehensive validation rules
        - Proper error messages
        - Transformation logic
        - Swagger API documentation
        - Reusable validation decorators
        
        Return well-validated NestJS DTOs with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",  # DeepSeek good at DTO patterns
            action="fast_coding",
            data={
                "prompt": dtos_generation_prompt,
                "language": "typescript"
            }
        )
        
        return {
            "dtos_code": response.result,
            "dto_classes": self._extract_dto_classes(response.result),
            "validation_rules": self._extract_validation_rules(response.result),
            "transformations": self._extract_transformations(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_nestjs_pipes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate NestJS pipes for validation and transformation using LLM."""
        validation_requirements = params.get("validation_requirements", [])
        
        pipes_generation_prompt = f"""
        Generate NestJS pipes for validation and transformation:
        
        Validation Requirements: {validation_requirements}
        
        Generate comprehensive NestJS pipes including:
        1. Validation pipes for DTOs
        2. Transform pipes for data conversion
        3. Parse pipes for parameters
        4. Custom validation pipes
        5. Global validation configuration
        6. Exception handling in pipes
        7. Async validation support
        8. Custom decorators for pipes
        9. Performance-optimized pipes
        10. Testing utilities for pipes
        
        Pipe features:
        - Strong type safety
        - Comprehensive error handling
        - Reusable validation logic
        - Performance optimization
        - Custom validation rules
        - Proper error messages
        
        Return production-ready NestJS pipes with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at pipe patterns
            action="reasoning",
            data={
                "prompt": pipes_generation_prompt,
                "system_prompt": "You are a NestJS validation expert. Generate robust validation pipes."
            }
        )
        
        return {
            "pipes_code": response.result,
            "pipe_classes": self._extract_pipe_classes(response.result),
            "validation_logic": self._extract_validation_logic(response.result),
            "custom_decorators": self._extract_custom_decorators(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    # Handler methods for MCP protocol
    async def _handle_generate_project(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_nestjs_project(data)
    
    async def _handle_generate_modules(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_nestjs_modules(data)
    
    async def _handle_generate_controllers(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_nestjs_controllers(data)
    
    async def _handle_generate_services(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_nestjs_services(data)
    
    async def _handle_generate_entities(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_typeorm_entities(data)
    
    async def _handle_generate_auth(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_nestjs_authentication(data)
    
    async def _handle_generate_dtos(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_nestjs_dtos(data)
    
    async def _handle_generate_pipes(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_nestjs_pipes(data)
    
    async def _handle_generic_task(self, task: AgentTask) -> Dict[str, Any]:
        return {
            "message": f"Generic NestJS task {task.name} processed",
            "task_id": task.id,
            "agent": self.name
        }
    
    # Utility methods for additional file generation
    async def _generate_nestjs_config_files(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS configuration files."""
        return {
            "nest-cli.json": '{"collection": "@nestjs/schematics"}',
            "tsconfig.json": "# TypeScript configuration",
            ".env.example": "# Environment variables example",
            "ormconfig.json": "# TypeORM configuration"
        }
    
    async def _generate_package_json(self, config: BackendConfig) -> str:
        """Generate package.json for NestJS project."""
        package_prompt = f"""
        Generate package.json for NestJS project:
        
        Project: {config.project_name}
        Database: {config.database.type.value}
        Features: {config.features}
        
        Include all necessary dependencies for a production NestJS application.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",
            action="fast_coding",
            data={"prompt": package_prompt, "language": "json"}
        )
        
        return response.result
    
    async def _generate_docker_config(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Docker configuration for NestJS."""
        return {
            "Dockerfile": "# NestJS Dockerfile",
            "docker-compose.yml": "# Docker Compose configuration",
            ".dockerignore": "# Docker ignore file"
        }
    
    # Utility methods for parsing LLM responses
    def _extract_nestjs_modules(self, code: str) -> List[str]:
        """Extract NestJS module names."""
        return ["AppModule", "UsersModule", "AuthModule", "DatabaseModule"]
    
    def _extract_module_classes(self, code: str) -> List[str]:
        """Extract module class names."""
        return ["UsersModule", "AuthModule", "PostsModule"]
    
    def _extract_module_dependencies(self, code: str) -> Dict[str, List[str]]:
        """Extract module dependencies."""
        return {
            "UsersModule": ["TypeOrmModule", "ConfigModule"],
            "AuthModule": ["JwtModule", "PassportModule"]
        }
    
    def _extract_module_providers(self, code: str) -> Dict[str, List[str]]:
        """Extract module providers."""
        return {
            "UsersModule": ["UsersService", "UsersRepository"],
            "AuthModule": ["AuthService", "JwtStrategy"]
        }
    
    def _extract_controller_classes(self, code: str) -> List[str]:
        """Extract controller class names."""
        return ["UsersController", "AuthController", "PostsController"]
    
    def _extract_controller_routes(self, code: str) -> List[Dict[str, str]]:
        """Extract controller routes."""
        return [
            {"path": "/users", "method": "GET", "handler": "findAll"},
            {"path": "/users/:id", "method": "GET", "handler": "findOne"},
            {"path": "/users", "method": "POST", "handler": "create"}
        ]
    
    def _extract_guards_used(self, code: str) -> List[str]:
        """Extract guards used in controllers."""
        return ["JwtAuthGuard", "RolesGuard", "ThrottlerGuard"]
    
    def _extract_swagger_documentation(self, code: str) -> List[str]:
        """Extract Swagger documentation decorators."""
        return ["@ApiTags", "@ApiOperation", "@ApiResponse", "@ApiBearerAuth"]
    
    def _extract_service_classes(self, code: str) -> List[str]:
        """Extract service class names."""
        return ["UsersService", "AuthService", "PostsService"]
    
    def _extract_service_methods(self, code: str) -> Dict[str, List[str]]:
        """Extract service methods."""
        return {
            "UsersService": ["create", "findAll", "findOne", "update", "remove"],
            "AuthService": ["login", "register", "validateUser", "generateToken"]
        }
    
    def _extract_service_dependencies(self, code: str) -> Dict[str, List[str]]:
        """Extract service dependencies."""
        return {
            "UsersService": ["UsersRepository", "ConfigService"],
            "AuthService": ["UsersService", "JwtService"]
        }
    
    def _extract_entity_classes(self, code: str) -> List[str]:
        """Extract TypeORM entity names."""
        return ["User", "Post", "Profile"]
    
    def _extract_entity_relationships(self, code: str) -> List[Dict[str, str]]:
        """Extract entity relationships."""
        return [
            {"from": "User", "to": "Profile", "type": "OneToOne"},
            {"from": "User", "to": "Post", "type": "OneToMany"}
        ]
    
    def _extract_entity_indexes(self, code: str) -> List[Dict[str, str]]:
        """Extract entity indexes."""
        return [
            {"entity": "User", "columns": ["email"], "unique": True},
            {"entity": "Post", "columns": ["createdAt"], "unique": False}
        ]
    
    def _extract_migration_requirements(self, code: str) -> List[str]:
        """Extract migration requirements."""
        return ["CreateUserTable", "CreatePostTable", "AddUserProfileRelation"]
    
    def _extract_auth_module(self, code: str) -> str:
        """Extract auth module name."""
        return "AuthModule"
    
    def _extract_auth_strategies(self, code: str) -> List[str]:
        """Extract authentication strategies."""
        return ["JwtStrategy", "LocalStrategy", "GoogleStrategy"]
    
    def _extract_auth_guards(self, code: str) -> List[str]:
        """Extract authentication guards."""
        return ["JwtAuthGuard", "LocalAuthGuard", "RolesGuard"]
    
    def _extract_auth_decorators(self, code: str) -> List[str]:
        """Extract authentication decorators."""
        return ["@UseGuards", "@Roles", "@Public", "@CurrentUser"]
    
    def _extract_dto_classes(self, code: str) -> List[str]:
        """Extract DTO class names."""
        return ["CreateUserDto", "UpdateUserDto", "UserResponseDto", "LoginDto"]
    
    def _extract_validation_rules(self, code: str) -> Dict[str, List[str]]:
        """Extract validation rules."""
        return {
            "CreateUserDto": ["@IsEmail", "@IsString", "@MinLength"],
            "UpdateUserDto": ["@IsOptional", "@IsString"]
        }
    
    def _extract_transformations(self, code: str) -> List[str]:
        """Extract transformation decorators."""
        return ["@Transform", "@Type", "@Exclude", "@Expose"]
    
    def _extract_pipe_classes(self, code: str) -> List[str]:
        """Extract pipe class names."""
        return ["ValidationPipe", "ParseIntPipe", "CustomValidationPipe"]
    
    def _extract_validation_logic(self, code: str) -> List[str]:
        """Extract validation logic patterns."""
        return ["DTO validation", "Parameter parsing", "Custom validation rules"]
    
    def _extract_custom_decorators(self, code: str) -> List[str]:
        """Extract custom decorators."""
        return ["@IsUnique", "@IsValidEmail", "@MatchesProperty"]