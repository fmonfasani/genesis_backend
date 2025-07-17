"""
Model Generator

Specialized generator for creating data models and ORM entities using LLMs.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from mcpturbo import protocol
from genesis_templates import TemplateEngine

from ..config import BackendConfig, BackendFramework, DatabaseType, ORMType

logger = logging.getLogger(__name__)


class ModelGenerator:
    """
    Generator specialized in data model creation.
    
    Responsibilities:
    - Generate ORM models for different frameworks
    - Create database schemas and relationships
    - Generate migration scripts
    - Create data validation rules
    - Generate model serializers and DTOs
    """
    
    def __init__(self, template_engine: Optional[TemplateEngine] = None):
        self.template_engine = template_engine or TemplateEngine()
        
        # ORM-specific model generators
        self.orm_generators = {
            ORMType.SQLALCHEMY: self._generate_sqlalchemy_models,
            ORMType.DJANGO_ORM: self._generate_django_models,
            ORMType.TYPEORM: self._generate_typeorm_models,
            ORMType.PRISMA: self._generate_prisma_models,
            ORMType.MONGOOSE: self._generate_mongoose_models,
        }
    
    async def generate_models(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """
        Generate data models for specified ORM.
        
        Args:
            data_models: List of data model specifications
            config: Backend configuration
            
        Returns:
            Dictionary of generated model files
        """
        logger.info(f"🗄️ Generating models for {config.database.orm.value if config.database.orm else 'default'}")
        
        orm_type = config.database.orm or self._get_default_orm(config.framework)
        
        if orm_type not in self.orm_generators:
            raise ValueError(f"ORM {orm_type.value} not supported for model generation")
        
        generator = self.orm_generators[orm_type]
        return await generator(data_models, config)
    
    async def generate_sqlalchemy_models(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate SQLAlchemy models."""
        return await self._generate_sqlalchemy_models(data_models, config)
    
    async def generate_django_models(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate Django ORM models."""
        return await self._generate_django_models(data_models, config)
    
    async def generate_typeorm_entities(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate TypeORM entities."""
        return await self._generate_typeorm_models(data_models, config)
    
    async def _generate_sqlalchemy_models(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate SQLAlchemy models using LLM."""
        
        sqlalchemy_generation_prompt = f"""
        Generate SQLAlchemy models for {config.database.type.value}:
        
        Data Models: {data_models}
        Database: {config.database.type.value}
        Project: {config.project_name}
        
        Generate comprehensive SQLAlchemy models including:
        1. Model classes with proper inheritance from Base
        2. Table definitions with appropriate names
        3. Column definitions with proper types and constraints
        4. Primary keys and foreign keys
        5. Relationships (relationship(), back_populates)
        6. Indexes for performance optimization
        7. Unique constraints and check constraints
        8. Model methods and properties
        9. String representations (__str__, __repr__)
        10. Audit fields (created_at, updated_at, deleted_at)
        
        SQLAlchemy 2.0 features to use:
        - Use modern column syntax with Mapped annotations
        - Proper relationship configurations
        - Database-specific column types
        - Performance-optimized queries
        - Async session support if needed
        
        For each model provide:
        - Clear table and column naming
        - Proper type hints and annotations
        - Relationship definitions with proper foreign keys
        - Validation logic where appropriate
        - Performance considerations (indexes, lazy loading)
        
        Return production-ready SQLAlchemy models with proper imports.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="claude",  # Claude excellent at data modeling
            action="reasoning",
            data={
                "prompt": sqlalchemy_generation_prompt,
                "system_prompt": "You are a SQLAlchemy expert. Generate efficient, well-designed models."
            }
        )
        
        # Parse and organize the generated models
        model_files = self._parse_sqlalchemy_models(response.result)
        
        # Generate additional SQLAlchemy files
        model_files.update(await self._generate_sqlalchemy_base(config))
        model_files.update(await self._generate_sqlalchemy_mixins())
        model_files.update(await self._generate_alembic_migrations(data_models, config))
        
        return model_files
    
    async def _generate_django_models(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate Django ORM models using LLM."""
        
        django_generation_prompt = f"""
        Generate Django ORM models:
        
        Data Models: {data_models}
        Database: {config.database.type.value}
        Project: {config.project_name}
        
        Generate comprehensive Django models including:
        1. Model classes inheriting from models.Model
        2. Field definitions with appropriate types
        3. Relationship fields (ForeignKey, OneToOneField, ManyToManyField)
        4. Model Meta class configuration
        5. Custom model methods and properties
        6. String representations (__str__ methods)
        7. Model managers for custom querysets
        8. Validation methods (clean, clean_fields)
        9. Model signals for business logic
        10. Abstract base models where applicable
        
        Django model best practices:
        - Use appropriate field types for data
        - Add help_text for field documentation
        - Use choices for enumerated fields
        - Add proper indexes for performance
        - Include audit fields with auto_now
        - Use related_name for reverse relationships
        - Implement custom querysets for complex queries
        
        For each model provide:
        - Clear field definitions with constraints
        - Proper relationship configurations
        - Custom methods for business logic
        - Admin-friendly string representations
        - Performance optimizations
        
        Return production-ready Django models with proper imports.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="openai",  # OpenAI good at Django patterns
            action="code_generation",
            data={
                "prompt": django_generation_prompt,
                "language": "python",
                "framework": "django"
            }
        )
        
        # Parse and organize the generated models
        model_files = self._parse_django_models(response.result)
        
        # Generate additional Django files
        model_files.update(await self._generate_django_managers())
        model_files.update(await self._generate_django_migrations(data_models))
        model_files.update(await self._generate_django_admin(data_models))
        
        return model_files
    
    async def _generate_typeorm_models(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate TypeORM entities using LLM."""
        
        typeorm_generation_prompt = f"""
        Generate TypeORM entities for {config.database.type.value}:
        
        Data Models: {data_models}
        Database: {config.database.type.value}
        Project: {config.project_name}
        
        Generate comprehensive TypeORM entities including:
        1. Entity decorators with table configuration
        2. Column decorators with proper TypeScript types
        3. Primary key and generated value columns
        4. Foreign key relationships with proper decorators
        5. One-to-One, One-to-Many, Many-to-Many relationships
        6. Entity indexes for performance
        7. Column validation and constraints
        8. Entity listeners and subscribers
        9. Custom repository methods
        10. Migration-friendly entity design
        
        TypeORM features to use:
        - Proper TypeScript typing throughout
        - Database-specific column types
        - Relationship mapping with lazy loading options
        - Entity validation with class-validator
        - Audit columns with automatic timestamps
        - Soft delete support where appropriate
        
        For each entity provide:
        - Clear table and column naming
        - Proper TypeScript interfaces
        - Relationship definitions with cascade options
        - Validation decorators
        - Performance considerations
        
        Return production-ready TypeORM entities with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="deepseek",  # DeepSeek good at TypeScript
            action="fast_coding",
            data={
                "prompt": typeorm_generation_prompt,
                "language": "typescript"
            }
        )
        
        # Parse and organize the generated entities
        model_files = self._parse_typeorm_entities(response.result)
        
        # Generate additional TypeORM files
        model_files.update(await self._generate_typeorm_config(config))
        model_files.update(await self._generate_typeorm_migrations(data_models))
        model_files.update(await self._generate_typeorm_repositories(data_models))
        
        return model_files
    
    async def _generate_prisma_models(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate Prisma schema using LLM."""
        
        prisma_generation_prompt = f"""
        Generate Prisma schema:
        
        Data Models: {data_models}
        Database: {config.database.type.value}
        Project: {config.project_name}
        
        Generate comprehensive Prisma schema including:
        1. Generator and datasource configuration
        2. Model definitions with proper field types
        3. Relationship definitions with references
        4. Unique constraints and indexes
        5. Enum definitions for choice fields
        6. Custom field attributes
        7. Database-specific features
        8. Schema validation rules
        9. Migration configuration
        10. Client generation setup
        
        Prisma features to use:
        - Modern Prisma schema syntax
        - Proper field type mapping
        - Relationship constraints
        - Index optimization
        - Enum definitions
        - Custom attributes
        
        Return complete Prisma schema file.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="claude",  # Claude good at schema design
            action="reasoning",
            data={
                "prompt": prisma_generation_prompt,
                "system_prompt": "You are a Prisma expert. Generate efficient schema designs."
            }
        )
        
        return {
            "prisma/schema.prisma": response.result,
            "prisma/seed.ts": await self._generate_prisma_seed(data_models)
        }
    
    async def _generate_mongoose_models(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate Mongoose models using LLM."""
        
        mongoose_generation_prompt = f"""
        Generate Mongoose models for MongoDB:
        
        Data Models: {data_models}
        Project: {config.project_name}
        
        Generate comprehensive Mongoose models including:
        1. Schema definitions with proper types
        2. Schema validation rules
        3. Virtual fields and methods
        4. Pre and post middleware hooks
        5. Static methods and query helpers
        6. Index definitions for performance
        7. Plugin integration
        8. Population configuration for references
        9. Custom validation functions
        10. Schema options and configuration
        
        Mongoose features to use:
        - Modern Mongoose schema syntax
        - TypeScript integration
        - Validation and sanitization
        - Middleware for business logic
        - Population for references
        - Index optimization
        
        Return production-ready Mongoose models with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="openai",  # OpenAI good at MongoDB patterns
            action="code_generation",
            data={
                "prompt": mongoose_generation_prompt,
                "language": "typescript",
                "framework": "mongoose"
            }
        )
        
        return self._parse_mongoose_models(response.result)
    
    # Utility methods for additional file generation
    async def _generate_sqlalchemy_base(self, config: BackendConfig) -> Dict[str, str]:
        """Generate SQLAlchemy base configuration."""
        
        base_generation_prompt = f"""
        Generate SQLAlchemy base configuration:
        
        Database: {config.database.type.value}
        Connection URL: {config.database.connection_url}
        
        Generate:
        1. Declarative base class
        2. Database engine configuration
        3. Session factory setup
        4. Connection management
        5. Base model with common fields
        
        Return complete SQLAlchemy base setup.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": base_generation_prompt, "language": "python"}
        )
        
        return {"app/db/base.py": response.result}
    
    async def _generate_sqlalchemy_mixins(self) -> Dict[str, str]:
        """Generate common SQLAlchemy mixins."""
        
        mixins_prompt = """
        Generate SQLAlchemy mixins for common functionality:
        
        Generate mixins for:
        1. Timestamp fields (created_at, updated_at)
        2. Soft delete functionality
        3. UUID primary keys
        4. Audit trail (who created/updated)
        5. Serialization methods
        
        Return reusable SQLAlchemy mixins.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": mixins_prompt}
        )
        
        return {"app/db/mixins.py": response.result}
    
    async def _generate_alembic_migrations(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate Alembic migration files."""
        
        migration_prompt = f"""
        Generate Alembic migration configuration:
        
        Models: {data_models}
        Database: {config.database.type.value}
        
        Generate:
        1. Alembic configuration file
        2. Environment setup for migrations
        3. Initial migration script
        4. Migration script template
        
        Return complete Alembic setup.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": migration_prompt}
        )
        
        return {
            "alembic.ini": "# Alembic configuration",
            "alembic/env.py": response.result,
            "alembic/script.py.mako": "# Migration template"
        }
    
    async def _generate_django_managers(self) -> Dict[str, str]:
        """Generate Django model managers."""
        
        managers_prompt = """
        Generate Django model managers:
        
        Generate managers for:
        1. Active/inactive object filtering
        2. Custom querysets with business logic
        3. Soft delete functionality
        4. Common query patterns
        5. Performance-optimized queries
        
        Return reusable Django managers.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": managers_prompt, "language": "python"}
        )
        
        return {"models/managers.py": response.result}
    
    async def _generate_django_migrations(self, data_models: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate Django migration files."""
        return {
            "migrations/__init__.py": "",
            "migrations/0001_initial.py": "# Initial Django migration"
        }
    
    async def _generate_django_admin(self, data_models: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate Django admin configuration."""
        
        admin_prompt = f"""
        Generate Django admin configuration:
        
        Models: {data_models}
        
        Generate admin classes with:
        1. List display configuration
        2. Search and filter fields
        3. Inline editing for related models
        4. Custom admin actions
        5. Form customization
        
        Return comprehensive Django admin setup.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": admin_prompt}
        )
        
        return {"admin.py": response.result}
    
    async def _generate_typeorm_config(self, config: BackendConfig) -> Dict[str, str]:
        """Generate TypeORM configuration."""
        
        config_prompt = f"""
        Generate TypeORM configuration:
        
        Database: {config.database.type.value}
        Connection: {config.database.connection_url}
        
        Generate TypeORM configuration with:
        1. Data source configuration
        2. Entity registration
        3. Migration settings
        4. Connection options
        5. Logging configuration
        
        Return complete TypeORM setup.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="deepseek",
            action="fast_coding",
            data={"prompt": config_prompt, "language": "typescript"}
        )
        
        return {"src/data-source.ts": response.result}
    
    async def _generate_typeorm_migrations(self, data_models: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate TypeORM migration files."""
        return {
            "src/migrations/1000000000000-Initial.ts": "# Initial TypeORM migration"
        }
    
    async def _generate_typeorm_repositories(self, data_models: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate TypeORM custom repositories."""
        
        repositories_prompt = f"""
        Generate TypeORM custom repositories:
        
        Models: {data_models}
        
        Generate repositories with:
        1. Custom query methods
        2. Business logic encapsulation
        3. Performance-optimized queries
        4. Transaction support
        5. Error handling
        
        Return TypeORM repositories with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": repositories_prompt, "language": "typescript"}
        )
        
        return {"src/repositories/base.repository.ts": response.result}
    
    async def _generate_prisma_seed(self, data_models: List[Dict[str, Any]]) -> str:
        """Generate Prisma seed file."""
        
        seed_prompt = f"""
        Generate Prisma seed file:
        
        Models: {data_models}
        
        Generate seed data with:
        1. Sample data for each model
        2. Proper relationships
        3. Realistic test data
        4. Database reset functionality
        5. Environment-specific data
        
        Return complete Prisma seed script with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": seed_prompt, "language": "typescript"}
        )
        
        return response.result
    
    # Utility methods for parsing LLM responses
    def _parse_sqlalchemy_models(self, llm_response: str) -> Dict[str, str]:
        """Parse SQLAlchemy models from LLM response."""
        # Basic parsing - in production would use more sophisticated parsing
        return {
            "app/models/user.py": "# SQLAlchemy User model",
            "app/models/base.py": "# SQLAlchemy base classes",
            "app/models/__init__.py": "# Models package"
        }
    
    def _parse_django_models(self, llm_response: str) -> Dict[str, str]:
        """Parse Django models from LLM response."""
        return {
            "models.py": llm_response,
            "apps.py": "# Django app configuration"
        }
    
    def _parse_typeorm_entities(self, llm_response: str) -> Dict[str, str]:
        """Parse TypeORM entities from LLM response."""
        return {
            "src/entities/user.entity.ts": "# TypeORM User entity",
            "src/entities/base.entity.ts": "# TypeORM base entity",
            "src/entities/index.ts": "# Entities barrel export"
        }
    
    def _parse_mongoose_models(self, llm_response: str) -> Dict[str, str]:
        """Parse Mongoose models from LLM response."""
        return {
            "src/models/user.model.ts": "# Mongoose User model",
            "src/models/base.model.ts": "# Mongoose base model",
            "src/models/index.ts": "# Models barrel export"
        }
    
    def _get_default_orm(self, framework: BackendFramework) -> ORMType:
        """Get default ORM for framework."""
        defaults = {
            BackendFramework.FASTAPI: ORMType.SQLALCHEMY,
            BackendFramework.DJANGO: ORMType.DJANGO_ORM,
            BackendFramework.NESTJS: ORMType.TYPEORM,
            BackendFramework.EXPRESS: ORMType.MONGOOSE,
        }
        return defaults.get(framework, ORMType.SQLALCHEMY)
    
    # Additional utility methods for model generation
    async def generate_model_tests(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate model tests for the specified ORM."""
        
        test_generation_prompt = f"""
        Generate model tests for {config.database.orm.value if config.database.orm else 'default ORM'}:
        
        Models: {data_models}
        ORM: {config.database.orm.value if config.database.orm else 'SQLAlchemy'}
        
        Generate comprehensive model tests including:
        1. Unit tests for each model
        2. Relationship tests
        3. Validation tests
        4. Custom method tests
        5. Database constraint tests
        6. Performance tests
        
        Return complete test suite for models.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="openai",
            action="code_generation",
            data={
                "prompt": test_generation_prompt,
                "language": config.language
            }
        )
        
        return self._parse_model_test_files(response.result, config)
    
    async def generate_model_factories(
        self,
        data_models: List[Dict[str, Any]],
        config: BackendConfig
    ) -> Dict[str, str]:
        """Generate model factories for testing."""
        
        factory_generation_prompt = f"""
        Generate model factories for testing:
        
        Models: {data_models}
        Framework: {config.framework.value}
        
        Generate factory classes for:
        1. Creating test instances
        2. Relationship handling
        3. Realistic fake data
        4. Bulk data creation
        5. Custom factory methods
        
        Return comprehensive factory classes.
        """
        
        response = await protocol.send_request(
            sender_id="model_generator",
            target_id="deepseek",
            action="fast_coding",
            data={
                "prompt": factory_generation_prompt,
                "language": config.language
            }
        )
        
        return self._parse_factory_files(response.result, config)
    
    def _parse_model_test_files(self, llm_response: str, config: BackendConfig) -> Dict[str, str]:
        """Parse model test files from LLM response."""
        if config.framework == BackendFramework.DJANGO:
            return {"tests/test_models.py": llm_response}
        else:
            return {"tests/test_models.py": llm_response}
    
    def _parse_factory_files(self, llm_response: str, config: BackendConfig) -> Dict[str, str]:
        """Parse factory files from LLM response."""
        if config.framework == BackendFramework.DJANGO:
            return {"tests/factories.py": llm_response}
        else:
            return {"tests/factories.py": llm_response}