"""
Integration tests for Genesis Backend.

These tests verify that different components work together correctly
and test realistic end-to-end scenarios.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from typing import Dict, Any

from genesis_backend import (
    BackendConfig,
    BackendFramework,
    DatabaseType,
    AuthMethod,
    get_agents
)
from genesis_backend.agents import (
    ArchitectAgent,
    FastAPIAgent,
    DjangoAgent,
    NestJSAgent,
    DatabaseAgent,
    AuthAgent
)
from genesis_backend.generators import (
    BackendGenerator,
    APIGenerator,
    ModelGenerator,
    AuthGenerator
)
from genesis_agents import AgentTask


class TestEndToEndGeneration:
    """Test complete end-to-end backend generation scenarios."""
    
    @pytest.fixture
    def ecommerce_requirements(self):
        """E-commerce application requirements."""
        return {
            "description": "E-commerce platform with user management, product catalog, and order processing",
            "features": ["users", "products", "orders", "payments", "inventory", "reviews"],
            "entities": [
                {
                    "name": "User",
                    "attributes": ["id", "email", "password", "first_name", "last_name", "phone", "address"],
                    "relationships": ["orders", "reviews", "cart"]
                },
                {
                    "name": "Product",
                    "attributes": ["id", "name", "description", "price", "stock", "category", "images"],
                    "relationships": ["reviews", "order_items", "categories"]
                },
                {
                    "name": "Order",
                    "attributes": ["id", "user_id", "total_amount", "status", "shipping_address", "payment_method"],
                    "relationships": ["user", "order_items", "payments"]
                },
                {
                    "name": "OrderItem",
                    "attributes": ["id", "order_id", "product_id", "quantity", "unit_price"],
                    "relationships": ["order", "product"]
                },
                {
                    "name": "Review",
                    "attributes": ["id", "user_id", "product_id", "rating", "comment", "created_at"],
                    "relationships": ["user", "product"]
                }
            ],
            "constraints": [
                "high_performance",
                "secure_payments",
                "scalable",
                "mobile_friendly_api"
            ]
        }
    
    @pytest.fixture
    def blog_requirements(self):
        """Blog application requirements."""
        return {
            "description": "Multi-user blog platform with content management and commenting",
            "features": ["authors", "posts", "comments", "categories", "tags", "media"],
            "entities": [
                {
                    "name": "Author",
                    "attributes": ["id", "username", "email", "bio", "avatar", "social_links"],
                    "relationships": ["posts", "comments"]
                },
                {
                    "name": "Post",
                    "attributes": ["id", "title", "slug", "content", "excerpt", "author_id", "status", "published_at"],
                    "relationships": ["author", "comments", "categories", "tags"]
                },
                {
                    "name": "Comment",
                    "attributes": ["id", "post_id", "author_id", "content", "parent_id", "approved"],
                    "relationships": ["post", "author", "replies"]
                },
                {
                    "name": "Category",
                    "attributes": ["id", "name", "slug", "description"],
                    "relationships": ["posts"]
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_fastapi_ecommerce_generation(self, ecommerce_requirements, tmp_path):
        """Test complete FastAPI e-commerce application generation."""
        # Configuration
        config = BackendConfig(
            project_name="ecommerce-api",
            description=ecommerce_requirements["description"],
            framework=BackendFramework.FASTAPI,
            features=["api", "authentication", "database", "payments", "documentation"],
            database={
                "type": "postgresql",
                "host": "localhost",
                "name": "ecommerce_db",
                "orm": "sqlalchemy"
            },
            auth={
                "method": "jwt",
                "secret_key": "test-secret-key",
                "access_token_expire_minutes": 30
            }
        )
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated FastAPI ecommerce code"
            
            # Step 1: Initialize agents
            architect = ArchitectAgent()
            fastapi_agent = FastAPIAgent()
            database_agent = DatabaseAgent()
            auth_agent = AuthAgent()
            
            # Step 2: Architecture analysis
            analysis_task = AgentTask(
                id="analysis-1",
                name="analyze_backend_requirements",
                params=ecommerce_requirements
            )
            
            analysis_result = await architect.execute_task(analysis_task)
            assert analysis_result.success
            
            # Step 3: Database schema design
            schema_task = AgentTask(
                id="schema-1",
                name="design_database_schema",
                params={
                    "entities": ecommerce_requirements["entities"],
                    "database_type": "postgresql"
                }
            )
            
            schema_result = await database_agent.execute_task(schema_task)
            assert schema_result.success
            
            # Step 4: API design
            api_task = AgentTask(
                id="api-1",
                name="design_api_architecture",
                params={
                    "requirements": ecommerce_requirements,
                    "entities": ecommerce_requirements["entities"]
                }
            )
            
            api_result = await architect.execute_task(api_task)
            assert api_result.success
            
            # Step 5: Authentication system
            auth_task = AgentTask(
                id="auth-1",
                name="generate_jwt_auth",
                params={"config": config.to_dict()}
            )
            
            auth_result = await auth_agent.execute_task(auth_task)
            assert auth_result.success
            
            # Step 6: FastAPI application
            app_task = AgentTask(
                id="app-1",
                name="generate_fastapi_app",
                params={
                    "config": config.to_dict(),
                    "architecture": {
                        "entities": ecommerce_requirements["entities"],
                        "api_design": api_result.result,
                        "database_schema": schema_result.result
                    }
                }
            )
            
            app_result = await fastapi_agent.execute_task(app_task)
            assert app_result.success
            
            # Verify all components were generated
            assert analysis_result.success
            assert schema_result.success
            assert api_result.success
            assert auth_result.success
            assert app_result.success
    
    @pytest.mark.asyncio
    async def test_django_blog_generation(self, blog_requirements, tmp_path):
        """Test complete Django blog application generation."""
        config = BackendConfig(
            project_name="blog-platform",
            description=blog_requirements["description"],
            framework=BackendFramework.DJANGO,
            features=["admin", "rest_api", "authentication", "media", "search"],
            database={
                "type": "postgresql",
                "host": "localhost",
                "name": "blog_db",
                "orm": "django_orm"
            },
            auth={
                "method": "session",
                "session_timeout": 3600
            }
        )
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated Django blog code"
            
            # Initialize agents
            architect = ArchitectAgent()
            django_agent = DjangoAgent()
            database_agent = DatabaseAgent()
            auth_agent = AuthAgent()
            
            # Generate complete Django blog
            tasks = [
                AgentTask(
                    id="blog-analysis",
                    name="analyze_backend_requirements",
                    params=blog_requirements
                ),
                AgentTask(
                    id="blog-schema",
                    name="design_database_schema",
                    params={
                        "entities": blog_requirements["entities"],
                        "database_type": "postgresql"
                    }
                ),
                AgentTask(
                    id="blog-models",
                    name="generate_django_models",
                    params={
                        "config": config.to_dict(),
                        "data_models": blog_requirements["entities"]
                    }
                ),
                AgentTask(
                    id="blog-admin",
                    name="generate_django_admin",
                    params={
                        "models": blog_requirements["entities"]
                    }
                ),
                AgentTask(
                    id="blog-auth",
                    name="generate_session_auth",
                    params={"config": config.to_dict()}
                )
            ]
            
            # Execute all tasks
            results = []
            for task in tasks:
                if task.name.startswith("analyze") or task.name.startswith("design"):
                    result = await architect.execute_task(task)
                elif task.name.startswith("generate_django"):
                    result = await django_agent.execute_task(task)
                elif task.name.startswith("generate_session"):
                    result = await auth_agent.execute_task(task)
                else:
                    result = await database_agent.execute_task(task)
                
                results.append(result)
                assert result.success, f"Task {task.name} failed"
            
            assert len(results) == len(tasks)
            assert all(r.success for r in results)
    
    @pytest.mark.asyncio
    async def test_nestjs_microservice_generation(self, tmp_path):
        """Test NestJS microservice generation."""
        microservice_requirements = {
            "description": "User management microservice",
            "features": ["users", "authentication", "authorization", "audit"],
            "entities": [
                {
                    "name": "User",
                    "attributes": ["id", "email", "password", "roles", "permissions", "last_login"],
                    "relationships": ["roles", "audit_logs"]
                },
                {
                    "name": "Role",
                    "attributes": ["id", "name", "permissions"],
                    "relationships": ["users"]
                },
                {
                    "name": "AuditLog",
                    "attributes": ["id", "user_id", "action", "resource", "timestamp", "ip_address"],
                    "relationships": ["user"]
                }
            ]
        }
        
        config = BackendConfig(
            project_name="user-microservice",
            framework=BackendFramework.NESTJS,
            features=["api", "authentication", "authorization", "typeorm", "swagger"],
            database={
                "type": "postgresql",
                "host": "localhost",
                "name": "users_db",
                "orm": "typeorm"
            },
            auth={
                "method": "jwt",
                "secret_key": "microservice-secret",
                "access_token_expire_minutes": 15
            }
        )
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated NestJS microservice code"
            
            # Use BackendGenerator for complete generation
            backend_generator = BackendGenerator()
            
            architecture = {
                "entities": microservice_requirements["entities"],
                "api_design": {
                    "version": "v1",
                    "endpoints": [
                        {"path": "/users", "methods": ["GET", "POST"]},
                        {"path": "/users/{id}", "methods": ["GET", "PUT", "DELETE"]},
                        {"path": "/auth/login", "methods": ["POST"]},
                        {"path": "/roles", "methods": ["GET", "POST"]},
                        {"path": "/audit", "methods": ["GET"]}
                    ]
                }
            }
            
            result = await backend_generator.generate_backend(
                config=config,
                architecture=architecture,
                output_path=tmp_path
            )
            
            assert result["framework"] == "nestjs"
            assert "files" in result
            assert result["generation_metadata"]["framework"] == "nestjs"


class TestAgentOrchestration:
    """Test orchestration between multiple agents."""
    
    @pytest.mark.asyncio
    async def test_agent_workflow_coordination(self):
        """Test coordinated workflow between agents."""
        # Initialize all agents
        agents = {
            "architect": ArchitectAgent(),
            "fastapi": FastAPIAgent(),
            "database": DatabaseAgent(),
            "auth": AuthAgent()
        }
        
        workflow_state = {}
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated content"
            
            # Step 1: Requirements analysis
            requirements_task = AgentTask(
                id="req-1",
                name="analyze_backend_requirements",
                params={
                    "description": "Simple API service",
                    "features": ["api", "authentication"]
                }
            )
            
            req_result = await agents["architect"].execute_task(requirements_task)
            workflow_state["requirements"] = req_result.result
            
            # Step 2: Database design (depends on requirements)
            db_task = AgentTask(
                id="db-1",
                name="design_database_schema",
                params={
                    "entities": [{"name": "User", "attributes": ["id", "email"]}],
                    "requirements": workflow_state["requirements"]
                }
            )
            
            db_result = await agents["database"].execute_task(db_task)
            workflow_state["database"] = db_result.result
            
            # Step 3: Authentication (depends on requirements and database)
            auth_task = AgentTask(
                id="auth-1",
                name="generate_jwt_auth",
                params={
                    "config": {
                        "framework": "fastapi",
                        "auth": {"method": "jwt"}
                    },
                    "user_model": workflow_state["database"]
                }
            )
            
            auth_result = await agents["auth"].execute_task(auth_task)
            workflow_state["authentication"] = auth_result.result
            
            # Step 4: Application generation (depends on all previous)
            app_task = AgentTask(
                id="app-1",
                name="generate_fastapi_app",
                params={
                    "config": {"project_name": "test-api", "framework": "fastapi"},
                    "architecture": workflow_state
                }
            )
            
            app_result = await agents["fastapi"].execute_task(app_task)
            
            # Verify workflow state propagation
            assert all(result.success for result in [req_result, db_result, auth_result, app_result])
            assert len(workflow_state) == 3  # requirements, database, authentication
    
    @pytest.mark.asyncio
    async def test_parallel_agent_execution(self):
        """Test parallel execution of independent agent tasks."""
        api_generator = APIGenerator()
        model_generator = ModelGenerator()
        auth_generator = AuthGenerator()
        
        config = BackendConfig(
            project_name="parallel-test",
            framework=BackendFramework.FASTAPI
        )
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Parallel generated content"
            
            # Create independent tasks that can run in parallel
            tasks = [
                api_generator.generate_api_endpoints(
                    api_design={"version": "v1", "endpoints": []},
                    config=config
                ),
                model_generator.generate_models(
                    data_models=[{"name": "User", "fields": ["id", "email"]}],
                    config=config
                ),
                auth_generator.generate_authentication(config)
            ]
            
            # Execute in parallel
            results = await asyncio.gather(*tasks)
            
            assert len(results) == 3
            assert all(isinstance(result, dict) for result in results)
    
    @pytest.mark.asyncio
    async def test_error_handling_in_workflow(self):
        """Test error handling when agents fail in a workflow."""
        architect = ArchitectAgent()
        fastapi_agent = FastAPIAgent()
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            # First call succeeds, second fails
            mock_protocol.side_effect = [
                AsyncMock(result="Success"),
                Exception("Network error")
            ]
            
            # First task succeeds
            task1 = AgentTask(
                id="success-task",
                name="analyze_backend_requirements",
                params={"description": "Test"}
            )
            
            result1 = await architect.execute_task(task1)
            assert result1.success
            
            # Second task fails
            task2 = AgentTask(
                id="fail-task",
                name="generate_fastapi_app",
                params={"config": {"project_name": "test"}}
            )
            
            result2 = await fastapi_agent.execute_task(task2)
            assert not result2.success
            assert "Network error" in result2.error


class TestRealWorldScenarios:
    """Test real-world backend generation scenarios."""
    
    @pytest.mark.asyncio
    async def test_multi_tenant_saas_generation(self, tmp_path):
        """Test generation of multi-tenant SaaS backend."""
        saas_config = BackendConfig(
            project_name="saas-platform",
            description="Multi-tenant SaaS platform with organizations and workspaces",
            framework=BackendFramework.FASTAPI,
            features=["api", "authentication", "multi_tenancy", "billing", "webhooks"],
            database={
                "type": "postgresql",
                "name": "saas_db",
                "orm": "sqlalchemy"
            },
            auth={
                "method": "jwt",
                "secret_key": "saas-secret-key"
            }
        )
        
        saas_architecture = {
            "entities": [
                {
                    "name": "Organization",
                    "attributes": ["id", "name", "subdomain", "plan", "billing_info"],
                    "relationships": ["users", "workspaces", "subscriptions"]
                },
                {
                    "name": "User",
                    "attributes": ["id", "email", "role", "organization_id"],
                    "relationships": ["organization", "workspaces"]
                },
                {
                    "name": "Workspace",
                    "attributes": ["id", "name", "organization_id", "settings"],
                    "relationships": ["organization", "users", "projects"]
                }
            ],
            "multi_tenancy": {
                "strategy": "shared_database_separate_schema",
                "tenant_identifier": "organization_id"
            }
        }
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated SaaS backend"
            
            backend_generator = BackendGenerator()
            
            result = await backend_generator.generate_backend(
                config=saas_config,
                architecture=saas_architecture,
                output_path=tmp_path
            )
            
            assert result["framework"] == "fastapi"
            assert "files" in result
    
    @pytest.mark.asyncio
    async def test_api_gateway_generation(self, tmp_path):
        """Test generation of API gateway service."""
        gateway_config = BackendConfig(
            project_name="api-gateway",
            description="API Gateway with routing, authentication, and rate limiting",
            framework=BackendFramework.FASTAPI,
            features=["api", "authentication", "rate_limiting", "logging", "monitoring"],
            auth={
                "method": "jwt",
                "secret_key": "gateway-secret"
            }
        )
        
        gateway_architecture = {
            "services": [
                {"name": "user-service", "base_url": "http://user-service:8001"},
                {"name": "order-service", "base_url": "http://order-service:8002"},
                {"name": "product-service", "base_url": "http://product-service:8003"}
            ],
            "routing_rules": [
                {"path": "/api/users/**", "service": "user-service"},
                {"path": "/api/orders/**", "service": "order-service"},
                {"path": "/api/products/**", "service": "product-service"}
            ],
            "middleware": ["authentication", "rate_limiting", "cors", "logging"]
        }
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated API Gateway"
            
            backend_generator = BackendGenerator()
            
            result = await backend_generator.generate_backend(
                config=gateway_config,
                architecture=gateway_architecture,
                output_path=tmp_path
            )
            
            assert result["framework"] == "fastapi"
    
    @pytest.mark.asyncio
    async def test_data_pipeline_backend(self, tmp_path):
        """Test generation of data pipeline backend."""
        pipeline_config = BackendConfig(
            project_name="data-pipeline",
            description="Data processing pipeline with ETL capabilities",
            framework=BackendFramework.FASTAPI,
            features=["api", "data_processing", "scheduling", "monitoring"],
            database={
                "type": "postgresql",
                "name": "pipeline_db"
            }
        )
        
        pipeline_architecture = {
            "data_sources": [
                {"name": "postgres", "type": "postgresql"},
                {"name": "s3", "type": "s3"},
                {"name": "api", "type": "rest_api"}
            ],
            "processors": [
                {"name": "data_cleaner", "type": "pandas"},
                {"name": "transformer", "type": "custom"},
                {"name": "validator", "type": "pydantic"}
            ],
            "destinations": [
                {"name": "warehouse", "type": "postgresql"},
                {"name": "analytics", "type": "elasticsearch"}
            ]
        }
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated data pipeline"
            
            backend_generator = BackendGenerator()
            
            result = await backend_generator.generate_backend(
                config=pipeline_config,
                architecture=pipeline_architecture,
                output_path=tmp_path
            )
            
            assert result["framework"] == "fastapi"


class TestPerformanceIntegration:
    """Test performance aspects of integrated generation."""
    
    @pytest.mark.asyncio
    async def test_large_scale_generation_performance(self, performance_monitor):
        """Test performance with large-scale generation."""
        # Create large configuration
        large_config = BackendConfig(
            project_name="large-scale-app",
            framework=BackendFramework.FASTAPI,
            features=["api", "authentication", "database", "caching", "search", "analytics"]
        )
        
        # Large architecture with many entities
        large_architecture = {
            "entities": [
                {
                    "name": f"Entity{i}",
                    "attributes": [f"field{j}" for j in range(10)],
                    "relationships": [f"rel{k}" for k in range(3)]
                }
                for i in range(20)  # 20 entities
            ],
            "api_design": {
                "endpoints": [
                    {"path": f"/api/entity{i}", "methods": ["GET", "POST", "PUT", "DELETE"]}
                    for i in range(20)
                ]
            }
        }
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated large scale backend"
            
            backend_generator = BackendGenerator()
            
            performance_monitor.start()
            
            result = await backend_generator.generate_backend(
                config=large_config,
                architecture=large_architecture,
                output_path=Path("/tmp/large_backend")
            )
            
            performance_monitor.stop()
            
            assert result["framework"] == "fastapi"
            assert performance_monitor.duration is not None
            # Should complete within reasonable time even for large projects
            assert performance_monitor.duration < 60.0  # 1 minute max
    
    @pytest.mark.asyncio
    async def test_concurrent_project_generation(self):
        """Test concurrent generation of multiple projects."""
        configs = [
            BackendConfig(project_name=f"project-{i}", framework=BackendFramework.FASTAPI)
            for i in range(5)
        ]
        
        architectures = [
            {"entities": [{"name": f"Entity{i}", "attributes": ["id", "name"]}]}
            for i in range(5)
        ]
        
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated concurrent project"
            
            backend_generator = BackendGenerator()
            
            # Generate multiple projects concurrently
            tasks = [
                backend_generator.generate_backend(
                    config=configs[i],
                    architecture=architectures[i],
                    output_path=Path(f"/tmp/project_{i}")
                )
                for i in range(5)
            ]
            
            results = await asyncio.gather(*tasks)
            
            assert len(results) == 5
            assert all(result["framework"] == "fastapi" for result in results)


class TestConfigurationIntegration:
    """Test configuration handling in integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_config_validation_in_generation(self):
        """Test configuration validation during generation."""
        # Invalid configuration
        invalid_config = BackendConfig(
            project_name="",  # Invalid: empty name
            framework=BackendFramework.FASTAPI
        )
        
        backend_generator = BackendGenerator()
        
        with pytest.raises(ValueError, match="project_name"):
            await backend_generator.generate_backend(
                config=invalid_config,
                architecture={},
                output_path=Path("/tmp")
            )
    
    @pytest.mark.asyncio 
    async def test_framework_specific_generation(self):
        """Test that framework-specific features are generated correctly."""
        framework_configs = [
            (BackendFramework.FASTAPI, ["swagger", "async", "pydantic"]),
            (BackendFramework.DJANGO, ["admin", "orm", "migrations"]),
            (BackendFramework.NESTJS, ["decorators", "guards", "modules"])
        ]
        
        for framework, expected_features in framework_configs:
            config = BackendConfig(
                project_name=f"test-{framework.value}",
                framework=framework
            )
            
            with patch('mcpturbo.protocol.send_request') as mock_protocol:
                mock_protocol.return_value = AsyncMock()
                mock_protocol.return_value.result = f"Generated {framework.value} code"
                
                backend_generator = BackendGenerator()
                
                result = await backend_generator.generate_backend(
                    config=config,
                    architecture={"entities": []},
                    output_path=Path(f"/tmp/{framework.value}")
                )
                
                assert result["framework"] == framework.value
