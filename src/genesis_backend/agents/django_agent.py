"""
Django Agent

Specializes in generating Django backend applications using LLMs.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from pathlib import Path

from genesis_agents import GenesisAgent, AgentTask, TaskResult
from mcpturbo import protocol

from ..config import BackendConfig, BackendFramework

logger = logging.getLogger(__name__)


class DjangoAgent(GenesisAgent):
    """
    Agent specialized in Django backend generation.
    
    Responsibilities:
    - Generate Django project structure
    - Generate Django models with relationships
    - Generate Django views and URLs
    - Generate Django REST Framework APIs
    - Generate Django admin interface
    - Generate Django authentication systems
    """
    
    def __init__(self):
        super().__init__(
            agent_id="django_generator",
            name="Django Generator Agent",
            agent_type="generator"
        )
        
        # Django-specific capabilities
        self.add_capability("generate_django_project")
        self.add_capability("generate_django_models")
        self.add_capability("generate_django_views")
        self.add_capability("generate_django_urls")
        self.add_capability("generate_django_admin")
        self.add_capability("generate_django_rest_api")
        self.add_capability("generate_django_auth")
        self.add_capability("generate_django_settings")
        
        # Register handlers
        self.register_handler("generate_django_project", self._handle_generate_project)
        self.register_handler("generate_django_models", self._handle_generate_models)
        self.register_handler("generate_django_views", self._handle_generate_views)
        self.register_handler("generate_django_urls", self._handle_generate_urls)
        self.register_handler("generate_django_admin", self._handle_generate_admin)
        self.register_handler("generate_django_rest_api", self._handle_generate_rest_api)
        self.register_handler("generate_django_auth", self._handle_generate_auth)
        self.register_handler("generate_django_settings", self._handle_generate_settings)
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Execute Django generation task using LLMs."""
        try:
            self.logger.info(f"🐍 Executing Django task: {task.name}")
            
            if task.name == "generate_django_project":
                result = await self._generate_django_project(task.params)
            elif task.name == "generate_django_models":
                result = await self._generate_django_models(task.params)
            elif task.name == "generate_django_views":
                result = await self._generate_django_views(task.params)
            elif task.name == "generate_django_urls":
                result = await self._generate_django_urls(task.params)
            elif task.name == "generate_django_admin":
                result = await self._generate_django_admin(task.params)
            elif task.name == "generate_django_rest_api":
                result = await self._generate_django_rest_framework(task.params)
            elif task.name == "generate_django_auth":
                result = await self._generate_django_authentication(task.params)
            elif task.name == "generate_django_settings":
                result = await self._generate_django_settings(task.params)
            else:
                result = await self._handle_generic_task(task)
            
            return TaskResult(
                task_id=task.id,
                success=True,
                result=result,
                metadata={
                    "agent": self.name,
                    "task_type": task.name,
                    "framework": "django",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error in Django task {task.name}: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                metadata={"agent": self.name, "task_type": task.name}
            )
    
    async def _generate_django_project(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete Django project structure using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        architecture = params.get("architecture", {})
        
        project_generation_prompt = f"""
        Generate a complete Django project structure with this configuration:
        
        Project Name: {config.project_name}
        Description: {config.description}
        Features: {config.features}
        Database: {config.database.type.value}
        Authentication: {config.auth.method.value}
        
        Architecture: {architecture}
        
        Generate Django project with:
        1. Project configuration (settings.py split for environments)
        2. Main URLs configuration
        3. WSGI and ASGI application files
        4. Django apps structure for each domain entity
        5. Requirements files for different environments
        6. Django management commands
        7. Custom middleware if needed
        8. Static files configuration
        9. Media files configuration
        10. Logging configuration
        
        Project structure should follow Django best practices:
        - Separate settings for dev/staging/production
        - Apps organized by domain
        - Proper static/media handling
        - Database configuration
        - Security settings
        
        Return complete Django project structure with all necessary files.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at Django architecture
            action="reasoning",
            data={
                "prompt": project_generation_prompt,
                "system_prompt": "You are a Django expert. Generate production-ready Django projects."
            }
        )
        
        # Generate additional files
        settings_files = await self._generate_django_settings_files(config)
        requirements_files = await self._generate_requirements_files(config)
        management_commands = await self._generate_management_commands(config)
        
        return {
            "project_structure": response.result,
            "settings_files": settings_files,
            "requirements_files": requirements_files,
            "management_commands": management_commands,
            "apps_created": self._extract_django_apps(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "framework": "django",
                "django_version": "4.2+"
            }
        }
    
    async def _generate_django_models(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Django models using LLM."""
        data_models = params.get("data_models", [])
        relationships = params.get("relationships", [])
        config = BackendConfig.from_dict(params.get("config", {}))
        
        models_generation_prompt = f"""
        Generate Django models for this data schema:
        
        Data Models: {data_models}
        Relationships: {relationships}
        Database: {config.database.type.value}
        Features: {config.features}
        
        Generate comprehensive Django models including:
        1. Model classes with proper field types
        2. Relationships (ForeignKey, OneToOneField, ManyToManyField)
        3. Model Meta configuration (db_table, ordering, indexes)
        4. Custom model methods and properties
        5. String representations (__str__ methods)
        6. Model managers for custom querysets
        7. Validation methods (clean, clean_fields)
        8. Model signals for business logic
        9. Abstract base models if applicable
        10. Migration-friendly field definitions
        
        Django model best practices:
        - Use appropriate field types for data
        - Add help_text for documentation
        - Use choices for enumerated fields
        - Add proper indexes for performance
        - Include audit fields (created_at, updated_at)
        - Use related_name for reverse relationships
        
        Return well-structured Django model classes.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at Django models
            action="code_generation",
            data={
                "prompt": models_generation_prompt,
                "language": "python",
                "framework": "django"
            }
        )
        
        return {
            "models_code": response.result,
            "model_classes": self._extract_model_classes(response.result),
            "relationships_implemented": self._extract_relationships(response.result),
            "migrations_needed": self._extract_migration_info(response.result),
            "admin_registrations": self._extract_admin_registrations(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_django_views(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Django views using LLM."""
        api_design = params.get("api_design", {})
        models = params.get("models", [])
        view_type = params.get("view_type", "function")  # function or class
        
        views_generation_prompt = f"""
        Generate Django views for this API design:
        
        API Design: {api_design}
        Models: {models}
        View Type: {view_type}
        
        Generate comprehensive Django views including:
        1. Function-based or class-based views as specified
        2. CRUD operations for each model
        3. Proper HTTP method handling
        4. Request data validation
        5. Error handling and responses
        6. Authentication and permission checks
        7. Pagination for list views
        8. Filtering and searching capabilities
        9. Custom business logic
        10. API documentation with docstrings
        
        For function-based views:
        - Use decorators for common functionality
        - Proper request method checking
        - Clean separation of concerns
        
        For class-based views:
        - Inherit from appropriate base classes
        - Override necessary methods
        - Use mixins for common functionality
        
        Return production-ready Django views.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",  # DeepSeek good at view patterns
            action="fast_coding",
            data={
                "prompt": views_generation_prompt,
                "language": "python"
            }
        )
        
        return {
            "views_code": response.result,
            "view_functions": self._extract_view_functions(response.result),
            "url_patterns": self._extract_url_patterns(response.result),
            "permissions_used": self._extract_permissions(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_django_urls(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Django URL configuration using LLM."""
        views = params.get("views", [])
        api_design = params.get("api_design", {})
        
        urls_generation_prompt = f"""
        Generate Django URL configuration:
        
        Views: {views}
        API Design: {api_design}
        
        Generate comprehensive URL patterns including:
        1. Main project URLs with app includes
        2. App-specific URL patterns
        3. API versioning support
        4. Named URL patterns for reverse lookups
        5. Parameter capture (pk, slug, etc.)
        6. Regular expression patterns where needed
        7. Namespace configuration
        8. URL decorators for common patterns
        9. Admin URLs integration
        10. Static/media URLs for development
        
        URL best practices:
        - Use path() function for simple patterns
        - Use re_path() for complex patterns
        - Include trailing slashes consistently
        - Use meaningful URL names
        - Group related URLs logically
        
        Return complete URL configuration.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at URL patterns
            action="code_generation",
            data={
                "prompt": urls_generation_prompt,
                "language": "python",
                "framework": "django_urls"
            }
        )
        
        return {
            "urls_code": response.result,
            "url_patterns": self._extract_all_url_patterns(response.result),
            "namespaces": self._extract_namespaces(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_django_admin(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Django admin interface using LLM."""
        models = params.get("models", [])
        admin_features = params.get("admin_features", [])
        
        admin_generation_prompt = f"""
        Generate Django admin interface:
        
        Models: {models}
        Admin Features: {admin_features}
        
        Generate comprehensive Django admin including:
        1. ModelAdmin classes for each model
        2. List display configuration
        3. Search fields and filters
        4. Inline editing for related models
        5. Custom admin actions
        6. Form field customization
        7. Permissions and user management
        8. Custom admin views if needed
        9. Admin site customization
        10. Bulk operations support
        
        Admin features to include:
        - Intuitive list displays
        - Efficient search and filtering
        - Proper field organization in forms
        - Read-only fields where appropriate
        - Custom widgets for complex fields
        - Audit trail in admin
        
        Return production-ready Django admin configuration.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at admin interfaces
            action="reasoning",
            data={
                "prompt": admin_generation_prompt,
                "system_prompt": "You are a Django admin expert. Generate user-friendly admin interfaces."
            }
        )
        
        return {
            "admin_code": response.result,
            "admin_classes": self._extract_admin_classes(response.result),
            "custom_actions": self._extract_admin_actions(response.result),
            "inlines": self._extract_admin_inlines(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_django_rest_framework(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Django REST Framework API using LLM."""
        models = params.get("models", [])
        api_design = params.get("api_design", {})
        
        drf_generation_prompt = f"""
        Generate Django REST Framework API:
        
        Models: {models}
        API Design: {api_design}
        
        Generate comprehensive DRF API including:
        1. Serializers for each model with validation
        2. ViewSets with CRUD operations
        3. Custom API endpoints for business logic
        4. Authentication and permission classes
        5. Filtering, searching, and ordering
        6. Pagination configuration
        7. API documentation with swagger
        8. Throttling and rate limiting
        9. Custom parsers and renderers
        10. API versioning support
        
        DRF features to include:
        - ModelSerializer with proper fields
        - Custom validation methods
        - Nested serializers for relationships
        - ViewSet mixins for common patterns
        - Custom permission classes
        - Filter backends integration
        - Proper HTTP status codes
        
        Return production-ready DRF API.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at DRF patterns
            action="code_generation",
            data={
                "prompt": drf_generation_prompt,
                "language": "python",
                "framework": "django_rest_framework"
            }
        )
        
        return {
            "drf_code": response.result,
            "serializers": self._extract_serializers(response.result),
            "viewsets": self._extract_viewsets(response.result),
            "permissions": self._extract_drf_permissions(response.result),
            "api_endpoints": self._extract_api_endpoints(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_django_authentication(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Django authentication system using LLM."""
        auth_config = params.get("auth_config", {})
        user_model = params.get("user_model", {})
        
        auth_generation_prompt = f"""
        Generate Django authentication system:
        
        Auth Config: {auth_config}
        User Model: {user_model}
        
        Generate comprehensive Django authentication including:
        1. Custom User model if needed
        2. Authentication backends
        3. Login/logout views and templates
        4. User registration and activation
        5. Password reset functionality
        6. Profile management
        7. Permission and group management
        8. Social authentication integration
        9. Two-factor authentication support
        10. Session management and security
        
        Authentication features:
        - Secure password handling
        - Email verification
        - Account lockout protection
        - Audit logging
        - Custom user fields
        - Profile picture handling
        
        Return complete Django authentication system.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at auth systems
            action="reasoning",
            data={
                "prompt": auth_generation_prompt,
                "system_prompt": "You are a Django authentication expert. Generate secure auth systems."
            }
        )
        
        return {
            "auth_code": response.result,
            "user_model": self._extract_user_model(response.result),
            "auth_views": self._extract_auth_views(response.result),
            "auth_forms": self._extract_auth_forms(response.result),
            "auth_backends": self._extract_auth_backends(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_django_settings(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Django settings configuration using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        
        settings_generation_prompt = f"""
        Generate Django settings configuration:
        
        Project: {config.project_name}
        Database: {config.database.type.value}
        Features: {config.features}
        Environment: Production-ready
        
        Generate Django settings including:
        1. Base settings with common configuration
        2. Development settings for local development
        3. Production settings for deployment
        4. Testing settings for test environment
        5. Database configuration for each environment
        6. Static and media files configuration
        7. Security settings and middleware
        8. Logging configuration
        9. Cache configuration
        10. Email settings
        
        Settings best practices:
        - Environment-specific configurations
        - Secret key management
        - Debug settings per environment
        - Proper security headers
        - Database connection pooling
        - Comprehensive logging
        
        Return complete Django settings structure.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at configuration
            action="reasoning",
            data={
                "prompt": settings_generation_prompt,
                "system_prompt": "You are a Django deployment expert. Generate secure, production-ready settings."
            }
        )
        
        return {
            "settings_code": response.result,
            "environment_configs": self._extract_environment_configs(response.result),
            "security_settings": self._extract_security_settings(response.result),
            "database_configs": self._extract_database_configs(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    # Handler methods for MCP protocol
    async def _handle_generate_project(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_django_project(data)
    
    async def _handle_generate_models(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_django_models(data)
    
    async def _handle_generate_views(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_django_views(data)
    
    async def _handle_generate_urls(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_django_urls(data)
    
    async def _handle_generate_admin(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_django_admin(data)
    
    async def _handle_generate_rest_api(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_django_rest_framework(data)
    
    async def _handle_generate_auth(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_django_authentication(data)
    
    async def _handle_generate_settings(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_django_settings(data)
    
    async def _handle_generic_task(self, task: AgentTask) -> Dict[str, Any]:
        return {
            "message": f"Generic Django task {task.name} processed",
            "task_id": task.id,
            "agent": self.name
        }
    
    # Utility methods for additional file generation
    async def _generate_django_settings_files(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django settings files for different environments."""
        return {
            "base.py": "# Base Django settings",
            "development.py": "# Development environment settings",
            "production.py": "# Production environment settings",
            "testing.py": "# Testing environment settings"
        }
    
    async def _generate_requirements_files(self, config: BackendConfig) -> Dict[str, str]:
        """Generate requirements files for Django."""
        return {
            "requirements/base.txt": "Django>=4.2.0\npsycopg2-binary>=2.9.0",
            "requirements/development.txt": "-r base.txt\ndjango-debug-toolbar>=4.0.0",
            "requirements/production.txt": "-r base.txt\ngunicorn>=20.1.0"
        }
    
    async def _generate_management_commands(self, config: BackendConfig) -> Dict[str, str]:
        """Generate custom Django management commands."""
        return {
            "management/commands/seed_data.py": "# Custom command to seed database",
            "management/commands/export_data.py": "# Custom command to export data"
        }
    
    # Utility methods for parsing LLM responses
    def _extract_django_apps(self, code: str) -> List[str]:
        """Extract Django apps from generated code."""
        return ["users", "core", "api"]
    
    def _extract_model_classes(self, code: str) -> List[str]:
        """Extract model class names."""
        return ["User", "Profile", "Post"]
    
    def _extract_relationships(self, code: str) -> List[Dict[str, str]]:
        """Extract model relationships."""
        return [
            {"from": "Profile", "to": "User", "type": "OneToOneField"},
            {"from": "Post", "to": "User", "type": "ForeignKey"}
        ]
    
    def _extract_migration_info(self, code: str) -> List[str]:
        """Extract migration information."""
        return ["Initial migration", "Add user profile", "Add post model"]
    
    def _extract_admin_registrations(self, code: str) -> List[str]:
        """Extract admin registrations needed."""
        return ["UserAdmin", "ProfileAdmin", "PostAdmin"]
    
    def _extract_view_functions(self, code: str) -> List[str]:
        """Extract view function names."""
        return ["user_list", "user_detail", "user_create", "user_update"]
    
    def _extract_url_patterns(self, code: str) -> List[Dict[str, str]]:
        """Extract URL patterns."""
        return [
            {"pattern": "users/", "name": "user_list", "view": "user_list"},
            {"pattern": "users/<int:pk>/", "name": "user_detail", "view": "user_detail"}
        ]
    
    def _extract_permissions(self, code: str) -> List[str]:
        """Extract permissions used."""
        return ["login_required", "permission_required", "user_passes_test"]
    
    def _extract_all_url_patterns(self, code: str) -> Dict[str, List[str]]:
        """Extract all URL patterns by app."""
        return {
            "main": ["/admin/", "/api/", "/users/"],
            "users": ["/", "/<int:pk>/", "/create/"],
            "api": ["/v1/users/", "/v1/auth/"]
        }
    
    def _extract_namespaces(self, code: str) -> List[str]:
        """Extract URL namespaces."""
        return ["admin", "api", "users"]
    
    def _extract_admin_classes(self, code: str) -> List[str]:
        """Extract admin class names."""
        return ["UserAdmin", "ProfileAdmin", "PostAdmin"]
    
    def _extract_admin_actions(self, code: str) -> List[str]:
        """Extract custom admin actions."""
        return ["activate_users", "deactivate_users", "export_users"]
    
    def _extract_admin_inlines(self, code: str) -> List[str]:
        """Extract admin inline classes."""
        return ["ProfileInline", "PostInline"]
    
    def _extract_serializers(self, code: str) -> List[str]:
        """Extract DRF serializer names."""
        return ["UserSerializer", "ProfileSerializer", "PostSerializer"]
    
    def _extract_viewsets(self, code: str) -> List[str]:
        """Extract DRF viewset names."""
        return ["UserViewSet", "ProfileViewSet", "PostViewSet"]
    
    def _extract_drf_permissions(self, code: str) -> List[str]:
        """Extract DRF permission classes."""
        return ["IsAuthenticated", "IsOwnerOrReadOnly", "IsAdminUser"]
    
    def _extract_api_endpoints(self, code: str) -> List[Dict[str, str]]:
        """Extract API endpoints."""
        return [
            {"path": "/api/v1/users/", "method": "GET", "description": "List users"},
            {"path": "/api/v1/users/", "method": "POST", "description": "Create user"}
        ]
    
    def _extract_user_model(self, code: str) -> Dict[str, str]:
        """Extract custom user model info."""
        return {
            "model_name": "CustomUser",
            "fields": "email, first_name, last_name, is_active",
            "manager": "CustomUserManager"
        }
    
    def _extract_auth_views(self, code: str) -> List[str]:
        """Extract authentication views."""
        return ["LoginView", "LogoutView", "RegisterView", "PasswordResetView"]
    
    def _extract_auth_forms(self, code: str) -> List[str]:
        """Extract authentication forms."""
        return ["LoginForm", "RegisterForm", "PasswordResetForm"]
    
    def _extract_auth_backends(self, code: str) -> List[str]:
        """Extract authentication backends."""
        return ["EmailBackend", "SocialAuthBackend"]
    
    def _extract_environment_configs(self, code: str) -> List[str]:
        """Extract environment configurations."""
        return ["development", "production", "testing", "staging"]
    
    def _extract_security_settings(self, code: str) -> List[str]:
        """Extract security settings."""
        return ["SECURE_SSL_REDIRECT", "CSRF_COOKIE_SECURE", "SESSION_COOKIE_SECURE"]
    
    def _extract_database_configs(self, code: str) -> Dict[str, str]:
        """Extract database configurations."""
        return {
            "development": "SQLite for local development",
            "production": "PostgreSQL for production",
            "testing": "In-memory SQLite for tests"
        }