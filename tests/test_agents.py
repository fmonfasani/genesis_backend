"""
Tests for backend generation agents.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from genesis_agents import AgentTask, TaskResult

from genesis_backend.agents import (
    ArchitectAgent,
    FastAPIAgent,
    DjangoAgent,
    NestJSAgent,
    DatabaseAgent,
    AuthAgent
)
from genesis_backend.config import (
    BackendConfig,
    BackendFramework,
    DatabaseType,
    AuthMethod,
    DatabaseConfig,
    AuthConfig,
    ORMType
)


class TestArchitectAgent:
    """Test ArchitectAgent functionality."""
    
    @pytest.fixture
    def architect_agent(self):
        """Create ArchitectAgent instance for testing."""
        return ArchitectAgent()
    
    @pytest.fixture
    def sample_config(self):
        """Create sample backend configuration."""
        return BackendConfig(
            project_name="test-api",
            description="Test API project",
            framework=BackendFramework.FASTAPI,
            features=["api", "authentication", "database"]
        )
    
    def test_agent_initialization(self, architect_agent):
        """Test agent initialization."""
        assert architect_agent.agent_id == "backend_architect"
        assert architect_agent.name == "Backend Architect Agent"
        assert architect_agent.agent_type == "architect"
        
        # Check capabilities
        expected_capabilities = [
            "analyze_backend_requirements",
            "design_api_architecture",
            "design_data_models",
            "select_backend_technologies",
            "design_service_architecture",
            "validate_backend_architecture"
        ]
        
        for capability in expected_capabilities:
            assert capability in architect_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_analyze_requirements_task(self, architect_agent, sample_config):
        """Test requirements analysis task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            # Mock LLM response
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Analysis complete"
            
            task = AgentTask(
                id="test-task-1",
                name="analyze_backend_requirements",
                params={
                    "description": "E-commerce API with user management",
                    "features": ["users", "products", "orders", "payments"],
                    "constraints": ["high_performance", "secure"]
                }
            )
            
            result = await architect_agent.execute_task(task)
            
            assert isinstance(result, TaskResult)
            assert result.task_id == "test-task-1"
            assert result.success is True
            assert "backend_requirements" in result.result
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_design_api_architecture_task(self, architect_agent):
        """Test API architecture design task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "API design complete"
            
            task = AgentTask(
                id="test-task-2",
                name="design_api_architecture",
                params={
                    "requirements": {"type": "REST API", "version": "v1"},
                    "entities": ["User", "Product", "Order"]
                }
            )
            
            result = await architect_agent.execute_task(task)
            
            assert result.success is True
            assert "api_specification" in result.result
            assert "endpoint_summary" in result.result
    
    @pytest.mark.asyncio
    async def test_unsupported_task(self, architect_agent):
        """Test handling of unsupported task."""
        task = AgentTask(
            id="test-task-3",
            name="unsupported_task",
            params={}
        )
        
        result = await architect_agent.execute_task(task)
        
        assert result.success is True
        assert "Generic backend architecture task" in result.result["message"]


class TestFastAPIAgent:
    """Test FastAPIAgent functionality."""
    
    @pytest.fixture
    def fastapi_agent(self):
        """Create FastAPIAgent instance for testing."""
        return FastAPIAgent()
    
    @pytest.fixture
    def fastapi_config(self):
        """Create FastAPI configuration."""
        return BackendConfig(
            project_name="fastapi-test",
            framework=BackendFramework.FASTAPI,
            database=DatabaseConfig(
                type=DatabaseType.POSTGRESQL,
                orm=ORMType.SQLALCHEMY
            ),
            auth=AuthConfig(
                method=AuthMethod.JWT,
                secret_key="test-secret"
            )
        )
    
    def test_agent_initialization(self, fastapi_agent):
        """Test FastAPI agent initialization."""
        assert fastapi_agent.agent_id == "fastapi_generator"
        assert fastapi_agent.name == "FastAPI Generator Agent"
        assert fastapi_agent.agent_type == "generator"
        
        expected_capabilities = [
            "generate_fastapi_app",
            "generate_fastapi_routes",
            "generate_pydantic_models",
            "generate_fastapi_middleware",
            "generate_fastapi_auth",
            "generate_sqlalchemy_models",
            "generate_fastapi_dependencies"
        ]
        
        for capability in expected_capabilities:
            assert capability in fastapi_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_generate_fastapi_app_task(self, fastapi_agent, fastapi_config):
        """Test FastAPI app generation task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "FastAPI app generated"
            
            task = AgentTask(
                id="fastapi-app-1",
                name="generate_fastapi_app",
                params={
                    "config": fastapi_config.to_dict(),
                    "architecture": {
                        "entities": ["User", "Product"],
                        "api_design": {"version": "v1", "prefix": "/api/v1"}
                    }
                }
            )
            
            result = await fastapi_agent.execute_task(task)
            
            assert result.success is True
            assert "main_application" in result.result
            assert result.metadata["framework"] == "fastapi"
    
    @pytest.mark.asyncio
    async def test_generate_pydantic_models_task(self, fastapi_agent):
        """Test Pydantic models generation task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Pydantic models generated"
            
            task = AgentTask(
                id="pydantic-models-1",
                name="generate_pydantic_models",
                params={
                    "data_models": [
                        {"name": "User", "fields": ["id", "email", "name"]},
                        {"name": "Product", "fields": ["id", "name", "price"]}
                    ],
                    "api_design": {"version": "v1"}
                }
            )
            
            result = await fastapi_agent.execute_task(task)
            
            assert result.success is True
            assert "schemas_code" in result.result


class TestDjangoAgent:
    """Test DjangoAgent functionality."""
    
    @pytest.fixture
    def django_agent(self):
        """Create DjangoAgent instance for testing."""
        return DjangoAgent()
    
    @pytest.fixture
    def django_config(self):
        """Create Django configuration."""
        return BackendConfig(
            project_name="django-test",
            framework=BackendFramework.DJANGO,
            database=DatabaseConfig(
                type=DatabaseType.POSTGRESQL,
                orm=ORMType.DJANGO_ORM
            ),
            auth=AuthConfig(
                method=AuthMethod.SESSION
            )
        )
    
    def test_agent_initialization(self, django_agent):
        """Test Django agent initialization."""
        assert django_agent.agent_id == "django_generator"
        assert django_agent.name == "Django Generator Agent"
        
        expected_capabilities = [
            "generate_django_project",
            "generate_django_models",
            "generate_django_views",
            "generate_django_urls",
            "generate_django_admin",
            "generate_django_rest_api",
            "generate_django_auth",
            "generate_django_settings"
        ]
        
        for capability in expected_capabilities:
            assert capability in django_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_generate_django_models_task(self, django_agent, django_config):
        """Test Django models generation task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Django models generated"
            
            task = AgentTask(
                id="django-models-1",
                name="generate_django_models",
                params={
                    "config": django_config.to_dict(),
                    "data_models": [
                        {"name": "User", "fields": ["email", "first_name", "last_name"]},
                        {"name": "Post", "fields": ["title", "content", "author"]}
                    ],
                    "relationships": [
                        {"from": "Post", "to": "User", "type": "ForeignKey"}
                    ]
                }
            )
            
            result = await django_agent.execute_task(task)
            
            assert result.success is True
            assert "models_code" in result.result
            assert result.metadata["framework"] == "django"


class TestNestJSAgent:
    """Test NestJSAgent functionality."""
    
    @pytest.fixture
    def nestjs_agent(self):
        """Create NestJSAgent instance for testing."""
        return NestJSAgent()
    
    @pytest.fixture
    def nestjs_config(self):
        """Create NestJS configuration."""
        return BackendConfig(
            project_name="nestjs-test",
            framework=BackendFramework.NESTJS,
            database=DatabaseConfig(
                type=DatabaseType.POSTGRESQL,
                orm=ORMType.TYPEORM
            ),
            auth=AuthConfig(
                method=AuthMethod.JWT,
                secret_key="nestjs-secret"
            )
        )
    
    def test_agent_initialization(self, nestjs_agent):
        """Test NestJS agent initialization."""
        assert nestjs_agent.agent_id == "nestjs_generator"
        assert nestjs_agent.name == "NestJS Generator Agent"
        
        expected_capabilities = [
            "generate_nestjs_project",
            "generate_nestjs_modules",
            "generate_nestjs_controllers",
            "generate_nestjs_services",
            "generate_typeorm_entities",
            "generate_nestjs_auth",
            "generate_nestjs_dtos",
            "generate_nestjs_pipes"
        ]
        
        for capability in expected_capabilities:
            assert capability in nestjs_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_generate_nestjs_controllers_task(self, nestjs_agent, nestjs_config):
        """Test NestJS controllers generation task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "NestJS controllers generated"
            
            task = AgentTask(
                id="nestjs-controllers-1",
                name="generate_nestjs_controllers",
                params={
                    "config": nestjs_config.to_dict(),
                    "api_design": {
                        "endpoints": [
                            {"path": "/users", "method": "GET", "handler": "findAll"},
                            {"path": "/users/:id", "method": "GET", "handler": "findOne"}
                        ]
                    },
                    "entities": ["User", "Product"]
                }
            )
            
            result = await nestjs_agent.execute_task(task)
            
            assert result.success is True
            assert "controllers_code" in result.result
            assert result.metadata["framework"] == "nestjs"


class TestDatabaseAgent:
    """Test DatabaseAgent functionality."""
    
    @pytest.fixture
    def database_agent(self):
        """Create DatabaseAgent instance for testing."""
        return DatabaseAgent()
    
    def test_agent_initialization(self, database_agent):
        """Test database agent initialization."""
        assert database_agent.agent_id == "database_specialist"
        assert database_agent.name == "Database Specialist Agent"
        
        expected_capabilities = [
            "design_database_schema",
            "generate_orm_models",
            "create_database_migrations",
            "optimize_database_queries",
            "design_relationships",
            "validate_data_integrity",
            "generate_seed_data"
        ]
        
        for capability in expected_capabilities:
            assert capability in database_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_design_database_schema_task(self, database_agent):
        """Test database schema design task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Database schema designed"
            
            task = AgentTask(
                id="db-schema-1",
                name="design_database_schema",
                params={
                    "entities": [
                        {"name": "User", "attributes": ["id", "email", "password"]},
                        {"name": "Product", "attributes": ["id", "name", "price"]}
                    ],
                    "requirements": {
                        "performance": "high",
                        "scalability": "horizontal"
                    },
                    "database_type": "postgresql"
                }
            )
            
            result = await database_agent.execute_task(task)
            
            assert result.success is True
            assert "database_schema" in result.result
            assert "tables" in result.result
            assert "relationships" in result.result
    
    @pytest.mark.asyncio
    async def test_generate_orm_models_task(self, database_agent):
        """Test ORM models generation task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "ORM models generated"
            
            task = AgentTask(
                id="orm-models-1",
                name="generate_orm_models",
                params={
                    "schema": {
                        "tables": [
                            {"name": "users", "columns": ["id", "email", "password_hash"]},
                            {"name": "products", "columns": ["id", "name", "price"]}
                        ]
                    },
                    "orm_type": "sqlalchemy",
                    "config": {
                        "framework": "fastapi",
                        "database": {"type": "postgresql"}
                    }
                }
            )
            
            result = await database_agent.execute_task(task)
            
            assert result.success is True
            assert "models_code" in result.result


class TestAuthAgent:
    """Test AuthAgent functionality."""
    
    @pytest.fixture
    def auth_agent(self):
        """Create AuthAgent instance for testing."""
        return AuthAgent()
    
    def test_agent_initialization(self, auth_agent):
        """Test auth agent initialization."""
        assert auth_agent.agent_id == "auth_specialist"
        assert auth_agent.name == "Authentication Specialist Agent"
        
        expected_capabilities = [
            "generate_jwt_auth",
            "generate_oauth2_auth",
            "generate_session_auth",
            "generate_user_management",
            "generate_role_permissions",
            "generate_auth_middleware",
            "generate_password_security",
            "generate_social_auth"
        ]
        
        for capability in expected_capabilities:
            assert capability in auth_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_generate_jwt_auth_task(self, auth_agent):
        """Test JWT authentication generation task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "JWT auth generated"
            
            task = AgentTask(
                id="jwt-auth-1",
                name="generate_jwt_auth",
                params={
                    "config": {
                        "framework": "fastapi",
                        "auth": {
                            "method": "jwt",
                            "secret_key": "test-secret",
                            "algorithm": "HS256",
                            "access_token_expire_minutes": 30,
                            "refresh_token_expire_days": 7
                        }
                    },
                    "user_model": {
                        "fields": ["id", "email", "password_hash", "is_active"]
                    }
                }
            )
            
            result = await auth_agent.execute_task(task)
            
            assert result.success is True
            assert "auth_code" in result.result
            assert "endpoints" in result.result
            assert "middleware" in result.result
    
    @pytest.mark.asyncio
    async def test_generate_user_management_task(self, auth_agent):
        """Test user management system generation task."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "User management generated"
            
            task = AgentTask(
                id="user-mgmt-1",
                name="generate_user_management",
                params={
                    "config": {
                        "framework": "fastapi",
                        "auth": {"method": "jwt"}
                    },
                    "user_fields": [
                        {"name": "email", "type": "string", "required": True},
                        {"name": "first_name", "type": "string"},
                        {"name": "last_name", "type": "string"},
                        {"name": "is_active", "type": "boolean", "default": True}
                    ]
                }
            )
            
            result = await auth_agent.execute_task(task)
            
            assert result.success is True
            assert "user_management_code" in result.result
            assert "user_model" in result.result
            assert "crud_operations" in result.result


class TestAgentErrorHandling:
    """Test error handling in agents."""
    
    @pytest.mark.asyncio
    async def test_agent_task_failure(self):
        """Test agent behavior when task fails."""
        agent = ArchitectAgent()
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            # Simulate protocol failure
            mock_protocol.side_effect = Exception("Protocol connection failed")
            
            task = AgentTask(
                id="failing-task",
                name="analyze_backend_requirements",
                params={"description": "Test project"}
            )
            
            result = await agent.execute_task(task)
            
            assert result.success is False
            assert "Protocol connection failed" in result.error
            assert result.task_id == "failing-task"
    
    @pytest.mark.asyncio
    async def test_invalid_task_params(self):
        """Test agent behavior with invalid task parameters."""
        agent = FastAPIAgent()
        
        task = AgentTask(
            id="invalid-params-task",
            name="generate_fastapi_app",
            params={}  # Missing required config
        )
        
        # This should handle gracefully and not crash
        result = await agent.execute_task(task)
        
        # The exact behavior depends on implementation,
        # but it should not raise an unhandled exception
        assert isinstance(result, TaskResult)
        assert result.task_id == "invalid-params-task"


class TestAgentIntegration:
    """Test agent integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_multi_agent_workflow(self):
        """Test workflow involving multiple agents."""
        # This would test a realistic scenario where multiple agents
        # work together to generate a complete backend
        
        architect = ArchitectAgent()
        fastapi_agent = FastAPIAgent()
        database_agent = DatabaseAgent()
        auth_agent = AuthAgent()
        
        # Step 1: Architect analyzes requirements
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Analysis complete"
            
            requirements_task = AgentTask(
                id="requirements-1",
                name="analyze_backend_requirements",
                params={
                    "description": "E-commerce API",
                    "features": ["users", "products", "orders", "payments"]
                }
            )
            
            architect_result = await architect.execute_task(requirements_task)
            assert architect_result.success is True
        
        # Step 2: Database agent designs schema
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Schema designed"
            
            schema_task = AgentTask(
                id="schema-1",
                name="design_database_schema",
                params={
                    "entities": ["User", "Product", "Order"],
                    "database_type": "postgresql"
                }
            )
            
            db_result = await database_agent.execute_task(schema_task)
            assert db_result.success is True
        
        # Step 3: Auth agent generates authentication
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Auth generated"
            
            auth_task = AgentTask(
                id="auth-1",
                name="generate_jwt_auth",
                params={
                    "config": {
                        "framework": "fastapi",
                        "auth": {"method": "jwt"}
                    }
                }
            )
            
            auth_result = await auth_agent.execute_task(auth_task)
            assert auth_result.success is True
        
        # Step 4: FastAPI agent generates application
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "FastAPI app generated"
            
            app_task = AgentTask(
                id="app-1",
                name="generate_fastapi_app",
                params={
                    "config": {
                        "project_name": "ecommerce-api",
                        "framework": "fastapi"
                    }
                }
            )
            
            app_result = await fastapi_agent.execute_task(app_task)
            assert app_result.success is True
        
        # All agents should have completed successfully
        assert architect_result.success is True
        assert db_result.success is True
        assert auth_result.success is True
        assert app_result.success is True
