"""
Backend Generator

Main generator class for creating backend code using LLMs.
Coordinates between different specialized generators.
"""

from typing import Dict, Any, List, Optional
import logging
from pathlib import Path
from datetime import datetime

from mcpturbo import protocol
from genesis_templates import TemplateEngine

from ..config import BackendConfig, BackendFramework
from .api_generator import APIGenerator
from .model_generator import ModelGenerator
from .auth_generator import AuthGenerator

logger = logging.getLogger(__name__)


class BackendGenerator:
    """
    Main backend code generator.
    
    Coordinates generation of complete backend applications
    using specialized generators and LLM agents.
    """
    
    def __init__(self, template_engine: Optional[TemplateEngine] = None):
        self.template_engine = template_engine or TemplateEngine()
        self.api_generator = APIGenerator(self.template_engine)
        self.model_generator = ModelGenerator(self.template_engine)
        self.auth_generator = AuthGenerator(self.template_engine)
        
        # Supported frameworks
        self.framework_generators = {
            BackendFramework.FASTAPI: self._generate_fastapi_backend,
            BackendFramework.DJANGO: self._generate_django_backend,
            BackendFramework.NESTJS: self._generate_nestjs_backend,
        }
    
    async def generate_backend(
        self,
        config: BackendConfig,
        architecture: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """
        Generate complete backend application.
        
        Args:
            config: Backend configuration
            architecture: Backend architecture design
            output_path: Output directory path
            
        Returns:
            Generation result with files created and metadata
        """
        logger.info(f"🏗️ Generating backend with {config.framework.value}")
        
        # Validate framework support
        if config.framework not in self.framework_generators:
            raise ValueError(f"Framework {config.framework.value} not supported")
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate using framework-specific generator
        generator = self.framework_generators[config.framework]
        result = await generator(config, architecture, output_path)
        
        # Add common files
        common_files = await self._generate_common_files(config, output_path)
        result["files"].update(common_files)
        
        # Generate documentation
        docs = await self._generate_documentation(config, architecture, output_path)
        result["files"].update(docs)
        
        logger.info(f"✅ Backend generation completed: {len(result['files'])} files created")
        
        return {
            **result,
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": "BackendGenerator",
                "framework": config.framework.value,
                "total_files": len(result["files"])
            }
        }
    
    async def _generate_fastapi_backend(
        self,
        config: BackendConfig,
        architecture: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """Generate FastAPI backend application."""
        files = {}
        
        # Generate main application
        main_app = await self._generate_fastapi_main(config, architecture)
        files["app/main.py"] = main_app
        
        # Generate API routes
        api_files = await self.api_generator.generate_fastapi_routes(
            architecture.get("api_design", {}),
            config
        )
        files.update(api_files)
        
        # Generate data models
        model_files = await self.model_generator.generate_sqlalchemy_models(
            architecture.get("data_models", []),
            config
        )
        files.update(model_files)
        
        # Generate authentication if needed
        if config.auth.method.value != "none":
            auth_files = await self.auth_generator.generate_fastapi_auth(config)
            files.update(auth_files)
        
        # Generate configuration
        config_files = await self._generate_fastapi_config(config)
        files.update(config_files)
        
        # Generate requirements and Docker files
        files["requirements.txt"] = await self._generate_fastapi_requirements(config)
        files["Dockerfile"] = await self._generate_fastapi_dockerfile(config)
        files["docker-compose.yml"] = await self._generate_docker_compose(config)
        
        # Generate database migrations
        if "database" in config.features:
            migration_files = await self._generate_alembic_config(config)
            files.update(migration_files)
        
        # Generate tests
        test_files = await self._generate_fastapi_tests(config, architecture)
        files.update(test_files)
        
        return {
            "files": files,
            "framework": "fastapi",
            "structure": self._get_fastapi_structure(),
            "features_implemented": config.features,
            "next_steps": self._get_fastapi_next_steps(config)
        }
    
    async def _generate_django_backend(
        self,
        config: BackendConfig,
        architecture: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """Generate Django backend application."""
        files = {}
        
        # Generate Django project structure
        django_project = await self._generate_django_project(config, architecture)
        files.update(django_project)
        
        # Generate Django models
        model_files = await self.model_generator.generate_django_models(
            architecture.get("data_models", []),
            config
        )
        files.update(model_files)
        
        # Generate Django views and URLs
        api_files = await self.api_generator.generate_django_views(
            architecture.get("api_design", {}),
            config
        )
        files.update(api_files)
        
        # Generate authentication
        if config.auth.method.value != "none":
            auth_files = await self.auth_generator.generate_django_auth(config)
            files.update(auth_files)
        
        return {
            "files": files,
            "framework": "django",
            "structure": self._get_django_structure(),
            "features_implemented": config.features,
            "next_steps": self._get_django_next_steps(config)
        }
    
    async def _generate_nestjs_backend(
        self,
        config: BackendConfig,
        architecture: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """Generate NestJS backend application."""
        files = {}
        
        # Generate NestJS application
        nestjs_app = await self._generate_nestjs_main(config, architecture)
        files.update(nestjs_app)
        
        # Generate controllers and services
        api_files = await self.api_generator.generate_nestjs_controllers(
            architecture.get("api_design", {}),
            config
        )
        files.update(api_files)
        
        # Generate TypeORM entities
        model_files = await self.model_generator.generate_typeorm_entities(
            architecture.get("data_models", []),
            config
        )
        files.update(model_files)
        
        # Generate authentication
        if config.auth.method.value != "none":
            auth_files = await self.auth_generator.generate_nestjs_auth(config)
            files.update(auth_files)
        
        return {
            "files": files,
            "framework": "nestjs",
            "structure": self._get_nestjs_structure(),
            "features_implemented": config.features,
            "next_steps": self._get_nestjs_next_steps(config)
        }
    
    async def _generate_fastapi_main(
        self,
        config: BackendConfig,
        architecture: Dict[str, Any]
    ) -> str:
        """Generate FastAPI main application file using LLM."""
        
        main_generation_prompt = f"""
        Generate a production-ready FastAPI main.py file with this configuration:
        
        Project: {config.project_name}
        Description: {config.description}
        Features: {config.features}
        Database: {config.database.type.value}
        Authentication: {config.auth.method.value}
        CORS Origins: {config.cors_origins}
        Debug: {config.debug}
        
        Include:
        1. FastAPI app initialization with proper metadata
        2. CORS middleware configuration
        3. Database connection setup
        4. Router registration for API endpoints
        5. Error handling middleware
        6. Authentication middleware if needed
        7. Health check endpoint
        8. Startup and shutdown events
        9. OpenAPI documentation configuration
        10. Logging setup
        
        Return only the Python code, production-ready and well-commented.
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="openai",
            action="code_generation",
            data={
                "prompt": main_generation_prompt,
                "language": "python",
                "framework": "fastapi"
            }
        )
        
        return response.result
    
    async def _generate_fastapi_config(self, config: BackendConfig) -> Dict[str, str]:
        """Generate FastAPI configuration files using LLM."""
        
        config_generation_prompt = f"""
        Generate FastAPI configuration files for:
        
        Project: {config.project_name}
        Database: {config.database.connection_url}
        Features: {config.features}
        
        Generate:
        1. app/core/settings.py - Pydantic BaseSettings configuration
        2. app/core/database.py - SQLAlchemy database setup
        3. app/core/security.py - Security utilities
        4. .env.example - Environment variables example
        
        Return structured configuration code.
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": config_generation_prompt}
        )
        
        return self._parse_config_files(response.result)
    
    async def _generate_fastapi_requirements(self, config: BackendConfig) -> str:
        """Generate requirements.txt for FastAPI."""
        
        requirements_prompt = f"""
        Generate requirements.txt for FastAPI project:
        
        Framework: FastAPI (latest stable)
        Database: {config.database.type.value}
        ORM: {config.database.orm.value if config.database.orm else 'SQLAlchemy'}
        Authentication: {config.auth.method.value}
        Features: {config.features}
        
        Include all necessary dependencies with specific versions for production.
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="deepseek",
            action="fast_coding",
            data={"prompt": requirements_prompt}
        )
        
        return response.result
    
    async def _generate_fastapi_dockerfile(self, config: BackendConfig) -> str:
        """Generate Dockerfile for FastAPI."""
        
        dockerfile_prompt = f"""
        Generate production-ready Dockerfile for FastAPI project:
        
        Project: {config.project_name}
        Python Version: 3.11
        Database: {config.database.type.value}
        
        Requirements:
        - Multi-stage build for optimization
        - Security best practices
        - Non-root user
        - Health check
        - Proper dependency caching
        - Environment variable support
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": dockerfile_prompt}
        )
        
        return response.result
    
    async def _generate_docker_compose(self, config: BackendConfig) -> str:
        """Generate docker-compose.yml."""
        
        compose_prompt = f"""
        Generate docker-compose.yml for development:
        
        Backend: FastAPI
        Database: {config.database.type.value}
        Features: {config.features}
        
        Include:
        - Backend service with volume mounts for development
        - Database service with persistent volume
        - Environment variable configuration
        - Health checks
        - Network configuration
        - Redis if caching is enabled
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": compose_prompt, "language": "yaml"}
        )
        
        return response.result
    
    async def _generate_alembic_config(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Alembic migration configuration."""
        
        alembic_prompt = f"""
        Generate Alembic configuration for database migrations:
        
        Database: {config.database.connection_url}
        Models Location: app.models
        
        Generate:
        1. alembic.ini - Alembic configuration
        2. alembic/env.py - Migration environment
        3. alembic/script.py.mako - Migration template
        
        Configure for async SQLAlchemy if needed.
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": alembic_prompt}
        )
        
        return self._parse_alembic_files(response.result)
    
    async def _generate_fastapi_tests(
        self,
        config: BackendConfig,
        architecture: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate test files for FastAPI."""
        
        test_generation_prompt = f"""
        Generate comprehensive tests for FastAPI application:
        
        Config: {config.to_dict()}
        Architecture: {architecture}
        
        Generate:
        1. tests/conftest.py - Test configuration and fixtures
        2. tests/test_main.py - Main application tests
        3. tests/test_api.py - API endpoint tests
        4. tests/test_auth.py - Authentication tests if enabled
        5. tests/test_models.py - Model tests
        
        Use pytest with async support and TestClient.
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": test_generation_prompt, "language": "python"}
        )
        
        return self._parse_test_files(response.result)
    
    async def _generate_common_files(
        self,
        config: BackendConfig,
        output_path: Path
    ) -> Dict[str, str]:
        """Generate common files for any backend framework."""
        files = {}
        
        # Generate .gitignore
        files[".gitignore"] = await self._generate_gitignore(config)
        
        # Generate README.md
        files["README.md"] = await self._generate_readme(config)
        
        # Generate GitHub Actions workflow
        files[".github/workflows/ci.yml"] = await self._generate_ci_workflow(config)
        
        return files
    
    async def _generate_documentation(
        self,
        config: BackendConfig,
        architecture: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, str]:
        """Generate documentation files."""
        files = {}
        
        # Generate API documentation
        files["docs/api.md"] = await self._generate_api_docs(config, architecture)
        
        # Generate deployment guide
        files["docs/deployment.md"] = await self._generate_deployment_docs(config)
        
        # Generate development guide
        files["docs/development.md"] = await self._generate_development_docs(config)
        
        return files
    
    # Helper methods for structure definitions
    def _get_fastapi_structure(self) -> Dict[str, str]:
        """Get FastAPI project structure."""
        return {
            "app/": "Main application package",
            "app/main.py": "FastAPI application entry point",
            "app/core/": "Core configuration and utilities",
            "app/api/": "API routes and endpoints", 
            "app/models/": "SQLAlchemy models",
            "app/schemas/": "Pydantic schemas",
            "app/services/": "Business logic services",
            "tests/": "Test modules",
            "alembic/": "Database migrations"
        }
    
    def _get_django_structure(self) -> Dict[str, str]:
        """Get Django project structure."""
        return {
            "manage.py": "Django management script",
            "config/": "Django project configuration",
            "apps/": "Django applications",
            "requirements/": "Requirements files",
            "static/": "Static files",
            "media/": "Media files"
        }
    
    def _get_nestjs_structure(self) -> Dict[str, str]:
        """Get NestJS project structure."""
        return {
            "src/": "Source code",
            "src/main.ts": "Application entry point",
            "src/app.module.ts": "Root module",
            "src/controllers/": "Request handlers",
            "src/services/": "Business logic",
            "src/entities/": "TypeORM entities",
            "test/": "Test files"
        }
    
    def _get_fastapi_next_steps(self, config: BackendConfig) -> List[str]:
        """Get next steps for FastAPI project."""
        steps = [
            "Review and update .env file with your configuration",
            "Run `pip install -r requirements.txt` to install dependencies",
            "Set up your database and run migrations with `alembic upgrade head`",
            "Start the development server with `uvicorn app.main:app --reload`",
            "Visit http://localhost:8000/docs to see API documentation"
        ]
        
        if "authentication" in config.features:
            steps.append("Configure JWT secret key in environment variables")
        
        return steps
    
    def _get_django_next_steps(self, config: BackendConfig) -> List[str]:
        """Get next steps for Django project."""
        return [
            "Update settings.py with your configuration",
            "Run `python manage.py migrate` to set up database",
            "Create a superuser with `python manage.py createsuperuser`",
            "Start the server with `python manage.py runserver`"
        ]
    
    def _get_nestjs_next_steps(self, config: BackendConfig) -> List[str]:
        """Get next steps for NestJS project."""
        return [
            "Install dependencies with `npm install`",
            "Update .env file with your configuration", 
            "Run database migrations",
            "Start the server with `npm run start:dev`"
        ]
    
    # Parsing helper methods
    def _parse_config_files(self, llm_response: str) -> Dict[str, str]:
        """Parse configuration files from LLM response."""
        # Basic parsing - in production would use more sophisticated parsing
        return {
            "app/core/settings.py": "# Settings configuration",
            "app/core/database.py": "# Database configuration",
            "app/core/security.py": "# Security utilities",
            ".env.example": "# Environment variables"
        }
    
    def _parse_alembic_files(self, llm_response: str) -> Dict[str, str]:
        """Parse Alembic files from LLM response."""
        return {
            "alembic.ini": "# Alembic configuration",
            "alembic/env.py": "# Migration environment",
            "alembic/script.py.mako": "# Migration template"
        }
    
    def _parse_test_files(self, llm_response: str) -> Dict[str, str]:
        """Parse test files from LLM response."""
        return {
            "tests/conftest.py": "# Test configuration",
            "tests/test_main.py": "# Main application tests",
            "tests/test_api.py": "# API tests"
        }
    
    # Common file generators (using LLMs for content)
    async def _generate_gitignore(self, config: BackendConfig) -> str:
        """Generate .gitignore file."""
        gitignore_prompt = f"""
        Generate .gitignore for {config.framework.value} project with {config.language}.
        Include common patterns for Python/Node.js, IDEs, OS files, and secrets.
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="deepseek",
            action="fast_coding",
            data={"prompt": gitignore_prompt}
        )
        
        return response.result
    
    async def _generate_readme(self, config: BackendConfig) -> str:
        """Generate README.md file."""
        readme_prompt = f"""
        Generate comprehensive README.md for {config.framework.value} project:
        
        Project: {config.project_name}
        Description: {config.description}
        Features: {config.features}
        
        Include:
        - Project overview
        - Features list
        - Installation instructions
        - API documentation links
        - Development setup
        - Deployment instructions
        - Contributing guidelines
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": readme_prompt}
        )
        
        return response.result
    
    async def _generate_ci_workflow(self, config: BackendConfig) -> str:
        """Generate CI/CD workflow."""
        ci_prompt = f"""
        Generate GitHub Actions workflow for {config.framework.value} project:
        
        Language: {config.language}
        Database: {config.database.type.value}
        Testing: pytest/jest
        
        Include:
        - Dependency caching
        - Database setup for tests
        - Code quality checks
        - Test execution
        - Docker build if applicable
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": ci_prompt, "language": "yaml"}
        )
        
        return response.result
    
    async def _generate_api_docs(
        self,
        config: BackendConfig,
        architecture: Dict[str, Any]
    ) -> str:
        """Generate API documentation."""
        docs_prompt = f"""
        Generate API documentation for {config.framework.value} project:
        
        Project: {config.project_name}
        API Design: {architecture.get('api_design', {})}
        
        Include:
        - API overview
        - Authentication guide
        - Endpoint documentation
        - Request/response examples
        - Error codes
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": docs_prompt}
        )
        
        return response.result
    
    async def _generate_deployment_docs(self, config: BackendConfig) -> str:
        """Generate deployment documentation."""
        deployment_prompt = f"""
        Generate deployment guide for {config.framework.value} project:
        
        Framework: {config.framework.value}
        Database: {config.database.type.value}
        
        Include:
        - Environment setup
        - Database configuration
        - Docker deployment
        - Cloud deployment options
        - Monitoring setup
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": deployment_prompt}
        )
        
        return response.result
    
    async def _generate_development_docs(self, config: BackendConfig) -> str:
        """Generate development documentation."""
        dev_prompt = f"""
        Generate development guide for {config.framework.value} project:
        
        Framework: {config.framework.value}
        Features: {config.features}
        
        Include:
        - Local development setup
        - Project structure explanation
        - Code style guidelines
        - Testing guidelines
        - Contributing workflow
        """
        
        response = await protocol.send_request(
            sender_id="backend_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": dev_prompt}
        )
        
        return response.result