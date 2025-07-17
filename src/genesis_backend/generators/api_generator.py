"""
API Generator

Specialized generator for creating API endpoints and routes using LLMs.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from mcpturbo import protocol
from genesis_templates import TemplateEngine

from ..config import BackendConfig, BackendFramework

logger = logging.getLogger(__name__)


class APIGenerator:
    """
    Generator specialized in API endpoint creation.
    
    Responsibilities:
    - Generate REST API endpoints
    - Create API route handlers
    - Generate request/response schemas
    - Create API documentation
    - Generate OpenAPI specifications
    """
    
    def __init__(self, template_engine: Optional[TemplateEngine] = None):
        self.template_engine = template_engine or TemplateEngine()
        
        # Framework-specific API generators
        self.framework_generators = {
            BackendFramework.FASTAPI: self._generate_fastapi_api,
            BackendFramework.DJANGO: self._generate_django_api,
            BackendFramework.NESTJS: self._generate_nestjs_api,
        }
    
    async def generate_api_endpoints(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """
        Generate API endpoints for specified framework.
        
        Args:
            api_design: API design specification
            config: Backend configuration
            
        Returns:
            Dictionary of generated API files
        """
        logger.info(f"🔌 Generating API endpoints for {config.framework.value}")
        
        if config.framework not in self.framework_generators:
            raise ValueError(f"Framework {config.framework.value} not supported for API generation")
        
        generator = self.framework_generators[config.framework]
        return await generator(api_design, config)
    
    async def generate_fastapi_routes(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate FastAPI routes and endpoints."""
        return await self._generate_fastapi_api(api_design, config)
    
    async def generate_django_views(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate Django views and URL patterns."""
        return await self._generate_django_api(api_design, config)
    
    async def generate_nestjs_controllers(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate NestJS controllers and modules."""
        return await self._generate_nestjs_api(api_design, config)
    
    async def _generate_fastapi_api(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate FastAPI API implementation using LLM."""
        
        fastapi_generation_prompt = f"""
        Generate FastAPI API implementation:
        
        API Design: {api_design}
        Project Config: {config.to_dict()}
        
        Generate comprehensive FastAPI API including:
        1. Router setup with proper prefixes and tags
        2. Route handlers for all endpoints
        3. Path and query parameter validation
        4. Request body validation with Pydantic
        5. Response models and status codes
        6. Authentication dependencies where needed
        7. Error handling with HTTPException
        8. OpenAPI documentation decorators
        9. CORS configuration if specified
        10. Rate limiting and security headers
        
        For each endpoint provide:
        - Proper HTTP method and path
        - Input validation and typing
        - Business logic placeholder
        - Error handling
        - Response formatting
        - API documentation
        
        Generate separate router files for different resource groups.
        Return well-structured FastAPI code with proper typing.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="openai",  # OpenAI good at FastAPI code
            action="code_generation",
            data={
                "prompt": fastapi_generation_prompt,
                "language": "python",
                "framework": "fastapi"
            }
        )
        
        # Parse and organize the generated code
        api_files = self._parse_fastapi_api_files(response.result)
        
        # Generate additional API support files
        api_files.update(await self._generate_fastapi_dependencies(config))
        api_files.update(await self._generate_fastapi_schemas(api_design))
        api_files.update(await self._generate_openapi_spec(api_design, config))
        
        return api_files
    
    async def _generate_django_api(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate Django API implementation using LLM."""
        
        django_generation_prompt = f"""
        Generate Django REST Framework API implementation:
        
        API Design: {api_design}
        Project Config: {config.to_dict()}
        
        Generate comprehensive Django API including:
        1. Django REST Framework viewsets
        2. Serializers for request/response validation
        3. URL patterns with proper routing
        4. Permission classes for authentication
        5. Filter backends for searching/filtering
        6. Pagination configuration
        7. Custom API views for business logic
        8. Exception handling
        9. API documentation with drf-spectacular
        10. Throttling and rate limiting
        
        For each model/resource provide:
        - ModelSerializer with validation
        - ModelViewSet with CRUD operations
        - Custom actions if needed
        - Permission handling
        - URL routing configuration
        
        Generate separate files for serializers, views, and URLs.
        Return production-ready Django REST code.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="claude",  # Claude good at Django patterns
            action="reasoning",
            data={
                "prompt": django_generation_prompt,
                "system_prompt": "You are a Django REST Framework expert. Generate scalable API code."
            }
        )
        
        # Parse and organize the generated code
        api_files = self._parse_django_api_files(response.result)
        
        # Generate additional Django API files
        api_files.update(await self._generate_django_serializers(api_design))
        api_files.update(await self._generate_django_permissions(config))
        api_files.update(await self._generate_django_filters(api_design))
        
        return api_files
    
    async def _generate_nestjs_api(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate NestJS API implementation using LLM."""
        
        nestjs_generation_prompt = f"""
        Generate NestJS API implementation:
        
        API Design: {api_design}
        Project Config: {config.to_dict()}
        
        Generate comprehensive NestJS API including:
        1. Controllers with proper decorators
        2. Services for business logic
        3. DTOs for request/response validation
        4. Guards for authentication/authorization
        5. Pipes for data transformation
        6. Interceptors for logging/transformation
        7. Exception filters for error handling
        8. Swagger decorators for documentation
        9. Module organization
        10. Dependency injection setup
        
        For each resource provide:
        - Controller with HTTP method decorators
        - Service with business logic
        - DTOs with validation decorators
        - Guards for route protection
        - Proper TypeScript typing
        
        Generate separate files for controllers, services, DTOs, and modules.
        Return production-ready NestJS code with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="deepseek",  # DeepSeek good at TypeScript
            action="fast_coding",
            data={
                "prompt": nestjs_generation_prompt,
                "language": "typescript"
            }
        )
        
        # Parse and organize the generated code
        api_files = self._parse_nestjs_api_files(response.result)
        
        # Generate additional NestJS API files
        api_files.update(await self._generate_nestjs_dtos(api_design))
        api_files.update(await self._generate_nestjs_guards(config))
        api_files.update(await self._generate_nestjs_interceptors(config))
        
        return api_files
    
    async def _generate_fastapi_dependencies(self, config: BackendConfig) -> Dict[str, str]:
        """Generate FastAPI dependency functions."""
        
        dependencies_prompt = f"""
        Generate FastAPI dependency functions for:
        
        Config: {config.to_dict()}
        
        Generate dependencies for:
        1. Database session management
        2. Current user authentication
        3. Permission checking
        4. Rate limiting
        5. Request validation
        6. Logging context
        7. Configuration injection
        8. Background tasks
        
        Return reusable dependency functions with proper typing.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": dependencies_prompt, "language": "python"}
        )
        
        return {"app/api/deps.py": response.result}
    
    async def _generate_fastapi_schemas(self, api_design: Dict[str, Any]) -> Dict[str, str]:
        """Generate FastAPI Pydantic schemas."""
        
        schemas_prompt = f"""
        Generate Pydantic schemas for FastAPI:
        
        API Design: {api_design}
        
        Generate schemas for:
        1. Request bodies (Create, Update)
        2. Response models (Read, List)
        3. Query parameters
        4. Error responses
        5. Nested objects
        6. Validation rules
        
        Include proper validation and documentation.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": schemas_prompt, "language": "python"}
        )
        
        return {"app/schemas/api.py": response.result}
    
    async def _generate_openapi_spec(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate OpenAPI specification."""
        
        openapi_prompt = f"""
        Generate OpenAPI 3.0 specification:
        
        API Design: {api_design}
        Project: {config.project_name}
        
        Generate complete OpenAPI spec with:
        1. API information and metadata
        2. Server configuration
        3. Path definitions with operations
        4. Schema definitions
        5. Security schemes
        6. Response definitions
        7. Parameter definitions
        8. Example values
        
        Return valid OpenAPI JSON specification.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": openapi_prompt}
        )
        
        return {"docs/openapi.json": response.result}
    
    async def _generate_django_serializers(self, api_design: Dict[str, Any]) -> Dict[str, str]:
        """Generate Django REST Framework serializers."""
        
        serializers_prompt = f"""
        Generate Django REST Framework serializers:
        
        API Design: {api_design}
        
        Generate serializers for:
        1. Model serializers for CRUD operations
        2. Custom validation methods
        3. Nested serializers for relationships
        4. Read-only and write-only fields
        5. Method fields for computed values
        6. Custom to_representation methods
        
        Return comprehensive DRF serializers.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": serializers_prompt, "language": "python"}
        )
        
        return {"api/serializers.py": response.result}
    
    async def _generate_django_permissions(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django REST Framework permissions."""
        
        permissions_prompt = f"""
        Generate Django REST Framework permissions:
        
        Config: {config.to_dict()}
        
        Generate permission classes for:
        1. Object-level permissions
        2. Model-level permissions
        3. Custom business logic permissions
        4. Role-based permissions
        5. Owner-only permissions
        
        Return reusable permission classes.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": permissions_prompt}
        )
        
        return {"api/permissions.py": response.result}
    
    async def _generate_django_filters(self, api_design: Dict[str, Any]) -> Dict[str, str]:
        """Generate Django REST Framework filters."""
        
        filters_prompt = f"""
        Generate Django REST Framework filters:
        
        API Design: {api_design}
        
        Generate filter classes for:
        1. Search filters
        2. Ordering filters
        3. Field-based filters
        4. Date range filters
        5. Custom filter logic
        
        Return comprehensive filter backends.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="deepseek",
            action="fast_coding",
            data={"prompt": filters_prompt, "language": "python"}
        )
        
        return {"api/filters.py": response.result}
    
    async def _generate_nestjs_dtos(self, api_design: Dict[str, Any]) -> Dict[str, str]:
        """Generate NestJS DTOs."""
        
        dtos_prompt = f"""
        Generate NestJS DTOs with validation:
        
        API Design: {api_design}
        
        Generate DTOs for:
        1. Create operations
        2. Update operations
        3. Query parameters
        4. Response formatting
        5. Validation rules
        6. Transformation logic
        
        Return comprehensive NestJS DTOs with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": dtos_prompt, "language": "typescript"}
        )
        
        return {"src/dto/api.dto.ts": response.result}
    
    async def _generate_nestjs_guards(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS guards."""
        
        guards_prompt = f"""
        Generate NestJS guards for security:
        
        Config: {config.to_dict()}
        
        Generate guards for:
        1. JWT authentication
        2. Role-based authorization
        3. Resource ownership
        4. Rate limiting
        5. API key validation
        
        Return comprehensive NestJS guards with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": guards_prompt}
        )
        
        return {"src/guards/api.guards.ts": response.result}
    
    async def _generate_nestjs_interceptors(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS interceptors."""
        
        interceptors_prompt = f"""
        Generate NestJS interceptors:
        
        Config: {config.to_dict()}
        
        Generate interceptors for:
        1. Response transformation
        2. Request logging
        3. Error handling
        4. Performance monitoring
        5. Cache management
        
        Return comprehensive NestJS interceptors with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="deepseek",
            action="fast_coding",
            data={"prompt": interceptors_prompt, "language": "typescript"}
        )
        
        return {"src/interceptors/api.interceptors.ts": response.result}
    
    # Utility methods for parsing LLM responses
    def _parse_fastapi_api_files(self, llm_response: str) -> Dict[str, str]:
        """Parse FastAPI API files from LLM response."""
        # Basic parsing - in production would use more sophisticated parsing
        return {
            "app/api/v1/endpoints/users.py": "# FastAPI user routes",
            "app/api/v1/endpoints/auth.py": "# FastAPI auth routes",
            "app/api/v1/api.py": "# API router configuration"
        }
    
    def _parse_django_api_files(self, llm_response: str) -> Dict[str, str]:
        """Parse Django API files from LLM response."""
        return {
            "api/views.py": "# Django REST Framework views",
            "api/urls.py": "# Django URL patterns",
            "api/viewsets.py": "# Django REST Framework viewsets"
        }
    
    def _parse_nestjs_api_files(self, llm_response: str) -> Dict[str, str]:
        """Parse NestJS API files from LLM response."""
        return {
            "src/controllers/users.controller.ts": "# NestJS user controller",
            "src/controllers/auth.controller.ts": "# NestJS auth controller",
            "src/services/users.service.ts": "# NestJS user service"
        }
    
    # Additional utility methods for specific API features
    async def generate_api_tests(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate API tests for the specified framework."""
        
        test_generation_prompt = f"""
        Generate API tests for {config.framework.value}:
        
        API Design: {api_design}
        Framework: {config.framework.value}
        
        Generate comprehensive API tests including:
        1. Unit tests for each endpoint
        2. Integration tests for workflows
        3. Authentication tests
        4. Error handling tests
        5. Performance tests
        6. Security tests
        
        Return complete test suite with proper assertions.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="openai",
            action="code_generation",
            data={
                "prompt": test_generation_prompt,
                "language": config.language,
                "framework": f"{config.framework.value}_tests"
            }
        )
        
        return self._parse_api_test_files(response.result, config.framework)
    
    async def generate_api_documentation(
        self,
        api_design: Dict[str, Any],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate comprehensive API documentation."""
        
        docs_generation_prompt = f"""
        Generate API documentation for {config.project_name}:
        
        API Design: {api_design}
        Framework: {config.framework.value}
        
        Generate documentation including:
        1. API overview and introduction
        2. Authentication guide
        3. Endpoint documentation with examples
        4. Error codes and responses
        5. SDK and client library guides
        6. Rate limiting information
        7. Changelog and versioning
        
        Return comprehensive API documentation in Markdown.
        """
        
        response = await protocol.send_request(
            sender_id="api_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": docs_generation_prompt}
        )
        
        return {
            "docs/api/README.md": response.result,
            "docs/api/authentication.md": "# Authentication guide",
            "docs/api/endpoints.md": "# Endpoints documentation",
            "docs/api/errors.md": "# Error handling guide"
        }
    
    def _parse_api_test_files(self, llm_response: str, framework: BackendFramework) -> Dict[str, str]:
        """Parse API test files from LLM response."""
        if framework == BackendFramework.FASTAPI:
            return {
                "tests/test_api_users.py": "# FastAPI user endpoint tests",
                "tests/test_api_auth.py": "# FastAPI auth endpoint tests"
            }
        elif framework == BackendFramework.DJANGO:
            return {
                "tests/test_api_views.py": "# Django API view tests",
                "tests/test_api_serializers.py": "# Django serializer tests"
            }
        elif framework == BackendFramework.NESTJS:
            return {
                "test/api/users.controller.spec.ts": "# NestJS user controller tests",
                "test/api/auth.controller.spec.ts": "# NestJS auth controller tests"
            }
        else:
            return {"tests/test_api.py": "# Generic API tests"}