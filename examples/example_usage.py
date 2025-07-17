"""
Basic usage example for Genesis Backend.

This example demonstrates how to use Genesis Backend agents
to generate a complete backend application.
"""

import asyncio
from pathlib import Path

from genesis_backend import (
    BackendConfig,
    BackendFramework,
    DatabaseType,
    AuthMethod,
    DatabaseConfig,
    AuthConfig,
    ORMType,
    get_agents
)
from genesis_backend.agents import ArchitectAgent, FastAPIAgent, DatabaseAgent, AuthAgent
from genesis_backend.generators import BackendGenerator


async def main():
    """
    Example of generating a complete FastAPI backend application.
    """
    print("🚀 Genesis Backend - Basic Usage Example")
    print("=" * 50)
    
    # Step 1: Create backend configuration
    print("\n📋 Step 1: Creating backend configuration...")
    
    config = BackendConfig(
        project_name="ecommerce-api",
        description="E-commerce API with user management and product catalog",
        framework=BackendFramework.FASTAPI,
        version="1.0.0",
        debug=True,
        features=[
            "api",
            "authentication", 
            "database",
            "documentation",
            "cors",
            "logging"
        ],
        api_version="v1",
        cors_origins=["http://localhost:3000", "http://localhost:8080"],
        database=DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            host="localhost",
            port=5432,
            name="ecommerce_db",
            user="api_user",
            password="secure_password",
            orm=ORMType.SQLALCHEMY
        ),
        auth=AuthConfig(
            method=AuthMethod.JWT,
            secret_key="your-super-secret-jwt-key-change-in-production",
            algorithm="HS256",
            access_token_expire_minutes=30,
            refresh_token_expire_days=7
        )
    )
    
    print(f"   ✅ Project: {config.project_name}")
    print(f"   ✅ Framework: {config.framework.value}")
    print(f"   ✅ Database: {config.database.type.value}")
    print(f"   ✅ Auth: {config.auth.method.value}")
    print(f"   ✅ Features: {', '.join(config.features)}")
    
    # Step 2: Initialize agents
    print("\n🤖 Step 2: Initializing Genesis Backend agents...")
    
    architect = ArchitectAgent()
    fastapi_agent = FastAPIAgent()
    database_agent = DatabaseAgent()
    auth_agent = AuthAgent()
    
    print(f"   ✅ {architect.name}")
    print(f"   ✅ {fastapi_agent.name}")
    print(f"   ✅ {database_agent.name}")
    print(f"   ✅ {auth_agent.name}")
    
    # Step 3: Architecture analysis
    print("\n🏗️ Step 3: Analyzing requirements and designing architecture...")
    
    # This would normally use LLMs - for the example we'll simulate the process
    architecture = {
        "entities": [
            {
                "name": "User",
                "attributes": [
                    "id", "email", "password_hash", "first_name", 
                    "last_name", "is_active", "created_at", "updated_at"
                ]
            },
            {
                "name": "Product",
                "attributes": [
                    "id", "name", "description", "price", "stock",
                    "category", "is_active", "created_at", "updated_at"
                ]
            },
            {
                "name": "Order",
                "attributes": [
                    "id", "user_id", "total_amount", "status",
                    "order_date", "updated_at"
                ]
            }
        ],
        "relationships": [
            {"from": "Order", "to": "User", "type": "many_to_one"}
        ],
        "api_design": {
            "version": "v1",
            "base_path": "/api/v1",
            "endpoints": [
                {"path": "/auth/login", "methods": ["POST"]},
                {"path": "/auth/register", "methods": ["POST"]},
                {"path": "/users", "methods": ["GET", "POST"]},
                {"path": "/users/{id}", "methods": ["GET", "PUT", "DELETE"]},
                {"path": "/products", "methods": ["GET", "POST"]},
                {"path": "/products/{id}", "methods": ["GET", "PUT", "DELETE"]},
                {"path": "/orders", "methods": ["GET", "POST"]},
                {"path": "/orders/{id}", "methods": ["GET", "PUT", "DELETE"]}
            ]
        }
    }
    
    print(f"   ✅ Entities: {len(architecture['entities'])} defined")
    print(f"   ✅ API Endpoints: {len(architecture['api_design']['endpoints'])} designed")
    print(f"   ✅ Relationships: {len(architecture['relationships'])} mapped")
    
    # Step 4: Generate backend using BackendGenerator
    print("\n⚙️ Step 4: Generating complete backend application...")
    
    output_path = Path("./generated_backend")
    backend_generator = BackendGenerator()
    
    # For demonstration, we'll show what would be generated
    # In a real scenario, this would call LLMs and generate actual code
    print("   🔄 Generating FastAPI application structure...")
    print("   🔄 Creating API routes and endpoints...")
    print("   🔄 Generating SQLAlchemy models...")
    print("   🔄 Setting up JWT authentication...")
    print("   🔄 Creating database migrations...")
    print("   🔄 Generating Docker configuration...")
    print("   🔄 Creating tests and documentation...")
    
    # Simulate the generation result
    generation_result = {
        "files": {
            "app/main.py": "# FastAPI application entry point",
            "app/core/config.py": "# Application configuration",
            "app/core/security.py": "# Security utilities",
            "app/api/v1/endpoints/auth.py": "# Authentication endpoints",
            "app/api/v1/endpoints/users.py": "# User management endpoints", 
            "app/api/v1/endpoints/products.py": "# Product management endpoints",
            "app/api/v1/endpoints/orders.py": "# Order management endpoints",
            "app/models/user.py": "# User SQLAlchemy model",
            "app/models/product.py": "# Product SQLAlchemy model",
            "app/models/order.py": "# Order SQLAlchemy model",
            "app/schemas/user.py": "# User Pydantic schemas",
            "app/schemas/product.py": "# Product Pydantic schemas",
            "app/schemas/order.py": "# Order Pydantic schemas",
            "alembic/versions/001_initial.py": "# Initial database migration",
            "requirements.txt": "# Python dependencies",
            "Dockerfile": "# Docker configuration",
            "docker-compose.yml": "# Docker Compose setup",
            "tests/test_api.py": "# API endpoint tests",
            "tests/test_models.py": "# Model tests",
            "README.md": "# Project documentation"
        },
        "framework": "fastapi",
        "total_files": 20
    }
    
    print(f"   ✅ Generated {generation_result['total_files']} files")
    print(f"   ✅ Framework: {generation_result['framework']}")
    
    # Step 5: Display generated file structure
    print("\n📁 Step 5: Generated file structure:")
    print("   ecommerce-api/")
    
    for file_path in sorted(generation_result["files"].keys()):
        depth = file_path.count("/")
        indent = "   " + "  " * depth
        file_name = file_path.split("/")[-1]
        print(f"{indent}├── {file_name}")
    
    # Step 6: Next steps
    print("\n🎯 Step 6: Next steps for your generated backend:")
    print("   1. Review and customize the generated configuration")
    print("   2. Set up your PostgreSQL database")
    print("   3. Update environment variables in .env file")
    print("   4. Install dependencies: pip install -r requirements.txt")
    print("   5. Run database migrations: alembic upgrade head")
    print("   6. Start the development server: uvicorn app.main:app --reload")
    print("   7. Visit http://localhost:8000/docs for API documentation")
    
    print("\n✨ Backend generation completed successfully!")
    return generation_result


async def demonstrate_agent_capabilities():
    """
    Demonstrate individual agent capabilities.
    """
    print("\n" + "=" * 50)
    print("🔍 Demonstrating Individual Agent Capabilities")
    print("=" * 50)
    
    # Get all available agents
    agent_classes = get_agents()
    print(f"\n📊 Available agents: {len(agent_classes)}")
    
    for agent_class in agent_classes:
        agent = agent_class()
        print(f"\n🤖 {agent.name}")
        print(f"   ID: {agent.agent_id}")
        print(f"   Type: {agent.agent_type}")
        print(f"   Capabilities: {len(agent.capabilities)}")
        
        for capability in agent.capabilities[:3]:  # Show first 3 capabilities
            print(f"     • {capability}")
        
        if len(agent.capabilities) > 3:
            print(f"     • ... and {len(agent.capabilities) - 3} more")


async def show_configuration_examples():
    """
    Show different configuration examples for various scenarios.
    """
    print("\n" + "=" * 50)
    print("⚙️ Configuration Examples")
    print("=" * 50)
    
    # FastAPI with PostgreSQL and JWT
    print("\n1. FastAPI + PostgreSQL + JWT Authentication:")
    fastapi_config = BackendConfig(
        project_name="fastapi-enterprise-api",
        framework=BackendFramework.FASTAPI,
        database=DatabaseConfig(type=DatabaseType.POSTGRESQL, orm=ORMType.SQLALCHEMY),
        auth=AuthConfig(method=AuthMethod.JWT),
        features=["api", "authentication", "database", "swagger", "cors"]
    )
    print(f"   Project: {fastapi_config.project_name}")
    print(f"   Stack: {fastapi_config.framework.value} + {fastapi_config.database.type.value} + {fastapi_config.auth.method.value}")
    
    # Django with MySQL and Session Auth
    print("\n2. Django + MySQL + Session Authentication:")
    django_config = BackendConfig(
        project_name="django-web-app",
        framework=BackendFramework.DJANGO,
        database=DatabaseConfig(type=DatabaseType.MYSQL, orm=ORMType.DJANGO_ORM),
        auth=AuthConfig(method=AuthMethod.SESSION),
        features=["admin", "rest_api", "authentication", "database"]
    )
    print(f"   Project: {django_config.project_name}")
    print(f"   Stack: {django_config.framework.value} + {django_config.database.type.value} + {django_config.auth.method.value}")
    
    # NestJS with PostgreSQL and JWT
    print("\n3. NestJS + PostgreSQL + JWT Authentication:")
    nestjs_config = BackendConfig(
        project_name="nestjs-microservice",
        framework=BackendFramework.NESTJS,
        database=DatabaseConfig(type=DatabaseType.POSTGRESQL, orm=ORMType.TYPEORM),
        auth=AuthConfig(method=AuthMethod.JWT),
        features=["api", "authentication", "typeorm", "swagger", "guards"]
    )
    print(f"   Project: {nestjs_config.project_name}")
    print(f"   Stack: {nestjs_config.framework.value} + {nestjs_config.database.type.value} + {nestjs_config.auth.method.value}")
    
    # MongoDB with Mongoose
    print("\n4. Express + MongoDB + OAuth2:")
    mongo_config = BackendConfig(
        project_name="express-social-api",
        framework=BackendFramework.EXPRESS,
        database=DatabaseConfig(type=DatabaseType.MONGODB, orm=ORMType.MONGOOSE),
        auth=AuthConfig(method=AuthMethod.OAUTH2, oauth_providers=["google", "github"]),
        features=["api", "social_auth", "database"]
    )
    print(f"   Project: {mongo_config.project_name}")
    print(f"   Stack: {mongo_config.framework.value} + {mongo_config.database.type.value} + {mongo_config.auth.method.value}")


if __name__ == "__main__":
    """
    Run the basic usage example.
    """
    print("Starting Genesis Backend basic usage example...")
    
    # Run the main example
    result = asyncio.run(main())
    
    # Show additional examples
    asyncio.run(demonstrate_agent_capabilities())
    asyncio.run(show_configuration_examples())
    
    print("\n" + "=" * 50)
    print("🎉 Example completed successfully!")
    print("Visit https://docs.genesis-engine.dev/backend for more examples")
    print("=" * 50)
