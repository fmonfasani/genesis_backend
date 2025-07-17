"""
Tests for backend configuration.
"""

import pytest
from genesis_backend.config import (
    BackendConfig,
    BackendFramework,
    DatabaseType,
    AuthMethod,
    DatabaseConfig,
    AuthConfig,
    ORMType
)


class TestBackendConfig:
    """Test BackendConfig class."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = BackendConfig(
            project_name="test-api",
            description="Test API project"
        )
        
        assert config.project_name == "test-api"
        assert config.description == "Test API project"
        assert config.framework == BackendFramework.FASTAPI
        assert config.version == "0.1.0"
        assert config.debug is False
        assert isinstance(config.features, list)
    
    def test_fastapi_config(self):
        """Test FastAPI configuration."""
        config = BackendConfig(
            project_name="fastapi-app",
            framework=BackendFramework.FASTAPI,
            features=["api", "authentication", "database"]
        )
        
        assert config.framework == BackendFramework.FASTAPI
        assert config.language == "python"
        assert "api" in config.features
        assert "authentication" in config.features
        assert "database" in config.features
    
    def test_django_config(self):
        """Test Django configuration."""
        config = BackendConfig(
            project_name="django-app",
            framework=BackendFramework.DJANGO,
            features=["admin", "rest_api", "authentication"]
        )
        
        assert config.framework == BackendFramework.DJANGO
        assert config.language == "python"
        assert "admin" in config.features
    
    def test_nestjs_config(self):
        """Test NestJS configuration."""
        config = BackendConfig(
            project_name="nestjs-app",
            framework=BackendFramework.NESTJS,
            features=["api", "authentication", "typeorm"]
        )
        
        assert config.framework == BackendFramework.NESTJS
        assert config.language == "typescript"
        assert "typeorm" in config.features
    
    def test_config_serialization(self):
        """Test configuration serialization to dict."""
        config = BackendConfig(
            project_name="test-app",
            description="Test application",
            framework=BackendFramework.FASTAPI,
            version="1.0.0"
        )
        
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert config_dict["project_name"] == "test-app"
        assert config_dict["framework"] == "fastapi"
        assert config_dict["version"] == "1.0.0"
    
    def test_config_deserialization(self):
        """Test configuration deserialization from dict."""
        config_data = {
            "project_name": "deserialized-app",
            "description": "Deserialized application",
            "framework": "django",
            "version": "2.0.0",
            "debug": True,
            "features": ["admin", "api"]
        }
        
        config = BackendConfig.from_dict(config_data)
        
        assert config.project_name == "deserialized-app"
        assert config.framework == BackendFramework.DJANGO
        assert config.version == "2.0.0"
        assert config.debug is True
        assert "admin" in config.features


class TestDatabaseConfig:
    """Test DatabaseConfig class."""
    
    def test_postgresql_config(self):
        """Test PostgreSQL configuration."""
        db_config = DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            host="localhost",
            port=5432,
            name="test_db",
            user="test_user",
            password="test_pass"
        )
        
        assert db_config.type == DatabaseType.POSTGRESQL
        assert db_config.host == "localhost"
        assert db_config.port == 5432
        assert db_config.name == "test_db"
        assert db_config.user == "test_user"
        assert db_config.password == "test_pass"
    
    def test_mysql_config(self):
        """Test MySQL configuration."""
        db_config = DatabaseConfig(
            type=DatabaseType.MYSQL,
            host="localhost",
            port=3306,
            name="mysql_db"
        )
        
        assert db_config.type == DatabaseType.MYSQL
        assert db_config.port == 3306
    
    def test_sqlite_config(self):
        """Test SQLite configuration."""
        db_config = DatabaseConfig(
            type=DatabaseType.SQLITE,
            name="test.db"
        )
        
        assert db_config.type == DatabaseType.SQLITE
        assert db_config.name == "test.db"
        # SQLite doesn't need host/port
        assert db_config.host is None
        assert db_config.port is None
    
    def test_mongodb_config(self):
        """Test MongoDB configuration."""
        db_config = DatabaseConfig(
            type=DatabaseType.MONGODB,
            host="localhost",
            port=27017,
            name="mongo_db",
            orm=ORMType.MONGOOSE
        )
        
        assert db_config.type == DatabaseType.MONGODB
        assert db_config.port == 27017
        assert db_config.orm == ORMType.MONGOOSE
    
    def test_connection_url_postgresql(self):
        """Test PostgreSQL connection URL generation."""
        db_config = DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            host="localhost",
            port=5432,
            name="test_db",
            user="test_user",
            password="test_pass"
        )
        
        expected_url = "postgresql://test_user:test_pass@localhost:5432/test_db"
        assert db_config.connection_url == expected_url
    
    def test_connection_url_sqlite(self):
        """Test SQLite connection URL generation."""
        db_config = DatabaseConfig(
            type=DatabaseType.SQLITE,
            name="test.db"
        )
        
        expected_url = "sqlite:///test.db"
        assert db_config.connection_url == expected_url
    
    def test_orm_selection(self):
        """Test ORM selection based on database type."""
        # PostgreSQL with SQLAlchemy
        pg_config = DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            orm=ORMType.SQLALCHEMY
        )
        assert pg_config.orm == ORMType.SQLALCHEMY
        
        # MongoDB with Mongoose
        mongo_config = DatabaseConfig(
            type=DatabaseType.MONGODB,
            orm=ORMType.MONGOOSE
        )
        assert mongo_config.orm == ORMType.MONGOOSE


class TestAuthConfig:
    """Test AuthConfig class."""
    
    def test_jwt_config(self):
        """Test JWT authentication configuration."""
        auth_config = AuthConfig(
            method=AuthMethod.JWT,
            secret_key="test-secret-key",
            algorithm="HS256",
            access_token_expire_minutes=30
        )
        
        assert auth_config.method == AuthMethod.JWT
        assert auth_config.secret_key == "test-secret-key"
        assert auth_config.algorithm == "HS256"
        assert auth_config.access_token_expire_minutes == 30
    
    def test_oauth2_config(self):
        """Test OAuth2 authentication configuration."""
        auth_config = AuthConfig(
            method=AuthMethod.OAUTH2,
            oauth_providers=["google", "github", "facebook"]
        )
        
        assert auth_config.method == AuthMethod.OAUTH2
        assert "google" in auth_config.oauth_providers
        assert "github" in auth_config.oauth_providers
        assert "facebook" in auth_config.oauth_providers
    
    def test_session_config(self):
        """Test session authentication configuration."""
        auth_config = AuthConfig(
            method=AuthMethod.SESSION,
            session_timeout=1800,
            cookie_secure=True,
            cookie_httponly=True
        )
        
        assert auth_config.method == AuthMethod.SESSION
        assert auth_config.session_timeout == 1800
        assert auth_config.cookie_secure is True
        assert auth_config.cookie_httponly is True
    
    def test_default_jwt_config(self):
        """Test default JWT configuration values."""
        auth_config = AuthConfig(
            method=AuthMethod.JWT,
            secret_key="test-key"
        )
        
        # Check default values
        assert auth_config.algorithm == "HS256"
        assert auth_config.access_token_expire_minutes == 30
        assert auth_config.refresh_token_expire_days == 7


class TestEnumValues:
    """Test enum value validations."""
    
    def test_backend_framework_values(self):
        """Test BackendFramework enum values."""
        assert BackendFramework.FASTAPI.value == "fastapi"
        assert BackendFramework.DJANGO.value == "django"
        assert BackendFramework.NESTJS.value == "nestjs"
        assert BackendFramework.EXPRESS.value == "express"
    
    def test_database_type_values(self):
        """Test DatabaseType enum values."""
        assert DatabaseType.POSTGRESQL.value == "postgresql"
        assert DatabaseType.MYSQL.value == "mysql"
        assert DatabaseType.SQLITE.value == "sqlite"
        assert DatabaseType.MONGODB.value == "mongodb"
        assert DatabaseType.REDIS.value == "redis"
    
    def test_auth_method_values(self):
        """Test AuthMethod enum values."""
        assert AuthMethod.JWT.value == "jwt"
        assert AuthMethod.OAUTH2.value == "oauth2"
        assert AuthMethod.SESSION.value == "session"
        assert AuthMethod.SOCIAL.value == "social"
    
    def test_orm_type_values(self):
        """Test ORMType enum values."""
        assert ORMType.SQLALCHEMY.value == "sqlalchemy"
        assert ORMType.DJANGO_ORM.value == "django_orm"
        assert ORMType.TYPEORM.value == "typeorm"
        assert ORMType.PRISMA.value == "prisma"
        assert ORMType.MONGOOSE.value == "mongoose"


class TestConfigValidation:
    """Test configuration validation."""
    
    def test_invalid_project_name(self):
        """Test validation of invalid project name."""
        with pytest.raises(ValueError):
            BackendConfig(project_name="")  # Empty name
    
    def test_invalid_framework_combination(self):
        """Test validation of invalid framework combinations."""
        # This should be fine - no validation error expected here
        # but we can add validation in the future
        config = BackendConfig(
            project_name="test",
            framework=BackendFramework.NESTJS,
            database=DatabaseConfig(
                type=DatabaseType.POSTGRESQL,
                orm=ORMType.DJANGO_ORM  # Wrong ORM for NestJS
            )
        )
        
        # For now, this should work but could be validated in the future
        assert config.framework == BackendFramework.NESTJS
    
    def test_required_fields(self):
        """Test that required fields are enforced."""
        # project_name is required
        with pytest.raises(TypeError):
            BackendConfig()  # Missing required project_name
        
        # But description is optional
        config = BackendConfig(project_name="test")
        assert config.project_name == "test"
        assert config.description == ""


class TestIntegrationConfig:
    """Test configuration integration scenarios."""
    
    def test_complete_fastapi_config(self):
        """Test complete FastAPI configuration."""
        config = BackendConfig(
            project_name="complete-fastapi-app",
            description="Complete FastAPI application",
            framework=BackendFramework.FASTAPI,
            version="1.0.0",
            debug=False,
            features=["api", "authentication", "database", "caching"],
            database=DatabaseConfig(
                type=DatabaseType.POSTGRESQL,
                host="localhost",
                port=5432,
                name="fastapi_db",
                user="api_user",
                password="secure_password",
                orm=ORMType.SQLALCHEMY
            ),
            auth=AuthConfig(
                method=AuthMethod.JWT,
                secret_key="super-secret-jwt-key",
                algorithm="HS256",
                access_token_expire_minutes=60,
                refresh_token_expire_days=30
            )
        )
        
        # Validate complete configuration
        assert config.project_name == "complete-fastapi-app"
        assert config.framework == BackendFramework.FASTAPI
        assert config.database.type == DatabaseType.POSTGRESQL
        assert config.database.orm == ORMType.SQLALCHEMY
        assert config.auth.method == AuthMethod.JWT
        assert config.auth.access_token_expire_minutes == 60
        
        # Test serialization
        config_dict = config.to_dict()
        assert config_dict["project_name"] == "complete-fastapi-app"
        assert config_dict["database"]["type"] == "postgresql"
        assert config_dict["auth"]["method"] == "jwt"
        
        # Test deserialization
        recreated_config = BackendConfig.from_dict(config_dict)
        assert recreated_config.project_name == config.project_name
        assert recreated_config.framework == config.framework
        assert recreated_config.database.type == config.database.type
        assert recreated_config.auth.method == config.auth.method
    
    def test_complete_nestjs_config(self):
        """Test complete NestJS configuration."""
        config = BackendConfig(
            project_name="enterprise-nestjs-api",
            description="Enterprise NestJS API with TypeORM",
            framework=BackendFramework.NESTJS,
            features=["api", "authentication", "authorization", "typeorm", "swagger"],
            database=DatabaseConfig(
                type=DatabaseType.POSTGRESQL,
                host="db.example.com",
                port=5432,
                name="enterprise_db",
                user="api_service",
                password="enterprise_password",
                orm=ORMType.TYPEORM
            ),
            auth=AuthConfig(
                method=AuthMethod.JWT,
                secret_key="enterprise-jwt-secret",
                algorithm="RS256",  # More secure for enterprise
                access_token_expire_minutes=15,  # Shorter for security
                refresh_token_expire_days=7
            )
        )
        
        assert config.language == "typescript"  # NestJS uses TypeScript
        assert config.database.orm == ORMType.TYPEORM
        assert config.auth.algorithm == "RS256"
        assert "swagger" in config.features
