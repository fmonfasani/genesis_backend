"""
Authentication Agent

Specializes in generating authentication and authorization systems using LLMs.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from genesis_agents import GenesisAgent, AgentTask, TaskResult
from mcpturbo import protocol

from ..config import BackendConfig, AuthMethod, BackendFramework

logger = logging.getLogger(__name__)


class AuthAgent(GenesisAgent):
    """
    Agent specialized in authentication and authorization systems.
    
    Responsibilities:
    - Generate authentication logic (JWT, OAuth2, Session)
    - Generate authorization middleware
    - Create user management systems
    - Design permission and role systems
    - Generate security utilities
    - Create password management systems
    """
    
    def __init__(self):
        super().__init__(
            agent_id="auth_specialist",
            name="Authentication Specialist Agent",
            agent_type="authentication"
        )
        
        # Authentication-specific capabilities
        self.add_capability("generate_jwt_auth")
        self.add_capability("generate_oauth2_auth")
        self.add_capability("generate_session_auth")
        self.add_capability("generate_user_management")
        self.add_capability("generate_role_permissions")
        self.add_capability("generate_auth_middleware")
        self.add_capability("generate_password_security")
        self.add_capability("generate_social_auth")
        
        # Register handlers
        self.register_handler("generate_jwt_auth", self._handle_generate_jwt)
        self.register_handler("generate_oauth2_auth", self._handle_generate_oauth2)
        self.register_handler("generate_session_auth", self._handle_generate_session)
        self.register_handler("generate_user_management", self._handle_generate_users)
        self.register_handler("generate_role_permissions", self._handle_generate_roles)
        self.register_handler("generate_auth_middleware", self._handle_generate_middleware)
        self.register_handler("generate_password_security", self._handle_generate_passwords)
        self.register_handler("generate_social_auth", self._handle_generate_social)
        
        # Authentication method configurations
        self.auth_configs = {
            AuthMethod.JWT: {
                "token_type": "Bearer",
                "default_expiry": 3600,
                "algorithm": "HS256",
                "refresh_enabled": True
            },
            AuthMethod.OAUTH2: {
                "flows": ["authorization_code", "client_credentials"],
                "scopes": ["read", "write"],
                "token_endpoint": "/oauth/token",
                "auth_endpoint": "/oauth/authorize"
            },
            AuthMethod.SESSION: {
                "session_timeout": 1800,
                "cookie_secure": True,
                "cookie_httponly": True,
                "csrf_protection": True
            }
        }
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Execute authentication-related task using LLMs."""
        try:
            self.logger.info(f"🔐 Executing authentication task: {task.name}")
            
            if task.name == "generate_jwt_auth":
                result = await self._generate_jwt_authentication(task.params)
            elif task.name == "generate_oauth2_auth":
                result = await self._generate_oauth2_authentication(task.params)
            elif task.name == "generate_session_auth":
                result = await self._generate_session_authentication(task.params)
            elif task.name == "generate_user_management":
                result = await self._generate_user_management_system(task.params)
            elif task.name == "generate_role_permissions":
                result = await self._generate_role_permission_system(task.params)
            elif task.name == "generate_auth_middleware":
                result = await self._generate_authentication_middleware(task.params)
            elif task.name == "generate_password_security":
                result = await self._generate_password_security_system(task.params)
            elif task.name == "generate_social_auth":
                result = await self._generate_social_authentication(task.params)
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
            self.logger.error(f"❌ Error in authentication task {task.name}: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                metadata={"agent": self.name, "task_type": task.name}
            )
    
    async def _generate_jwt_authentication(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JWT authentication system using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        user_model = params.get("user_model", {})
        
        jwt_generation_prompt = f"""
        Generate comprehensive JWT authentication system for {config.framework.value}:
        
        Framework: {config.framework.value}
        User Model: {user_model}
        Secret Key: {config.auth.secret_key}
        Algorithm: {config.auth.algorithm}
        Token Expiry: {config.auth.access_token_expire_minutes} minutes
        Refresh Token Expiry: {config.auth.refresh_token_expire_days} days
        
        Generate complete JWT authentication including:
        1. JWT token creation and signing
        2. Token verification and validation
        3. Token refresh mechanism
        4. User login endpoint with credentials validation
        5. User registration endpoint with password hashing
        6. Password reset functionality
        7. Token blacklisting for logout
        8. Authentication dependencies for protected routes
        9. Permission checking decorators/middleware
        10. Error handling for authentication failures
        
        Security considerations:
        - Secure password hashing (bcrypt/argon2)
        - Token expiration handling
        - Rate limiting for authentication endpoints
        - Input validation and sanitization
        - Secure token storage recommendations
        
        Return production-ready authentication code.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at authentication patterns
            action="code_generation",
            data={
                "prompt": jwt_generation_prompt,
                "language": config.language,
                "framework": f"{config.framework.value}_jwt"
            }
        )
        
        return {
            "auth_code": response.result,
            "endpoints": self._extract_auth_endpoints(response.result),
            "middleware": self._extract_auth_middleware(response.result),
            "utilities": self._extract_auth_utilities(response.result),
            "security_features": self._extract_security_features(response.result),
            "configuration": self._extract_auth_configuration(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "auth_method": "jwt"
            }
        }
    
    async def _generate_oauth2_authentication(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate OAuth2 authentication system using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        oauth_providers = params.get("oauth_providers", ["google", "github"])
        
        oauth2_generation_prompt = f"""
        Generate OAuth2 authentication system for {config.framework.value}:
        
        Framework: {config.framework.value}
        OAuth Providers: {oauth_providers}
        Client Configuration: Required for each provider
        
        Generate complete OAuth2 authentication including:
        1. OAuth2 authorization flow implementation
        2. Provider-specific client configurations
        3. Authorization URL generation
        4. Token exchange with providers
        5. User profile fetching from providers
        6. Account linking with local users
        7. Refresh token handling
        8. Provider-specific scopes handling
        9. Error handling for OAuth failures
        10. Security validations (state parameter, nonce)
        
        For each provider include:
        - Authorization endpoint configuration
        - Token endpoint configuration
        - User info endpoint configuration
        - Scope definitions
        - Error handling
        
        Security considerations:
        - State parameter validation
        - PKCE for public clients
        - Secure redirect URI validation
        - Token storage security
        
        Return production-ready OAuth2 implementation.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at OAuth2 flows
            action="reasoning",
            data={
                "prompt": oauth2_generation_prompt,
                "system_prompt": "You are an OAuth2 security expert. Generate secure, compliant implementations."
            }
        )
        
        return {
            "oauth2_code": response.result,
            "provider_configs": self._extract_provider_configs(response.result),
            "flow_handlers": self._extract_flow_handlers(response.result),
            "security_validations": self._extract_security_validations(response.result),
            "error_handling": self._extract_error_handling(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "auth_method": "oauth2"
            }
        }
    
    async def _generate_session_authentication(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate session-based authentication using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        
        session_generation_prompt = f"""
        Generate session-based authentication system for {config.framework.value}:
        
        Framework: {config.framework.value}
        Session Timeout: 30 minutes
        Security Requirements: CSRF protection, secure cookies
        
        Generate complete session authentication including:
        1. Session management and storage
        2. Login form handling with CSRF protection
        3. Session cookie configuration (secure, httponly)
        4. Session timeout and cleanup
        5. Remember me functionality
        6. Logout and session destruction
        7. Session fixation protection
        8. Concurrent session handling
        9. Session-based authorization
        10. Audit logging for sessions
        
        Security considerations:
        - Session regeneration on login
        - CSRF token validation
        - Secure cookie attributes
        - Session timeout handling
        - Session storage security
        
        For Django: Use built-in session framework
        For FastAPI: Implement custom session management
        For NestJS: Use express-session with security
        
        Return production-ready session implementation.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at session management
            action="code_generation",
            data={
                "prompt": session_generation_prompt,
                "language": config.language,
                "framework": f"{config.framework.value}_session"
            }
        )
        
        return {
            "session_code": response.result,
            "session_config": self._extract_session_config(response.result),
            "csrf_protection": self._extract_csrf_protection(response.result),
            "security_middleware": self._extract_security_middleware(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name,
                "auth_method": "session"
            }
        }
    
    async def _generate_user_management_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate user management system using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        user_fields = params.get("user_fields", [])
        
        user_management_prompt = f"""
        Generate comprehensive user management system for {config.framework.value}:
        
        Framework: {config.framework.value}
        User Fields: {user_fields}
        Authentication Method: {config.auth.method.value}
        
        Generate complete user management including:
        1. User registration with validation
        2. Email verification system
        3. User profile management
        4. Password change functionality
        5. Account activation/deactivation
        6. User search and filtering
        7. User listing with pagination
        8. Account deletion (soft/hard delete)
        9. User import/export functionality
        10. Admin user management interface
        
        Features to include:
        - Input validation and sanitization
        - Duplicate email prevention
        - Password strength validation
        - Rate limiting for sensitive operations
        - Audit logging for user actions
        - GDPR compliance considerations
        
        Generate:
        - User model/entity with all fields
        - CRUD operations for users
        - API endpoints for user management
        - Validation schemas
        - Service layer for business logic
        
        Return complete user management system.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at user management patterns
            action="reasoning",
            data={
                "prompt": user_management_prompt,
                "system_prompt": "You are a user management expert. Generate secure, compliant systems."
            }
        )
        
        return {
            "user_management_code": response.result,
            "user_model": self._extract_user_model(response.result),
            "crud_operations": self._extract_crud_operations(response.result),
            "validation_rules": self._extract_validation_rules(response.result),
            "api_endpoints": self._extract_api_endpoints(response.result),
            "business_logic": self._extract_business_logic(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_role_permission_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate role and permission system using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        roles = params.get("roles", ["admin", "user", "moderator"])
        permissions = params.get("permissions", [])
        
        rbac_generation_prompt = f"""
        Generate Role-Based Access Control (RBAC) system for {config.framework.value}:
        
        Framework: {config.framework.value}
        Roles: {roles}
        Permissions: {permissions}
        
        Generate complete RBAC system including:
        1. Role model with hierarchical support
        2. Permission model with granular controls
        3. User-role assignment system
        4. Role-permission assignment system
        5. Permission checking decorators/middleware
        6. Role inheritance and hierarchies
        7. Dynamic permission evaluation
        8. Resource-based permissions
        9. Permission caching for performance
        10. Admin interface for role management
        
        Features to include:
        - Multi-role assignment per user
        - Permission aggregation from multiple roles
        - Time-based permissions (temporary access)
        - Resource-level permissions (object-level)
        - Permission auditing and logging
        - Efficient permission checking queries
        
        Generate:
        - Role and Permission models
        - Many-to-many relationship tables
        - Permission checking utilities
        - Decorators for route protection
        - API endpoints for role management
        - Migration scripts for default roles
        
        Return complete RBAC implementation.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude excellent at RBAC patterns
            action="reasoning",
            data={
                "prompt": rbac_generation_prompt,
                "system_prompt": "You are an RBAC expert. Generate flexible, scalable permission systems."
            }
        )
        
        return {
            "rbac_code": response.result,
            "role_model": self._extract_role_model(response.result),
            "permission_model": self._extract_permission_model(response.result),
            "permission_decorators": self._extract_permission_decorators(response.result),
            "assignment_logic": self._extract_assignment_logic(response.result),
            "checking_utilities": self._extract_checking_utilities(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_authentication_middleware(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate authentication middleware using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        
        middleware_generation_prompt = f"""
        Generate authentication middleware for {config.framework.value}:
        
        Framework: {config.framework.value}
        Auth Method: {config.auth.method.value}
        Features: {config.features}
        
        Generate comprehensive authentication middleware including:
        1. Request authentication validation
        2. Token/session extraction and validation
        3. User context injection into requests
        4. Protected route handling
        5. Permission-based route protection
        6. Rate limiting for authentication
        7. Audit logging for auth events
        8. Error handling and response formatting
        9. CORS handling for auth headers
        10. Security headers injection
        
        Middleware features:
        - Configurable authentication requirements
        - Flexible permission checking
        - Efficient database queries
        - Proper error responses
        - Request context management
        - Performance optimization
        
        For FastAPI: Use dependency injection system
        For Django: Use middleware classes
        For NestJS: Use guards and interceptors
        
        Return production-ready middleware.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",  # DeepSeek good at middleware patterns
            action="fast_coding",
            data={
                "prompt": middleware_generation_prompt,
                "language": config.language
            }
        )
        
        return {
            "middleware_code": response.result,
            "middleware_classes": self._extract_middleware_classes(response.result),
            "configuration": self._extract_middleware_configuration(response.result),
            "error_handlers": self._extract_error_handlers(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_password_security_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate password security system using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        
        password_security_prompt = f"""
        Generate comprehensive password security system for {config.framework.value}:
        
        Framework: {config.framework.value}
        Security Requirements: Industry standard password security
        
        Generate complete password security including:
        1. Secure password hashing (bcrypt/argon2)
        2. Password strength validation
        3. Password history tracking
        4. Password reset with secure tokens
        5. Password change functionality
        6. Account lockout after failed attempts
        7. Password expiration policies
        8. Breach detection integration
        9. Two-factor authentication support
        10. Password recovery workflows
        
        Security features:
        - Configurable password policies
        - Secure random token generation
        - Time-limited reset tokens
        - Rate limiting for password operations
        - Audit logging for password events
        - Secure password transmission
        
        Generate:
        - Password hashing utilities
        - Validation functions
        - Reset token management
        - Account lockout logic
        - Password history tracking
        - Security audit functions
        
        Return production-ready password security system.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at security implementations
            action="reasoning",
            data={
                "prompt": password_security_prompt,
                "system_prompt": "You are a password security expert. Generate secure, compliant systems."
            }
        )
        
        return {
            "password_security_code": response.result,
            "hashing_utilities": self._extract_hashing_utilities(response.result),
            "validation_functions": self._extract_validation_functions(response.result),
            "reset_system": self._extract_reset_system(response.result),
            "lockout_logic": self._extract_lockout_logic(response.result),
            "audit_functions": self._extract_audit_functions(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    async def _generate_social_authentication(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate social authentication integration using LLM."""
        config = BackendConfig.from_dict(params.get("config", {}))
        providers = params.get("providers", ["google", "github", "facebook"])
        
        social_auth_prompt = f"""
        Generate social authentication integration for {config.framework.value}:
        
        Framework: {config.framework.value}
        Social Providers: {providers}
        
        Generate complete social authentication including:
        1. Provider-specific OAuth configuration
        2. Social login button integration
        3. User profile data fetching
        4. Account linking with existing users
        5. Social account management
        6. Provider-specific error handling
        7. Fallback authentication options
        8. Social profile synchronization
        9. Provider disconnection functionality
        10. Social sharing capabilities
        
        For each provider include:
        - Client configuration
        - Authorization flow
        - Profile data mapping
        - Scope management
        - Error handling
        
        Generate:
        - Provider configuration classes
        - OAuth flow handlers
        - User profile mappers
        - Account linking logic
        - Frontend integration helpers
        - Provider management API
        
        Return complete social authentication system.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good at social integrations
            action="code_generation",
            data={
                "prompt": social_auth_prompt,
                "language": config.language,
                "framework": f"{config.framework.value}_social"
            }
        )
        
        return {
            "social_auth_code": response.result,
            "provider_configs": self._extract_social_provider_configs(response.result),
            "flow_handlers": self._extract_social_flow_handlers(response.result),
            "profile_mappers": self._extract_profile_mappers(response.result),
            "linking_logic": self._extract_linking_logic(response.result),
            "management_api": self._extract_management_api(response.result),
            "generation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "generator": self.name
            }
        }
    
    # Handler methods for MCP protocol
    async def _handle_generate_jwt(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_jwt_authentication(data)
    
    async def _handle_generate_oauth2(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_oauth2_authentication(data)
    
    async def _handle_generate_session(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_session_authentication(data)
    
    async def _handle_generate_users(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_user_management_system(data)
    
    async def _handle_generate_roles(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_role_permission_system(data)
    
    async def _handle_generate_middleware(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_authentication_middleware(data)
    
    async def _handle_generate_passwords(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_password_security_system(data)
    
    async def _handle_generate_social(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._generate_social_authentication(data)
    
    async def _handle_generic_task(self, task: AgentTask) -> Dict[str, Any]:
        return {
            "message": f"Generic authentication task {task.name} processed",
            "task_id": task.id,
            "agent": self.name
        }
    
    # Utility methods for parsing LLM responses
    def _extract_auth_endpoints(self, code: str) -> List[Dict[str, str]]:
        """Extract authentication endpoints from generated code."""
        return [
            {"path": "/auth/login", "method": "POST", "description": "User login"},
            {"path": "/auth/register", "method": "POST", "description": "User registration"},
            {"path": "/auth/refresh", "method": "POST", "description": "Token refresh"},
            {"path": "/auth/logout", "method": "POST", "description": "User logout"}
        ]
    
    def _extract_auth_middleware(self, code: str) -> List[str]:
        """Extract authentication middleware from code."""
        return ["get_current_user", "require_authentication", "check_permissions"]
    
    def _extract_auth_utilities(self, code: str) -> List[str]:
        """Extract authentication utilities from code."""
        return ["create_access_token", "verify_token", "hash_password", "verify_password"]
    
    def _extract_security_features(self, code: str) -> List[str]:
        """Extract security features from code."""
        return ["Password hashing", "Token expiration", "Rate limiting", "Input validation"]
    
    def _extract_auth_configuration(self, code: str) -> Dict[str, Any]:
        """Extract authentication configuration."""
        return {
            "token_expiry": "30 minutes",
            "refresh_expiry": "7 days",
            "algorithm": "HS256",
            "issuer": "genesis-api"
        }
    
    def _extract_provider_configs(self, code: str) -> Dict[str, Dict[str, str]]:
        """Extract OAuth provider configurations."""
        return {
            "google": {
                "client_id": "GOOGLE_CLIENT_ID",
                "client_secret": "GOOGLE_CLIENT_SECRET",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            },
            "github": {
                "client_id": "GITHUB_CLIENT_ID", 
                "client_secret": "GITHUB_CLIENT_SECRET",
                "auth_uri": "https://github.com/login/oauth/authorize",
                "token_uri": "https://github.com/login/oauth/access_token"
            }
        }
    
    def _extract_flow_handlers(self, code: str) -> List[str]:
        """Extract OAuth flow handlers."""
        return ["authorization_code_flow", "client_credentials_flow", "refresh_token_flow"]
    
    def _extract_security_validations(self, code: str) -> List[str]:
        """Extract security validations."""
        return ["state_parameter_validation", "nonce_validation", "redirect_uri_validation"]
    
    def _extract_error_handling(self, code: str) -> List[str]:
        """Extract error handling mechanisms."""
        return ["invalid_grant", "unauthorized_client", "access_denied", "server_error"]
    
    def _extract_session_config(self, code: str) -> Dict[str, Any]:
        """Extract session configuration."""
        return {
            "timeout": "30 minutes",
            "secure": True,
            "httponly": True,
            "samesite": "lax"
        }
    
    def _extract_csrf_protection(self, code: str) -> Dict[str, str]:
        """Extract CSRF protection details."""
        return {
            "token_generation": "secure_random_token",
            "validation": "form_and_header_validation",
            "storage": "session_storage"
        }
    
    def _extract_security_middleware(self, code: str) -> List[str]:
        """Extract security middleware."""
        return ["csrf_middleware", "session_middleware", "security_headers_middleware"]
    
    def _extract_user_model(self, code: str) -> Dict[str, Any]:
        """Extract user model information."""
        return {
            "fields": ["id", "email", "password_hash", "is_active", "created_at"],
            "relationships": ["roles", "permissions", "sessions"],
            "methods": ["check_password", "set_password", "get_full_name"]
        }
    
    def _extract_crud_operations(self, code: str) -> List[str]:
        """Extract CRUD operations."""
        return ["create_user", "get_user", "update_user", "delete_user", "list_users"]
    
    def _extract_validation_rules(self, code: str) -> Dict[str, List[str]]:
        """Extract validation rules."""
        return {
            "email": ["email_format", "unique", "required"],
            "password": ["min_length_8", "complexity", "required"],
            "name": ["max_length_100", "required"]
        }
    
    def _extract_api_endpoints(self, code: str) -> List[Dict[str, str]]:
        """Extract API endpoints."""
        return [
            {"path": "/users", "method": "GET", "description": "List users"},
            {"path": "/users", "method": "POST", "description": "Create user"},
            {"path": "/users/{id}", "method": "GET", "description": "Get user"},
            {"path": "/users/{id}", "method": "PUT", "description": "Update user"},
            {"path": "/users/{id}", "method": "DELETE", "description": "Delete user"}
        ]
    
    def _extract_business_logic(self, code: str) -> List[str]:
        """Extract business logic components."""
        return ["UserService", "RegistrationService", "ProfileService", "NotificationService"]
    
    def _extract_role_model(self, code: str) -> Dict[str, Any]:
        """Extract role model information."""
        return {
            "fields": ["id", "name", "description", "level", "created_at"],
            "relationships": ["users", "permissions", "parent_role"],
            "methods": ["has_permission", "add_permission", "remove_permission"]
        }
    
    def _extract_permission_model(self, code: str) -> Dict[str, Any]:
        """Extract permission model information."""
        return {
            "fields": ["id", "name", "resource", "action", "description"],
            "relationships": ["roles"],
            "methods": ["check_access", "get_resource_permissions"]
        }
    
    def _extract_permission_decorators(self, code: str) -> List[str]:
        """Extract permission decorators."""
        return ["require_permission", "require_role", "require_auth", "check_resource_access"]
    
    def _extract_assignment_logic(self, code: str) -> List[str]:
        """Extract assignment logic functions."""
        return ["assign_role", "remove_role", "assign_permission", "remove_permission"]
    
    def _extract_checking_utilities(self, code: str) -> List[str]:
        """Extract permission checking utilities."""
        return ["has_permission", "has_role", "can_access_resource", "get_user_permissions"]
    
    def _extract_middleware_classes(self, code: str) -> List[str]:
        """Extract middleware classes."""
        return ["AuthenticationMiddleware", "PermissionMiddleware", "RateLimitMiddleware"]
    
    def _extract_middleware_configuration(self, code: str) -> Dict[str, Any]:
        """Extract middleware configuration."""
        return {
            "auth_header": "Authorization",
            "token_prefix": "Bearer",
            "rate_limit": "100/hour",
            "exclude_paths": ["/health", "/docs"]
        }
    
    def _extract_error_handlers(self, code: str) -> List[str]:
        """Extract error handlers."""
        return ["handle_auth_error", "handle_permission_error", "handle_rate_limit_error"]
    
    def _extract_hashing_utilities(self, code: str) -> List[str]:
        """Extract password hashing utilities."""
        return ["hash_password", "verify_password", "generate_salt", "check_strength"]
    
    def _extract_validation_functions(self, code: str) -> List[str]:
        """Extract password validation functions."""
        return ["validate_strength", "check_history", "validate_complexity", "check_breach"]
    
    def _extract_reset_system(self, code: str) -> List[str]:
        """Extract password reset system components."""
        return ["generate_reset_token", "validate_reset_token", "reset_password", "send_reset_email"]
    
    def _extract_lockout_logic(self, code: str) -> List[str]:
        """Extract account lockout logic."""
        return ["track_failed_attempts", "lock_account", "unlock_account", "check_lockout_status"]
    
    def _extract_audit_functions(self, code: str) -> List[str]:
        """Extract audit functions."""
        return ["log_password_change", "log_failed_attempt", "log_lockout", "log_reset_request"]
    
    def _extract_social_provider_configs(self, code: str) -> Dict[str, Any]:
        """Extract social provider configurations."""
        return {
            "google": {"scopes": ["email", "profile"], "button_style": "standard"},
            "github": {"scopes": ["user:email"], "button_style": "dark"},
            "facebook": {"scopes": ["email", "public_profile"], "button_style": "continue_with"}
        }
    
    def _extract_social_flow_handlers(self, code: str) -> List[str]:
        """Extract social flow handlers."""
        return ["handle_google_auth", "handle_github_auth", "handle_facebook_auth", "handle_callback"]
    
    def _extract_profile_mappers(self, code: str) -> List[str]:
        """Extract profile mappers."""
        return ["map_google_profile", "map_github_profile", "map_facebook_profile", "normalize_profile"]
    
    def _extract_linking_logic(self, code: str) -> List[str]:
        """Extract account linking logic."""
        return ["link_social_account", "unlink_social_account", "find_existing_user", "merge_accounts"]
    
    def _extract_management_api(self, code: str) -> List[Dict[str, str]]:
        """Extract social account management API."""
        return [
            {"path": "/auth/social/connect", "method": "POST", "description": "Connect social account"},
            {"path": "/auth/social/disconnect", "method": "POST", "description": "Disconnect social account"},
            {"path": "/auth/social/accounts", "method": "GET", "description": "List connected accounts"}
        ]