"""
Authentication Generator

Specialized generator for creating authentication systems using LLMs.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from mcpturbo import protocol
from genesis_templates import TemplateEngine

from ..config import BackendConfig, BackendFramework, AuthMethod

logger = logging.getLogger(__name__)


class AuthGenerator:
    """
    Generator specialized in authentication system creation.
    
    Responsibilities:
    - Generate authentication logic for different frameworks
    - Create authorization middleware and guards
    - Generate user management systems
    - Create JWT, OAuth2, and session authentication
    - Generate password security systems
    """
    
    def __init__(self, template_engine: Optional[TemplateEngine] = None):
        self.template_engine = template_engine or TemplateEngine()
        
        # Framework-specific auth generators
        self.framework_generators = {
            BackendFramework.FASTAPI: self._generate_fastapi_auth,
            BackendFramework.DJANGO: self._generate_django_auth,
            BackendFramework.NESTJS: self._generate_nestjs_auth,
        }
        
        # Auth method generators
        self.auth_method_generators = {
            AuthMethod.JWT: self._generate_jwt_system,
            AuthMethod.OAUTH2: self._generate_oauth2_system,
            AuthMethod.SESSION: self._generate_session_system,
        }
    
    async def generate_authentication(
        self,
        config: BackendConfig
    ) -> Dict[str, str]:
        """
        Generate authentication system for specified framework.
        
        Args:
            config: Backend configuration with auth settings
            
        Returns:
            Dictionary of generated authentication files
        """
        logger.info(f"🔐 Generating authentication for {config.framework.value} with {config.auth.method.value}")
        
        if config.framework not in self.framework_generators:
            raise ValueError(f"Framework {config.framework.value} not supported for auth generation")
        
        generator = self.framework_generators[config.framework]
        return await generator(config)
    
    async def generate_fastapi_auth(self, config: BackendConfig) -> Dict[str, str]:
        """Generate FastAPI authentication system."""
        return await self._generate_fastapi_auth(config)
    
    async def generate_django_auth(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django authentication system."""
        return await self._generate_django_auth(config)
    
    async def generate_nestjs_auth(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS authentication system."""
        return await self._generate_nestjs_auth(config)
    
    async def _generate_fastapi_auth(self, config: BackendConfig) -> Dict[str, str]:
        """Generate FastAPI authentication implementation using LLM."""
        
        fastapi_auth_prompt = f"""
        Generate FastAPI authentication system:
        
        Auth Method: {config.auth.method.value}
        Secret Key: {config.auth.secret_key}
        Algorithm: {config.auth.algorithm}
        Token Expiry: {config.auth.access_token_expire_minutes} minutes
        
        Generate comprehensive FastAPI authentication including:
        1. JWT token creation and validation utilities
        2. Password hashing with bcrypt
        3. Authentication dependencies for route protection
        4. Login and registration endpoints
        5. Token refresh mechanism
        6. User authentication middleware
        7. Permission-based decorators
        8. OAuth2 password bearer implementation
        9. Security utilities and helpers
        10. Error handling for authentication failures
        
        Files to generate:
        - app/core/security.py - Security utilities
        - app/core/auth.py - Authentication logic
        - app/api/auth.py - Authentication endpoints
        - app/dependencies/auth.py - Authentication dependencies
        
        Return production-ready FastAPI authentication code.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="openai",
            action="code_generation",
            data={
                "prompt": fastapi_auth_prompt,
                "language": "python",
                "framework": "fastapi"
            }
        )
        
        auth_files = self._parse_fastapi_auth_files(response.result)
        
        # Generate additional auth files
        if config.auth.method == AuthMethod.JWT:
            auth_files.update(await self._generate_jwt_utilities(config))
        elif config.auth.method == AuthMethod.OAUTH2:
            auth_files.update(await self._generate_oauth2_utilities(config))
        
        # Generate password security
        auth_files.update(await self._generate_password_security(config))
        
        return auth_files
    
    async def _generate_django_auth(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django authentication implementation using LLM."""
        
        django_auth_prompt = f"""
        Generate Django authentication system:
        
        Auth Method: {config.auth.method.value}
        User Model: Custom User model if needed
        Features: {config.features}
        
        Generate comprehensive Django authentication including:
        1. Custom User model if needed
        2. Authentication backends
        3. Login/logout views and forms
        4. User registration and activation
        5. Password reset functionality
        6. Profile management views
        7. Permission and group management
        8. Social authentication integration if specified
        9. Session management
        10. Authentication middleware and decorators
        
        Files to generate:
        - models.py - User model and profile
        - views.py - Authentication views
        - forms.py - Authentication forms
        - backends.py - Custom authentication backends
        - decorators.py - Permission decorators
        
        Return production-ready Django authentication code.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="claude",
            action="reasoning",
            data={
                "prompt": django_auth_prompt,
                "system_prompt": "You are a Django authentication expert. Generate secure, reusable auth systems."
            }
        )
        
        auth_files = self._parse_django_auth_files(response.result)
        
        # Generate Django-specific auth files
        auth_files.update(await self._generate_django_permissions(config))
        auth_files.update(await self._generate_django_signals(config))
        
        return auth_files
    
    async def _generate_nestjs_auth(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS authentication implementation using LLM."""
        
        nestjs_auth_prompt = f"""
        Generate NestJS authentication system:
        
        Auth Method: {config.auth.method.value}
        Strategy: Passport.js integration
        Guards: JWT and Local guards
        
        Generate comprehensive NestJS authentication including:
        1. Authentication module with providers
        2. Passport strategies (Local, JWT)
        3. Authentication guards for routes
        4. Authentication controller with login/register
        5. User service for authentication logic
        6. JWT token management
        7. Role-based authorization guards
        8. Authentication decorators
        9. Password hashing service
        10. Authentication exception filters
        
        Files to generate:
        - auth.module.ts - Authentication module
        - auth.controller.ts - Authentication endpoints
        - auth.service.ts - Authentication business logic
        - strategies/ - Passport strategies
        - guards/ - Authentication guards
        - decorators/ - Auth decorators
        
        Return production-ready NestJS authentication with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="deepseek",
            action="fast_coding",
            data={
                "prompt": nestjs_auth_prompt,
                "language": "typescript"
            }
        )
        
        auth_files = self._parse_nestjs_auth_files(response.result)
        
        # Generate NestJS-specific auth files
        auth_files.update(await self._generate_nestjs_strategies(config))
        auth_files.update(await self._generate_nestjs_guards(config))
        
        return auth_files
    
    async def _generate_jwt_utilities(self, config: BackendConfig) -> Dict[str, str]:
        """Generate JWT-specific utilities."""
        
        jwt_utils_prompt = f"""
        Generate JWT utilities for {config.framework.value}:
        
        Secret Key: {config.auth.secret_key}
        Algorithm: {config.auth.algorithm}
        Access Token Expiry: {config.auth.access_token_expire_minutes} minutes
        Refresh Token Expiry: {config.auth.refresh_token_expire_days} days
        
        Generate JWT utilities including:
        1. Token creation functions
        2. Token verification and validation
        3. Token refresh logic
        4. Payload extraction utilities
        5. Token blacklisting support
        6. Error handling for invalid tokens
        
        Return comprehensive JWT utility functions.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="openai",
            action="code_generation",
            data={"prompt": jwt_utils_prompt, "language": config.language}
        )
        
        return {"app/core/jwt.py": response.result}
    
    async def _generate_oauth2_utilities(self, config: BackendConfig) -> Dict[str, str]:
        """Generate OAuth2-specific utilities."""
        
        oauth2_utils_prompt = f"""
        Generate OAuth2 utilities for {config.framework.value}:
        
        Providers: {config.auth.oauth_providers if hasattr(config.auth, 'oauth_providers') else ['google', 'github']}
        
        Generate OAuth2 utilities including:
        1. Provider configurations
        2. Authorization URL generation
        3. Token exchange handlers
        4. User profile fetching
        5. Account linking logic
        6. Provider-specific error handling
        
        Return comprehensive OAuth2 utility functions.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": oauth2_utils_prompt}
        )
        
        return {"app/core/oauth2.py": response.result}
    
    async def _generate_password_security(self, config: BackendConfig) -> Dict[str, str]:
        """Generate password security utilities."""
        
        password_security_prompt = f"""
        Generate password security utilities for {config.framework.value}:
        
        Generate password security including:
        1. Password hashing with bcrypt/argon2
        2. Password strength validation
        3. Password history tracking
        4. Secure password generation
        5. Password reset token management
        6. Account lockout protection
        7. Breach detection integration
        
        Return comprehensive password security utilities.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": password_security_prompt}
        )
        
        return {"app/core/passwords.py": response.result}
    
    async def _generate_django_permissions(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django permission system."""
        
        permissions_prompt = """
        Generate Django permission system:
        
        Generate permissions including:
        1. Custom permission classes
        2. Object-level permissions
        3. Group-based permissions
        4. Role-based access control
        5. Permission decorators
        6. Permission templates and mixins
        
        Return Django permission system.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="django",
            action="code_generation",
            data={"prompt": permissions_prompt, "language": "python"}
        )
        
        return {"permissions.py": response.result}
    
    async def _generate_django_signals(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django authentication signals."""
        
        signals_prompt = """
        Generate Django authentication signals:
        
        Generate signals for:
        1. User registration
        2. User login/logout
        3. Password changes
        4. Profile updates
        5. Account activation
        6. Permission changes
        
        Return Django signal handlers.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="django",
            action="code_generation",
            data={"prompt": signals_prompt, "language": "python"}
        )
        
        return {"signals.py": response.result}
    
    async def _generate_nestjs_strategies(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS Passport strategies."""
        
        strategies_prompt = f"""
        Generate NestJS Passport strategies:
        
        Auth Method: {config.auth.method.value}
        
        Generate strategies for:
        1. Local strategy for username/password
        2. JWT strategy for token validation
        3. OAuth strategies if needed
        4. Custom validation logic
        5. Error handling
        
        Return NestJS Passport strategies with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="nestjs",
            action="code_generation",
            data={"prompt": strategies_prompt, "language": "typescript"}
        )
        
        return {
            "src/auth/strategies/local.strategy.ts": "# Local strategy",
            "src/auth/strategies/jwt.strategy.ts": response.result
        }
    
    async def _generate_nestjs_guards(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS authentication guards."""
        
        guards_prompt = """
        Generate NestJS authentication guards:
        
        Generate guards for:
        1. JWT authentication guard
        2. Local authentication guard
        3. Role-based authorization guard
        4. Permission-based guard
        5. Optional authentication guard
        6. Rate limiting guard
        
        Return NestJS guards with TypeScript.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="nestjs",
            action="code_generation",
            data={"prompt": guards_prompt, "language": "typescript"}
        )
        
        return {
            "src/auth/guards/jwt-auth.guard.ts": response.result,
            "src/auth/guards/roles.guard.ts": "# Roles guard"
        }
    
    # Method-specific generators
    async def _generate_jwt_system(self, config: BackendConfig) -> Dict[str, str]:
        """Generate JWT authentication system."""
        jwt_files = {}
        
        if config.framework == BackendFramework.FASTAPI:
            jwt_files.update(await self._generate_fastapi_jwt(config))
        elif config.framework == BackendFramework.DJANGO:
            jwt_files.update(await self._generate_django_jwt(config))
        elif config.framework == BackendFramework.NESTJS:
            jwt_files.update(await self._generate_nestjs_jwt(config))
        
        return jwt_files
    
    async def _generate_oauth2_system(self, config: BackendConfig) -> Dict[str, str]:
        """Generate OAuth2 authentication system."""
        oauth2_files = {}
        
        if config.framework == BackendFramework.FASTAPI:
            oauth2_files.update(await self._generate_fastapi_oauth2(config))
        elif config.framework == BackendFramework.DJANGO:
            oauth2_files.update(await self._generate_django_oauth2(config))
        elif config.framework == BackendFramework.NESTJS:
            oauth2_files.update(await self._generate_nestjs_oauth2(config))
        
        return oauth2_files
    
    async def _generate_session_system(self, config: BackendConfig) -> Dict[str, str]:
        """Generate session-based authentication system."""
        session_files = {}
        
        if config.framework == BackendFramework.FASTAPI:
            session_files.update(await self._generate_fastapi_sessions(config))
        elif config.framework == BackendFramework.DJANGO:
            session_files.update(await self._generate_django_sessions(config))
        elif config.framework == BackendFramework.NESTJS:
            session_files.update(await self._generate_nestjs_sessions(config))
        
        return session_files
    
    async def _generate_fastapi_jwt(self, config: BackendConfig) -> Dict[str, str]:
        """Generate FastAPI JWT implementation."""
        return {"app/auth/jwt.py": "# FastAPI JWT implementation"}
    
    async def _generate_django_jwt(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django JWT implementation."""
        return {"auth/jwt.py": "# Django JWT implementation"}
    
    async def _generate_nestjs_jwt(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS JWT implementation."""
        return {"src/auth/jwt.service.ts": "# NestJS JWT implementation"}
    
    async def _generate_fastapi_oauth2(self, config: BackendConfig) -> Dict[str, str]:
        """Generate FastAPI OAuth2 implementation."""
        return {"app/auth/oauth2.py": "# FastAPI OAuth2 implementation"}
    
    async def _generate_django_oauth2(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django OAuth2 implementation."""
        return {"auth/oauth2.py": "# Django OAuth2 implementation"}
    
    async def _generate_nestjs_oauth2(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS OAuth2 implementation."""
        return {"src/auth/oauth2.service.ts": "# NestJS OAuth2 implementation"}
    
    async def _generate_fastapi_sessions(self, config: BackendConfig) -> Dict[str, str]:
        """Generate FastAPI session implementation."""
        return {"app/auth/sessions.py": "# FastAPI sessions implementation"}
    
    async def _generate_django_sessions(self, config: BackendConfig) -> Dict[str, str]:
        """Generate Django session implementation."""
        return {"auth/sessions.py": "# Django sessions implementation"}
    
    async def _generate_nestjs_sessions(self, config: BackendConfig) -> Dict[str, str]:
        """Generate NestJS session implementation."""
        return {"src/auth/sessions.service.ts": "# NestJS sessions implementation"}
    
    # Utility methods for parsing LLM responses
    def _parse_fastapi_auth_files(self, llm_response: str) -> Dict[str, str]:
        """Parse FastAPI auth files from LLM response."""
        return {
            "app/core/security.py": "# FastAPI security utilities",
            "app/core/auth.py": llm_response,
            "app/api/v1/auth.py": "# Authentication endpoints",
            "app/dependencies/auth.py": "# Authentication dependencies"
        }
    
    def _parse_django_auth_files(self, llm_response: str) -> Dict[str, str]:
        """Parse Django auth files from LLM response."""
        return {
            "auth/models.py": "# User models",
            "auth/views.py": llm_response,
            "auth/forms.py": "# Authentication forms",
            "auth/backends.py": "# Authentication backends",
            "auth/urls.py": "# Authentication URLs"
        }
    
    def _parse_nestjs_auth_files(self, llm_response: str) -> Dict[str, str]:
        """Parse NestJS auth files from LLM response."""
        return {
            "src/auth/auth.module.ts": "# Authentication module",
            "src/auth/auth.controller.ts": "# Authentication controller",
            "src/auth/auth.service.ts": llm_response,
            "src/auth/dto/auth.dto.ts": "# Authentication DTOs"
        }
    
    # Additional utility methods
    async def generate_auth_tests(self, config: BackendConfig) -> Dict[str, str]:
        """Generate authentication tests."""
        
        auth_tests_prompt = f"""
        Generate authentication tests for {config.framework.value}:
        
        Auth Method: {config.auth.method.value}
        Framework: {config.framework.value}
        
        Generate tests for:
        1. User registration and login
        2. Token generation and validation
        3. Password hashing and verification
        4. Permission and authorization
        5. Authentication middleware
        6. Error handling scenarios
        
        Return comprehensive authentication test suite.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="openai",
            action="code_generation",
            data={
                "prompt": auth_tests_prompt,
                "language": config.language
            }
        )
        
        return {"tests/test_auth.py": response.result}
    
    async def generate_auth_documentation(self, config: BackendConfig) -> Dict[str, str]:
        """Generate authentication documentation."""
        
        auth_docs_prompt = f"""
        Generate authentication documentation for {config.framework.value}:
        
        Auth Method: {config.auth.method.value}
        Features: {config.features}
        
        Generate documentation for:
        1. Authentication setup and configuration
        2. API endpoints and usage examples
        3. Token management and refresh
        4. Permission and authorization guide
        5. Security best practices
        6. Troubleshooting guide
        
        Return comprehensive authentication documentation in Markdown.
        """
        
        response = await protocol.send_request(
            sender_id="auth_generator",
            target_id="claude",
            action="reasoning",
            data={"prompt": auth_docs_prompt}
        )
        
        return {
            "docs/authentication.md": response.result,
            "docs/authorization.md": "# Authorization guide",
            "docs/security.md": "# Security best practices"
        }
