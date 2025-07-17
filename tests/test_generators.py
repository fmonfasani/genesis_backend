"""
Tests for backend generators.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pathlib import Path

from genesis_backend.generators import (
    BackendGenerator,
    APIGenerator,
    ModelGenerator,
    AuthGenerator
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


class TestBackendGenerator:
    """Test BackendGenerator functionality."""
    
    @pytest.fixture
    def backend_generator(self, mock_template_engine):
        """Create BackendGenerator instance for testing."""
        return BackendGenerator(mock_template_engine)
    
    @pytest.fixture
    def sample_architecture(self):
        """Create sample architecture for testing."""
        return {
            "entities": [
                {"name": "User", "fields": ["id", "email", "password"]},
                {"name": "Product", "fields": ["id", "name", "price"]}
            ],
            "relationships": [
                {"from": "Order", "to": "User", "type": "many_to_one"}
            ],
            "api_design": {
                "version": "v1",
                "endpoints": [
                    {"path": "/users", "methods": ["GET", "POST"]},
                    {"path": "/products", "methods": ["GET", "POST"]}
                ]
            }
        }
    
    @pytest.mark.asyncio
    async def test_generate_fastapi_backend(self, backend_generator, fastapi_config, sample_architecture, tmp_path):
        """Test FastAPI backend generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated FastAPI code"
            
            result = await backend_generator.generate_backend(
                config=fastapi_config,
                architecture=sample_architecture,
                output_path=tmp_path
            )
            
            assert result["framework"] == "fastapi"
            assert "files" in result
            assert "generation_metadata" in result
            assert result["generation_metadata"]["framework"] == "fastapi"
            assert isinstance(result["files"], dict)
    
    @pytest.mark.asyncio
    async def test_generate_django_backend(self, backend_generator, django_config, sample_architecture, tmp_path):
        """Test Django backend generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated Django code"
            
            result = await backend_generator.generate_backend(
                config=django_config,
                architecture=sample_architecture,
                output_path=tmp_path
            )
            
            assert result["framework"] == "django"
            assert "files" in result
    
    @pytest.mark.asyncio
    async def test_generate_nestjs_backend(self, backend_generator, nestjs_config, sample_architecture, tmp_path):
        """Test NestJS backend generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated NestJS code"
            
            result = await backend_generator.generate_backend(
                config=nestjs_config,
                architecture=sample_architecture,
                output_path=tmp_path
            )
            
            assert result["framework"] == "nestjs"
            assert "files" in result
    
    @pytest.mark.asyncio
    async def test_unsupported_framework(self, backend_generator, sample_architecture, tmp_path):
        """Test error handling for unsupported framework."""
        # Create config with unsupported framework by directly setting enum
        config = BackendConfig(project_name="test")
        config.framework = "unsupported"  # This would normally not be possible
        
        with pytest.raises(ValueError, match="not supported"):
            await backend_generator.generate_backend(
                config=config,
                architecture=sample_architecture,
                output_path=tmp_path
            )
    
    @pytest.mark.asyncio
    async def test_output_directory_creation(self, backend_generator, fastapi_config, sample_architecture, tmp_path):
        """Test that output directory is created."""
        output_path = tmp_path / "backend_output"
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated code"
            
            await backend_generator.generate_backend(
                config=fastapi_config,
                architecture=sample_architecture,
                output_path=output_path
            )
            
            assert output_path.exists()
            assert output_path.is_dir()


class TestAPIGenerator:
    """Test APIGenerator functionality."""
    
    @pytest.fixture
    def api_generator(self, mock_template_engine):
        """Create APIGenerator instance for testing."""
        return APIGenerator(mock_template_engine)
    
    @pytest.fixture
    def sample_api_design(self):
        """Create sample API design for testing."""
        return {
            "version": "v1",
            "base_path": "/api/v1",
            "endpoints": [
                {
                    "path": "/users",
                    "methods": ["GET", "POST"],
                    "authentication_required": True
                },
                {
                    "path": "/users/{id}",
                    "methods": ["GET", "PUT", "DELETE"],
                    "authentication_required": True
                }
            ],
            "authentication": {
                "type": "JWT",
                "header": "Authorization"
            }
        }
    
    @pytest.mark.asyncio
    async def test_generate_fastapi_endpoints(self, api_generator, fastapi_config, sample_api_design):
        """Test FastAPI endpoints generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "FastAPI routes generated"
            
            result = await api_generator.generate_api_endpoints(
                api_design=sample_api_design,
                config=fastapi_config
            )
            
            assert isinstance(result, dict)
            # Should call LLM for code generation
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_django_views(self, api_generator, django_config, sample_api_design):
        """Test Django views generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Django views generated"
            
            result = await api_generator.generate_django_views(
                api_design=sample_api_design,
                config=django_config
            )
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_nestjs_controllers(self, api_generator, nestjs_config, sample_api_design):
        """Test NestJS controllers generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "NestJS controllers generated"
            
            result = await api_generator.generate_nestjs_controllers(
                api_design=sample_api_design,
                config=nestjs_config
            )
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_unsupported_framework_api(self, api_generator, sample_api_design):
        """Test error handling for unsupported framework in API generation."""
        config = BackendConfig(project_name="test")
        config.framework = "unsupported"
        
        with pytest.raises(ValueError, match="not supported"):
            await api_generator.generate_api_endpoints(
                api_design=sample_api_design,
                config=config
            )
    
    @pytest.mark.asyncio
    async def test_generate_api_tests(self, api_generator, fastapi_config, sample_api_design):
        """Test API tests generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "API tests generated"
            
            result = await api_generator.generate_api_tests(
                api_design=sample_api_design,
                config=fastapi_config
            )
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_api_documentation(self, api_generator, fastapi_config, sample_api_design):
        """Test API documentation generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "API documentation generated"
            
            result = await api_generator.generate_api_documentation(
                api_design=sample_api_design,
                config=fastapi_config
            )
            
            assert isinstance(result, dict)
            assert "docs/api/README.md" in result
            assert mock_protocol.called


class TestModelGenerator:
    """Test ModelGenerator functionality."""
    
    @pytest.fixture
    def model_generator(self, mock_template_engine):
        """Create ModelGenerator instance for testing."""
        return ModelGenerator(mock_template_engine)
    
    @pytest.mark.asyncio
    async def test_generate_sqlalchemy_models(self, model_generator, fastapi_config, sample_data_models):
        """Test SQLAlchemy models generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "SQLAlchemy models generated"
            
            result = await model_generator.generate_sqlalchemy_models(
                data_models=sample_data_models,
                config=fastapi_config
            )
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_django_models(self, model_generator, django_config, sample_data_models):
        """Test Django models generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Django models generated"
            
            result = await model_generator.generate_django_models(
                data_models=sample_data_models,
                config=django_config
            )
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_typeorm_entities(self, model_generator, nestjs_config, sample_data_models):
        """Test TypeORM entities generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "TypeORM entities generated"
            
            result = await model_generator.generate_typeorm_entities(
                data_models=sample_data_models,
                config=nestjs_config
            )
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_orm_selection(self, model_generator, sample_data_models):
        """Test automatic ORM selection based on framework."""
        # FastAPI should default to SQLAlchemy
        fastapi_config = BackendConfig(
            project_name="test",
            framework=BackendFramework.FASTAPI
        )
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Models generated"
            
            result = await model_generator.generate_models(
                data_models=sample_data_models,
                config=fastapi_config
            )
            
            assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_generate_model_tests(self, model_generator, fastapi_config, sample_data_models):
        """Test model tests generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Model tests generated"
            
            result = await model_generator.generate_model_tests(
                data_models=sample_data_models,
                config=fastapi_config
            )
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_model_factories(self, model_generator, fastapi_config, sample_data_models):
        """Test model factories generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Model factories generated"
            
            result = await model_generator.generate_model_factories(
                data_models=sample_data_models,
                config=fastapi_config
            )
            
            assert isinstance(result, dict)
            assert mock_protocol.called


class TestAuthGenerator:
    """Test AuthGenerator functionality."""
    
    @pytest.fixture
    def auth_generator(self, mock_template_engine):
        """Create AuthGenerator instance for testing."""
        return AuthGenerator(mock_template_engine)
    
    @pytest.mark.asyncio
    async def test_generate_fastapi_auth(self, auth_generator, fastapi_config):
        """Test FastAPI authentication generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "FastAPI auth generated"
            
            result = await auth_generator.generate_fastapi_auth(fastapi_config)
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_django_auth(self, auth_generator, django_config):
        """Test Django authentication generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Django auth generated"
            
            result = await auth_generator.generate_django_auth(django_config)
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_nestjs_auth(self, auth_generator, nestjs_config):
        """Test NestJS authentication generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "NestJS auth generated"
            
            result = await auth_generator.generate_nestjs_auth(nestjs_config)
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_unsupported_framework_auth(self, auth_generator):
        """Test error handling for unsupported framework in auth generation."""
        config = BackendConfig(project_name="test")
        config.framework = "unsupported"
        
        with pytest.raises(ValueError, match="not supported"):
            await auth_generator.generate_authentication(config)
    
    @pytest.mark.asyncio
    async def test_jwt_authentication_generation(self, auth_generator):
        """Test JWT authentication generation."""
        config = BackendConfig(
            project_name="test",
            framework=BackendFramework.FASTAPI,
            auth=AuthConfig(
                method=AuthMethod.JWT,
                secret_key="test-secret"
            )
        )
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "JWT auth generated"
            
            result = await auth_generator.generate_authentication(config)
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_oauth2_authentication_generation(self, auth_generator):
        """Test OAuth2 authentication generation."""
        config = BackendConfig(
            project_name="test",
            framework=BackendFramework.FASTAPI,
            auth=AuthConfig(
                method=AuthMethod.OAUTH2,
                oauth_providers=["google", "github"]
            )
        )
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "OAuth2 auth generated"
            
            result = await auth_generator.generate_authentication(config)
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_session_authentication_generation(self, auth_generator):
        """Test session authentication generation."""
        config = BackendConfig(
            project_name="test",
            framework=BackendFramework.DJANGO,
            auth=AuthConfig(method=AuthMethod.SESSION)
        )
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Session auth generated"
            
            result = await auth_generator.generate_authentication(config)
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_auth_tests(self, auth_generator, fastapi_config):
        """Test authentication tests generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Auth tests generated"
            
            result = await auth_generator.generate_auth_tests(fastapi_config)
            
            assert isinstance(result, dict)
            assert mock_protocol.called
    
    @pytest.mark.asyncio
    async def test_generate_auth_documentation(self, auth_generator, fastapi_config):
        """Test authentication documentation generation."""
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Auth docs generated"
            
            result = await auth_generator.generate_auth_documentation(fastapi_config)
            
            assert isinstance(result, dict)
            assert "docs/authentication.md" in result
            assert mock_protocol.called


class TestGeneratorIntegration:
    """Test integration between different generators."""
    
    @pytest.mark.asyncio
    async def test_full_stack_generation(self, mock_template_engine, fastapi_config, sample_data_models, sample_api_design):
        """Test complete stack generation using multiple generators."""
        # Initialize all generators
        backend_generator = BackendGenerator(mock_template_engine)
        api_generator = APIGenerator(mock_template_engine)
        model_generator = ModelGenerator(mock_template_engine)
        auth_generator = AuthGenerator(mock_template_engine)
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated code"
            
            # Generate models
            model_result = await model_generator.generate_models(
                data_models=sample_data_models,
                config=fastapi_config
            )
            
            # Generate API
            api_result = await api_generator.generate_api_endpoints(
                api_design=sample_api_design,
                config=fastapi_config
            )
            
            # Generate authentication
            auth_result = await auth_generator.generate_authentication(fastapi_config)
            
            # All should succeed
            assert isinstance(model_result, dict)
            assert isinstance(api_result, dict)
            assert isinstance(auth_result, dict)
    
    @pytest.mark.asyncio
    async def test_generator_error_handling(self, mock_template_engine, fastapi_config):
        """Test error handling in generators."""
        backend_generator = BackendGenerator(mock_template_engine)
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            # Simulate protocol failure
            mock_protocol.side_effect = Exception("Protocol error")
            
            with pytest.raises(Exception, match="Protocol error"):
                await backend_generator.generate_backend(
                    config=fastapi_config,
                    architecture={},
                    output_path=Path("/tmp")
                )


class TestGeneratorPerformance:
    """Test generator performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_concurrent_generation(self, mock_template_engine, fastapi_config):
        """Test concurrent generation operations."""
        import asyncio
        
        api_generator = APIGenerator(mock_template_engine)
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated code"
            
            # Create multiple concurrent generation tasks
            tasks = []
            for i in range(3):
                task = api_generator.generate_api_endpoints(
                    api_design={"version": f"v{i+1}", "endpoints": []},
                    config=fastapi_config
                )
                tasks.append(task)
            
            # Execute concurrently
            results = await asyncio.gather(*tasks)
            
            # All should complete successfully
            assert len(results) == 3
            for result in results:
                assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_large_schema_generation(self, model_generator, fastapi_config, performance_monitor):
        """Test generation with large data models."""
        # Create large schema
        large_schema = []
        for i in range(50):  # 50 models
            model = {
                "name": f"Model{i}",
                "fields": [f"field{j}" for j in range(20)]  # 20 fields each
            }
            large_schema.append(model)
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Large schema generated"
            
            performance_monitor.start()
            
            result = await model_generator.generate_models(
                data_models=large_schema,
                config=fastapi_config
            )
            
            performance_monitor.stop()
            
            assert isinstance(result, dict)
            assert performance_monitor.duration is not None
            # Should complete within reasonable time
            assert performance_monitor.duration < 30.0  # 30 seconds max
