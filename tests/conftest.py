"""
Test configuration and fixtures for Genesis Backend tests.
"""

import pytest
import asyncio
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock

from genesis_backend.config import (
    BackendConfig,
    BackendFramework,
    DatabaseType,
    AuthMethod,
    DatabaseConfig,
    AuthConfig,
    ORMType
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_backend_config():
    """Create a sample backend configuration for testing."""
    return BackendConfig(
        project_name="test-api",
        description="Test API project for Genesis Backend",
        framework=BackendFramework.FASTAPI,
        version="1.0.0",
        debug=True,
        features=["api", "authentication", "database", "documentation"],
        api_version="v1",
        cors_origins=["http://localhost:3000"],
        database=DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            host="localhost",
            port=5432,
            name="test_db",
            user="test_user",
            password="test_password",
            orm=ORMType.SQLALCHEMY
        ),
        auth=AuthConfig(
            method=AuthMethod.JWT,
            secret_key="test-secret-key-for-jwt",
            algorithm="HS256",
            access_token_expire_minutes=30,
            refresh_token_expire_days=7
        )
    )


@pytest.fixture
def fastapi_config():
    """Create FastAPI-specific configuration."""
    return BackendConfig(
        project_name="fastapi-test-app",
        description="FastAPI test application",
        framework=BackendFramework.FASTAPI,
        features=["api", "authentication", "database", "swagger"],
        database=DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            orm=ORMType.SQLALCHEMY
        ),
        auth=AuthConfig(
            method=AuthMethod.JWT,
            secret_key="fastapi-test-secret"
        )
    )


@pytest.fixture
def django_config():
    """Create Django-specific configuration."""
    return BackendConfig(
        project_name="django-test-app",
        description="Django test application",
        framework=BackendFramework.DJANGO,
        features=["admin", "rest_api", "authentication", "database"],
        database=DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            orm=ORMType.DJANGO_ORM
        ),
        auth=AuthConfig(
            method=AuthMethod.SESSION,
            session_timeout=1800,
            cookie_secure=True,
            cookie_httponly=True
        )
    )


@pytest.fixture
def nestjs_config():
    """Create NestJS-specific configuration."""
    return BackendConfig(
        project_name="nestjs-test-app",
        description="NestJS test application",
        framework=BackendFramework.NESTJS,
        features=["api", "authentication", "typeorm", "swagger"],
        database=DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            orm=ORMType.TYPEORM
        ),
        auth=AuthConfig(
            method=AuthMethod.JWT,
            secret_key="nestjs-test-secret",
            algorithm="HS256"
        )
    )


@pytest.fixture
def sample_data_models():
    """Create sample data models for testing."""
    return [
        {
            "name": "User",
            "fields": [
                {"name": "id", "type": "UUID", "primary_key": True},
                {"name": "email", "type": "String", "unique": True, "required": True},
                {"name": "password_hash", "type": "String", "required": True},
                {"name": "first_name", "type": "String"},
                {"name": "last_name", "type": "String"},
                {"name": "is_active", "type": "Boolean", "default": True},
                {"name": "created_at", "type": "DateTime", "auto_now_add": True},
                {"name": "updated_at", "type": "DateTime", "auto_now": True}
            ]
        },
        {
            "name": "Product",
            "fields": [
                {"name": "id", "type": "UUID", "primary_key": True},
                {"name": "name", "type": "String", "required": True},
                {"name": "description", "type": "Text"},
                {"name": "price", "type": "Decimal", "required": True},
                {"name": "stock", "type": "Integer", "default": 0},
                {"name": "category", "type": "String"},
                {"name": "is_active", "type": "Boolean", "default": True},
                {"name": "created_at", "type": "DateTime", "auto_now_add": True},
                {"name": "updated_at", "type": "DateTime", "auto_now": True}
            ]
        },
        {
            "name": "Order",
            "fields": [
                {"name": "id", "type": "UUID", "primary_key": True},
                {"name": "user_id", "type": "UUID", "foreign_key": "User.id"},
                {"name": "total_amount", "type": "Decimal", "required": True},
                {"name": "status", "type": "String", "choices": ["pending", "completed", "cancelled"]},
                {"name": "order_date", "type": "DateTime", "auto_now_add": True},
                {"name": "updated_at", "type": "DateTime", "auto_now": True}
            ]
        }
    ]


@pytest.fixture
def sample_api_design():
    """Create sample API design for testing."""
    return {
        "version": "v1",
        "base_path": "/api/v1",
        "endpoints": [
            {
                "path": "/users",
                "methods": ["GET", "POST"],
                "description": "User management endpoints",
                "authentication_required": True
            },
            {
                "path": "/users/{id}",
                "methods": ["GET", "PUT", "DELETE"],
                "description": "Individual user operations",
                "authentication_required": True
            },
            {
                "path": "/products",
                "methods": ["GET", "POST"],
                "description": "Product management endpoints",
                "authentication_required": False
            },
            {
                "path": "/products/{id}",
                "methods": ["GET", "PUT", "DELETE"],
                "description": "Individual product operations",
                "authentication_required": True
            },
            {
                "path": "/orders",
                "methods": ["GET", "POST"],
                "description": "Order management endpoints",
                "authentication_required": True
            },
            {
                "path": "/auth/login",
                "methods": ["POST"],
                "description": "User authentication",
                "authentication_required": False
            },
            {
                "path": "/auth/logout",
                "methods": ["POST"],
                "description": "User logout",
                "authentication_required": True
            }
        ],
        "authentication": {
            "type": "JWT",
            "header": "Authorization",
            "prefix": "Bearer"
        },
        "error_handling": {
            "format": "JSON",
            "include_stack_trace": False
        }
    }


@pytest.fixture
def sample_database_schema():
    """Create sample database schema for testing."""
    return {
        "database_type": "postgresql",
        "tables": [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "UUID", "constraints": ["PRIMARY KEY"]},
                    {"name": "email", "type": "VARCHAR(255)", "constraints": ["UNIQUE", "NOT NULL"]},
                    {"name": "password_hash", "type": "VARCHAR(255)", "constraints": ["NOT NULL"]},
                    {"name": "first_name", "type": "VARCHAR(100)"},
                    {"name": "last_name", "type": "VARCHAR(100)"},
                    {"name": "is_active", "type": "BOOLEAN", "constraints": ["DEFAULT TRUE"]},
                    {"name": "created_at", "type": "TIMESTAMP", "constraints": ["DEFAULT CURRENT_TIMESTAMP"]},
                    {"name": "updated_at", "type": "TIMESTAMP", "constraints": ["DEFAULT CURRENT_TIMESTAMP"]}
                ]
            },
            {
                "name": "products",
                "columns": [
                    {"name": "id", "type": "UUID", "constraints": ["PRIMARY KEY"]},
                    {"name": "name", "type": "VARCHAR(255)", "constraints": ["NOT NULL"]},
                    {"name": "description", "type": "TEXT"},
                    {"name": "price", "type": "DECIMAL(10,2)", "constraints": ["NOT NULL"]},
                    {"name": "stock", "type": "INTEGER", "constraints": ["DEFAULT 0"]},
                    {"name": "category", "type": "VARCHAR(100)"},
                    {"name": "is_active", "type": "BOOLEAN", "constraints": ["DEFAULT TRUE"]},
                    {"name": "created_at", "type": "TIMESTAMP", "constraints": ["DEFAULT CURRENT_TIMESTAMP"]},
                    {"name": "updated_at", "type": "TIMESTAMP", "constraints": ["DEFAULT CURRENT_TIMESTAMP"]}
                ]
            },
            {
                "name": "orders",
                "columns": [
                    {"name": "id", "type": "UUID", "constraints": ["PRIMARY KEY"]},
                    {"name": "user_id", "type": "UUID", "constraints": ["NOT NULL"]},
                    {"name": "total_amount", "type": "DECIMAL(10,2)", "constraints": ["NOT NULL"]},
                    {"name": "status", "type": "VARCHAR(50)", "constraints": ["DEFAULT 'pending'"]},
                    {"name": "order_date", "type": "TIMESTAMP", "constraints": ["DEFAULT CURRENT_TIMESTAMP"]},
                    {"name": "updated_at", "type": "TIMESTAMP", "constraints": ["DEFAULT CURRENT_TIMESTAMP"]}
                ]
            }
        ],
        "foreign_keys": [
            {
                "table": "orders",
                "column": "user_id",
                "references": "users(id)",
                "on_delete": "CASCADE"
            }
        ],
        "indexes": [
            {"name": "idx_users_email", "table": "users", "columns": ["email"], "unique": True},
            {"name": "idx_products_name", "table": "products", "columns": ["name"]},
            {"name": "idx_orders_user_id", "table": "orders", "columns": ["user_id"]},
            {"name": "idx_orders_status", "table": "orders", "columns": ["status"]}
        ]
    }


@pytest.fixture
def mock_llm_response():
    """Create mock LLM response for testing."""
    def _create_mock_response(content: str = "Mock LLM response", success: bool = True):
        mock = AsyncMock()
        mock.result = content
        mock.success = success
        return mock
    
    return _create_mock_response


@pytest.fixture
def mock_mcpturbo_protocol(mock_llm_response):
    """Create mock MCPturbo protocol for testing."""
    async def mock_send_request(sender_id: str, target_id: str, action: str, data: Dict[str, Any]):
        # Simulate different responses based on action
        if action == "code_generation":
            return mock_llm_response("Generated code content")
        elif action == "reasoning":
            return mock_llm_response("Reasoning and analysis result")
        elif action == "fast_coding":
            return mock_llm_response("Fast coding result")
        else:
            return mock_llm_response("Generic LLM response")
    
    return mock_send_request


@pytest.fixture(autouse=True)
def clean_temp_files():
    """Clean up temporary files after each test."""
    yield
    # Cleanup logic can be added here if needed
    pass


class MockTemplateEngine:
    """Mock template engine for testing."""
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        return f"Rendered template: {template_name} with context: {context}"
    
    def get_template(self, template_name: str):
        return f"Template: {template_name}"


@pytest.fixture
def mock_template_engine():
    """Create mock template engine for testing."""
    return MockTemplateEngine()


# Async helper functions for tests
async def async_test_helper(coro):
    """Helper function for async tests."""
    return await coro


# Test data constants
TEST_PROJECT_NAME = "genesis-backend-test"
TEST_API_VERSION = "v1"
TEST_SECRET_KEY = "test-secret-key-for-testing-only"

# Test configuration variations
@pytest.fixture(params=[
    BackendFramework.FASTAPI,
    BackendFramework.DJANGO,
    BackendFramework.NESTJS
])
def all_frameworks(request):
    """Parametrized fixture for testing all supported frameworks."""
    return request.param


@pytest.fixture(params=[
    DatabaseType.POSTGRESQL,
    DatabaseType.MYSQL,
    DatabaseType.SQLITE,
    DatabaseType.MONGODB
])
def all_databases(request):
    """Parametrized fixture for testing all supported databases."""
    return request.param


@pytest.fixture(params=[
    AuthMethod.JWT,
    AuthMethod.OAUTH2,
    AuthMethod.SESSION
])
def all_auth_methods(request):
    """Parametrized fixture for testing all supported auth methods."""
    return request.param


# Performance testing helpers
@pytest.fixture
def performance_monitor():
    """Monitor performance during tests."""
    import time
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def duration(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return PerformanceMonitor()


# Custom pytest marks
pytest.mark.integration = pytest.mark.slow
pytest.mark.unit = pytest.mark.fast
pytest.mark.agent = pytest.mark.slow
pytest.mark.generator = pytest.mark.slow
