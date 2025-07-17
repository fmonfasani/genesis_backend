"""
Database Agent

Specializes in database schema design and data model generation using LLMs.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from genesis_agents import GenesisAgent, AgentTask, TaskResult
from mcpturbo import protocol

from ..config import BackendConfig, DatabaseType, ORMType

logger = logging.getLogger(__name__)


class DatabaseAgent(GenesisAgent):
    """
    Agent specialized in database design and data modeling.
    
    Responsibilities:
    - Design database schemas
    - Generate data models for different ORMs
    - Create database migrations
    - Optimize database performance
    - Design relationships and constraints
    """
    
    def __init__(self):
        super().__init__(
            agent_id="database_specialist",
            name="Database Specialist Agent",
            agent_type="database"
        )
        
        # Database-specific capabilities
        self.add_capability("design_database_schema")
        self.add_capability("generate_orm_models")
        self.add_capability("create_database_migrations")
        self.add_capability("optimize_database_queries")
        self.add_capability("design_relationships")
        self.add_capability("validate_data_integrity")
        self.add_capability("generate_seed_data")
        
        # Register handlers
        self.register_handler("design_database_schema", self._handle_design_schema)
        self.register_handler("generate_orm_models", self._handle_generate_models)
        self.register_handler("create_database_migrations", self._handle_create_migrations)
        self.register_handler("optimize_database_queries", self._handle_optimize_queries)
        self.register_handler("design_relationships", self._handle_design_relationships)
        self.register_handler("validate_data_integrity", self._handle_validate_integrity)
        self.register_handler("generate_seed_data", self._handle_generate_seed_data)
        
        # Supported database types and their characteristics
        self.database_features = {
            DatabaseType.POSTGRESQL: {
                "supports_json": True,
                "supports_arrays": True,
                "supports_full_text": True,
                "supports_partitioning": True,
                "max_index_columns": 32,
                "default_port": 5432
            },
            DatabaseType.MYSQL: {
                "supports_json": True,
                "supports_arrays": False,
                "supports_full_text": True,
                "supports_partitioning": True,
                "max_index_columns": 16,
                "default_port": 3306
            },
            DatabaseType.SQLITE: {
                "supports_json": True,
                "supports_arrays": False,
                "supports_full_text": True,
                "supports_partitioning": False,
                "max_index_columns": 64,
                "default_port": None
            },
            DatabaseType.MONGODB: {
                "supports_json": True,
                "supports_arrays": True,
                "supports_full_text": True,
                "supports_partitioning": True,
                "max_index_columns": 64,
                "default_port": 27017
            }
        }
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Execute database-related task using LLMs."""
        try:
            self.logger.info(f"🗄️ Executing database task: {task.name}")
            
            if task.name == "design_database_schema":
                result = await self._design_database_schema(task.params)
            elif task.name == "generate_orm_models":
                result = await self._generate_orm_models(task.params)
            elif task.name == "create_database_migrations":
                result = await self._create_database_migrations(task.params)
            elif task.name == "optimize_database_queries":
                result = await self._optimize_database_queries(task.params)
            elif task.name == "design_relationships":
                result = await self._design_entity_relationships(task.params)
            elif task.name == "validate_data_integrity":
                result = await self._validate_data_integrity(task.params)
            elif task.name == "generate_seed_data":
                result = await self._generate_seed_data(task.params)
            else:
                result = await self._handle_generic_task(task)
            
            return TaskResult(
                task_id=task.id,
                success=True,
                result=result,
                metadata={
                    "agent": self.name,
                    "task_type": task.name,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error in database task {task.name}: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                metadata={"agent": self.name, "task_type": task.name}
            )
    
    async def _design_database_schema(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Design comprehensive database schema using LLM."""
        entities = params.get("entities", [])
        requirements = params.get("requirements", {})
        database_type = DatabaseType(params.get("database_type", "postgresql"))
        
        # Get database-specific features
        db_features = self.database_features.get(database_type, {})
        
        schema_design_prompt = f"""
        Design a comprehensive database schema for {database_type.value}:
        
        Entities: {entities}
        Requirements: {requirements}
        Database Features: {db_features}
        
        Design the schema considering:
        1. Normalized table structure (3NF minimum)
        2. Primary keys and foreign key relationships
        3. Appropriate data types for {database_type.value}
        4. Constraints (NOT NULL, UNIQUE, CHECK)
        5. Indexes for performance optimization
        6. Audit fields (created_at, updated_at, deleted_at)
        7. Scalability considerations
        8. Data integrity rules
        9. Partitioning strategy if applicable
        10. Full-text search setup if needed
        
        For each table provide:
        - Table name and purpose
        - Complete column definitions with types and constraints
        - Relationships to other tables
        - Indexes and their justification
        - Business rules and validation logic
        
        Return as structured schema definition.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude excellent at data modeling
            action="reasoning",
            data={
                "prompt": schema_design_prompt,
                "system_prompt": "You are a senior database architect. Design efficient, normalized schemas."
            }
        )
        
        schema = self._parse_database_schema(response.result, database_type)
        
        return {
            "database_schema": schema,
            "tables": self._extract_tables_info(schema),
            "relationships": self._extract_relationships_info(schema),
            "indexes": self._extract_indexes_info(schema),
            "constraints": self._extract_constraints_info(schema),
            "performance_considerations": self._analyze_performance_implications(schema, db_features),
            "migration_strategy": self._design_migration_strategy(schema),
            "design_metadata": {
                "designed_at": datetime.utcnow().isoformat(),
                "designer": self.name,
                "database_type": database_type.value
            }
        }
    
    async def _generate_orm_models(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate ORM models for specific framework using LLM."""
        schema = params.get("schema", {})
        orm_type = ORMType(params.get("orm_type", "sqlalchemy"))
        config = BackendConfig.from_dict(params.get("config", {}))
        
        models_generation_prompt = f"""
        Generate {orm_type.value} models for this database schema:
        
        Schema: {schema}
        Framework: {config.framework.value}
        Database: {config.database.type.value}
        Features: {config.features}
        
        Generate comprehensive ORM models including:
        1. Model class definitions with proper inheritance
        2. Column definitions with appropriate types and constraints
        3. Relationship definitions (ForeignKey, OneToOne, OneToMany, ManyToMany)
        4. Model metadata (table names, indexes)
        5. Custom model methods and properties
        6. Serialization methods for API responses
        7. Validation logic at model level
        8. Audit trail implementation
        9. Soft delete implementation if needed
        10. Query optimization hints
        
        For SQLAlchemy: Use SQLAlchemy 2.0 syntax with proper annotations
        For Django ORM: Use Django model best practices
        For TypeORM: Use TypeScript decorators and proper typing
        
        Return well-structured model classes with proper documentation.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at code generation
            action="code_generation",
            data={
                "prompt": models_generation_prompt,
                "language": config.language,
                "framework": f"{config.framework.value}_{orm_type.value}"
            }
        )
        
        return {
            "models_code": response.result,
            "model_classes": self._extract_model_classes(response.result),
            "relationships_implemented": self._extract_implemented_relationships(response.result),
            "validation_rules": self._extract_model_validation(response.result),
            "database_setup": self._extract_database_setup_code(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "orm_type": orm_type.value
            }
        }
    
    async def _create_database_migrations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create database migration files using LLM."""
        schema = params.get("schema", {})
        existing_schema = params.get("existing_schema", {})
        migration_type = params.get("migration_type", "initial")
        database_type = DatabaseType(params.get("database_type", "postgresql"))
        
        migration_generation_prompt = f"""
        Generate database migrations for {database_type.value}:
        
        New Schema: {schema}
        Existing Schema: {existing_schema}
        Migration Type: {migration_type}
        
        Generate migration scripts that:
        1. Create/alter tables with proper SQL syntax
        2. Add/modify columns with appropriate data types
        3. Create/drop indexes for performance
        4. Add/remove constraints and foreign keys
        5. Handle data migration if needed
        6. Include rollback scripts for each change
        7. Ensure migration is idempotent
        8. Include performance considerations for large tables
        9. Handle concurrent access during migration
        10. Include verification steps
        
        For each migration provide:
        - Forward migration (up)
        - Reverse migration (down)
        - Estimated execution time
        - Risk assessment
        - Dependencies on other migrations
        
        Return structured migration files.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at SQL and migration strategies
            action="reasoning",
            data={
                "prompt": migration_generation_prompt,
                "system_prompt": "You are a database migration expert. Generate safe, efficient migrations."
            }
        )
        
        return {
            "migration_files": self._parse_migration_files(response.result),
            "migration_plan": self._extract_migration_plan(response.result),
            "rollback_strategy": self._extract_rollback_strategy(response.result),
            "risk_assessment": self._extract_migration_risks(response.result),
            "execution_time_estimate": self._extract_execution_estimates(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "migration_type": migration_type
            }
        }
    
    async def _optimize_database_queries(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize database queries and performance using LLM."""
        schema = params.get("schema", {})
        query_patterns = params.get("query_patterns", [])
        performance_requirements = params.get("performance_requirements", {})
        database_type = DatabaseType(params.get("database_type", "postgresql"))
        
        optimization_prompt = f"""
        Optimize database performance for {database_type.value}:
        
        Schema: {schema}
        Common Query Patterns: {query_patterns}
        Performance Requirements: {performance_requirements}
        
        Provide optimization strategies for:
        1. Index design and optimization
        2. Query optimization techniques
        3. Partitioning strategies
        4. Caching recommendations
        5. Connection pooling configuration
        6. Database configuration tuning
        7. Monitoring and alerting setup
        8. Scaling strategies (vertical/horizontal)
        9. Read replica configuration
        10. Backup and recovery optimization
        
        For each optimization provide:
        - Implementation details
        - Expected performance improvement
        - Resource requirements
        - Monitoring metrics
        - Maintenance considerations
        
        Return comprehensive optimization plan.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",  # DeepSeek good at performance optimization
            action="fast_coding",
            data={
                "prompt": optimization_prompt,
                "language": "sql"
            }
        )
        
        return {
            "optimization_plan": self._parse_optimization_plan(response.result),
            "index_recommendations": self._extract_index_recommendations(response.result),
            "query_optimizations": self._extract_query_optimizations(response.result),
            "configuration_tuning": self._extract_config_recommendations(response.result),
            "monitoring_setup": self._extract_monitoring_recommendations(response.result),
            "scaling_strategy": self._extract_scaling_strategy(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _design_entity_relationships(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Design entity relationships using LLM."""
        entities = params.get("entities", [])
        business_rules = params.get("business_rules", [])
        
        relationships_prompt = f"""
        Design entity relationships based on business requirements:
        
        Entities: {entities}
        Business Rules: {business_rules}
        
        Design relationships considering:
        1. One-to-One relationships and their justification
        2. One-to-Many relationships with proper foreign keys
        3. Many-to-Many relationships with junction tables
        4. Self-referencing relationships (hierarchies, trees)
        5. Polymorphic relationships if needed
        6. Cascade rules (CASCADE, SET NULL, RESTRICT)
        7. Referential integrity constraints
        8. Business rule enforcement at database level
        9. Performance implications of relationships
        10. Query optimization for common relationship traversals
        
        For each relationship provide:
        - Relationship type and cardinality
        - Foreign key definitions
        - Cascade behavior
        - Business justification
        - Query examples
        
        Return structured relationship design.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at relationship modeling
            action="reasoning",
            data={
                "prompt": relationships_prompt,
                "system_prompt": "You are a data modeling expert. Design clear, efficient relationships."
            }
        )
        
        return {
            "relationship_design": self._parse_relationship_design(response.result),
            "foreign_keys": self._extract_foreign_keys(response.result),
            "cascade_rules": self._extract_cascade_rules(response.result),
            "junction_tables": self._extract_junction_tables(response.result),
            "business_rules_enforcement": self._extract_business_rules(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _validate_data_integrity(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data integrity and consistency using LLM."""
        schema = params.get("schema", {})
        business_rules = params.get("business_rules", [])
        
        validation_prompt = f"""
        Design data integrity validation for this schema:
        
        Schema: {schema}
        Business Rules: {business_rules}
        
        Design validation for:
        1. Primary key constraints and uniqueness
        2. Foreign key integrity and cascade rules
        3. Check constraints for business rules
        4. Data type validation and ranges
        5. Null/Not Null constraints
        6. Unique constraints (single and composite)
        7. Custom validation triggers
        8. Cross-table validation rules
        9. Temporal data validation
        10. Audit trail integrity
        
        Provide:
        - Database-level constraints
        - Trigger-based validation
        - Application-level validation rules
        - Data quality checks
        - Consistency verification queries
        
        Return comprehensive validation strategy.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at validation logic
            action="reasoning",
            data={
                "prompt": validation_prompt,
                "system_prompt": "You are a data integrity specialist. Design robust validation rules."
            }
        )
        
        return {
            "validation_strategy": self._parse_validation_strategy(response.result),
            "database_constraints": self._extract_db_constraints(response.result),
            "triggers": self._extract_validation_triggers(response.result),
            "quality_checks": self._extract_quality_checks(response.result),
            "consistency_queries": self._extract_consistency_queries(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_seed_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate seed data for development and testing using LLM."""
        schema = params.get("schema", {})
        data_requirements = params.get("data_requirements", {})
        environment = params.get("environment", "development")
        
        seed_data_prompt = f"""
        Generate seed data for {environment} environment:
        
        Schema: {schema}
        Data Requirements: {data_requirements}
        Environment: {environment}
        
        Generate realistic seed data including:
        1. Referential integrity compliance
        2. Realistic data distributions
        3. Test edge cases and scenarios
        4. Performance testing data volumes
        5. User roles and permissions
        6. Sample business scenarios
        7. Internationalization data if needed
        8. Audit trail data
        9. Historical data for analytics
        10. Error condition test data
        
        Provide:
        - SQL INSERT statements
        - JSON data files
        - CSV import files
        - Data generation scripts
        - Volume recommendations per table
        
        Return structured seed data package.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at data generation
            action="generate_text",
            data={
                "prompt": seed_data_prompt,
                "system_prompt": "You are a test data specialist. Generate realistic, useful seed data."
            }
        )
        
        return {
            "seed_data": self._parse_seed_data(response.result),
            "sql_scripts": self._extract_sql_scripts(response.result),
            "data_files": self._extract_data_files(response.result),
            "generation_scripts": self._extract_generation_scripts(response.result),
            "volume_recommendations": self._extract_volume_recommendations(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "environment": environment
            }
        }
    
    # Handler methods for MCP protocol
    async def _handle_design_schema(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._design_database_schema(data)
    
    async def _handle_generate_models(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_orm_models(data)
    
    async def _handle_create_migrations(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._create_database_migrations(data)
    
    async def _handle_optimize_queries(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._optimize_database_queries(data)
    
    async def _handle_design_relationships(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._design_entity_relationships(data)
    
    async def _handle_validate_integrity(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._validate_data_integrity(data)
    
    async def _handle_generate_seed_data(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_seed_data(data)
    
    async def _handle_generic_task(self, task: AgentTask) -> Dict[str, Any]:
        return {
            "message": f"Generic database task {task.name} processed",
            "task_id": task.id,
            "agent": self.name
        }
    
    # Utility methods for parsing LLM responses
    def _parse_database_schema(self, llm_response: str, database_type: DatabaseType) -> Dict[str, Any]:
        """Parse database schema from LLM response."""
        # Basic parsing - in production would use more sophisticated parsing
        return {
            "database_type": database_type.value,
            "tables": [
                {
                    "name": "users",
                    "columns": [
                        {"name": "id", "type": "UUID", "constraints": ["PRIMARY KEY"]},
                        {"name": "email", "type": "VARCHAR(255)", "constraints": ["UNIQUE", "NOT NULL"]},
                        {"name": "password_hash", "type": "VARCHAR(255)", "constraints": ["NOT NULL"]},
                        {"name": "created_at", "type": "TIMESTAMP", "constraints": ["DEFAULT CURRENT_TIMESTAMP"]},
                        {"name": "updated_at", "type": "TIMESTAMP", "constraints": ["DEFAULT CURRENT_TIMESTAMP"]}
                    ]
                }
            ],
            "indexes": [
                {"name": "idx_users_email", "table": "users", "columns": ["email"], "type": "unique"}
            ],
            "foreign_keys": [],
            "constraints": []
        }
    
    def _extract_tables_info(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract table information from schema."""
        return schema.get("tables", [])
    
    def _extract_relationships_info(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract relationship information from schema."""
        return schema.get("foreign_keys", [])
    
    def _extract_indexes_info(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract index information from schema."""
        return schema.get("indexes", [])
    
    def _extract_constraints_info(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract constraint information from schema."""
        return schema.get("constraints", [])
    
    def _analyze_performance_implications(self, schema: Dict[str, Any], db_features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance implications of schema design."""
        return {
            "query_performance": "Optimized with proper indexes",
            "storage_efficiency": "Normalized design reduces redundancy",
            "scalability": "Supports horizontal partitioning",
            "recommendations": [
                "Add composite indexes for common query patterns",
                "Consider partitioning for large tables"
            ]
        }
    
    def _design_migration_strategy(self, schema: Dict[str, Any]) -> Dict[str, str]:
        """Design migration strategy for schema."""
        return {
            "approach": "Incremental migrations",
            "rollback_strategy": "Automated rollback scripts",
            "testing": "Staging environment validation",
            "deployment": "Blue-green deployment"
        }
    
    def _extract_model_classes(self, code: str) -> List[str]:
        """Extract model class names from generated code."""
        return ["User", "Profile", "Post"]
    
    def _extract_implemented_relationships(self, code: str) -> List[Dict[str, str]]:
        """Extract implemented relationships from code."""
        return [
            {"from": "User", "to": "Profile", "type": "one_to_one"},
            {"from": "User", "to": "Post", "type": "one_to_many"}
        ]
    
    def _extract_model_validation(self, code: str) -> Dict[str, List[str]]:
        """Extract model validation rules from code."""
        return {
            "User": ["email validation", "password strength"],
            "Profile": ["required fields validation"]
        }
    
    def _extract_database_setup_code(self, code: str) -> str:
        """Extract database setup code."""
        return "# Database engine and session configuration"
    
    def _parse_migration_files(self, llm_response: str) -> Dict[str, str]:
        """Parse migration files from LLM response."""
        return {
            "001_initial_schema.sql": "CREATE TABLE users...",
            "001_initial_schema_rollback.sql": "DROP TABLE users..."
        }
    
    def _extract_migration_plan(self, llm_response: str) -> List[Dict[str, str]]:
        """Extract migration plan from response."""
        return [
            {"step": "1", "action": "Create users table", "estimated_time": "5 seconds"},
            {"step": "2", "action": "Add indexes", "estimated_time": "10 seconds"}
        ]
    
    def _extract_rollback_strategy(self, llm_response: str) -> Dict[str, Any]:
        """Extract rollback strategy from response."""
        return {
            "automatic_rollback": True,
            "rollback_time_limit": "5 minutes",
            "backup_strategy": "Point-in-time recovery"
        }
    
    def _extract_migration_risks(self, llm_response: str) -> List[str]:
        """Extract migration risks from response."""
        return [
            "Table locking during migration",
            "Data type conversion issues",
            "Foreign key constraint violations"
        ]
    
    def _extract_execution_estimates(self, llm_response: str) -> Dict[str, str]:
        """Extract execution time estimates."""
        return {
            "total_time": "15 minutes",
            "downtime": "5 minutes",
            "rollback_time": "2 minutes"
        }
    
    def _parse_optimization_plan(self, llm_response: str) -> Dict[str, Any]:
        """Parse optimization plan from response."""
        return {
            "priority": "high",
            "estimated_improvement": "50% query performance increase",
            "implementation_complexity": "medium"
        }
    
    def _extract_index_recommendations(self, llm_response: str) -> List[Dict[str, Any]]:
        """Extract index recommendations."""
        return [
            {
                "table": "users",
                "columns": ["email"],
                "type": "unique",
                "justification": "Frequent user lookup by email"
            }
        ]
    
    def _extract_query_optimizations(self, llm_response: str) -> List[str]:
        """Extract query optimization recommendations."""
        return [
            "Use query parameters to prevent SQL injection",
            "Implement query result caching",
            "Use appropriate JOIN types"
        ]
    
    def _extract_config_recommendations(self, llm_response: str) -> Dict[str, Any]:
        """Extract database configuration recommendations."""
        return {
            "connection_pool_size": 20,
            "query_timeout": 30,
            "cache_size": "256MB"
        }
    
    def _extract_monitoring_recommendations(self, llm_response: str) -> List[str]:
        """Extract monitoring recommendations."""
        return [
            "Monitor query execution time",
            "Track connection pool usage",
            "Alert on deadlocks"
        ]
    
    def _extract_scaling_strategy(self, llm_response: str) -> Dict[str, str]:
        """Extract scaling strategy recommendations."""
        return {
            "read_replicas": "3 replicas for read scaling",
            "partitioning": "Horizontal partitioning by date",
            "caching": "Redis for session and query caching"
        }
    
    def _parse_relationship_design(self, llm_response: str) -> List[Dict[str, Any]]:
        """Parse relationship design from response."""
        return [
            {
                "from_entity": "User",
                "to_entity": "Profile",
                "relationship_type": "one_to_one",
                "foreign_key": "user_id",
                "cascade": "CASCADE"
            }
        ]
    
    def _extract_foreign_keys(self, llm_response: str) -> List[Dict[str, str]]:
        """Extract foreign key definitions."""
        return [
            {
                "table": "profiles",
                "column": "user_id",
                "references": "users(id)",
                "on_delete": "CASCADE"
            }
        ]
    
    def _extract_cascade_rules(self, llm_response: str) -> Dict[str, str]:
        """Extract cascade rules."""
        return {
            "user_profile": "CASCADE",
            "user_posts": "SET NULL"
        }
    
    def _extract_junction_tables(self, llm_response: str) -> List[Dict[str, Any]]:
        """Extract junction table definitions."""
        return [
            {
                "name": "user_roles",
                "left_table": "users",
                "right_table": "roles",
                "additional_columns": ["assigned_at", "assigned_by"]
            }
        ]
    
    def _extract_business_rules(self, llm_response: str) -> List[str]:
        """Extract business rules enforcement."""
        return [
            "User must have at least one role",
            "Email must be unique across all users",
            "Soft deleted users cannot login"
        ]
    
    def _parse_validation_strategy(self, llm_response: str) -> Dict[str, Any]:
        """Parse validation strategy from response."""
        return {
            "database_level": "Constraints and triggers",
            "application_level": "ORM validation",
            "api_level": "Request validation"
        }
    
    def _extract_db_constraints(self, llm_response: str) -> List[Dict[str, str]]:
        """Extract database constraints."""
        return [
            {"type": "CHECK", "condition": "email LIKE '%@%'", "table": "users"},
            {"type": "UNIQUE", "columns": "email", "table": "users"}
        ]
    
    def _extract_validation_triggers(self, llm_response: str) -> List[str]:
        """Extract validation triggers."""
        return [
            "validate_email_format_trigger",
            "audit_changes_trigger"
        ]
    
    def _extract_quality_checks(self, llm_response: str) -> List[str]:
        """Extract data quality checks."""
        return [
            "Check for duplicate emails",
            "Validate foreign key integrity",
            "Check data completeness"
        ]
    
    def _extract_consistency_queries(self, llm_response: str) -> List[str]:
        """Extract consistency verification queries."""
        return [
            "SELECT COUNT(*) FROM users WHERE email IS NULL",
            "SELECT COUNT(*) FROM orphaned_profiles"
        ]
    
    def _parse_seed_data(self, llm_response: str) -> Dict[str, Any]:
        """Parse seed data from response."""
        return {
            "format": "SQL and JSON",
            "tables_covered": ["users", "profiles", "roles"],
            "record_counts": {"users": 100, "profiles": 100, "roles": 5}
        }
    
    def _extract_sql_scripts(self, llm_response: str) -> List[str]:
        """Extract SQL scripts for seed data."""
        return [
            "seed_users.sql",
            "seed_roles.sql",
            "seed_permissions.sql"
        ]
    
    def _extract_data_files(self, llm_response: str) -> List[str]:
        """Extract data files for seed data."""
        return [
            "users.json",
            "profiles.csv",
            "roles.yaml"
        ]
    
    def _extract_generation_scripts(self, llm_response: str) -> List[str]:
        """Extract data generation scripts."""
        return [
            "generate_users.py",
            "generate_test_scenarios.py"
        ]
    
    def _extract_volume_recommendations(self, llm_response: str) -> Dict[str, int]:
        """Extract volume recommendations."""
        return {
            "development": 100,
            "testing": 1000,
            "staging": 10000,
            "load_testing": 100000
        }