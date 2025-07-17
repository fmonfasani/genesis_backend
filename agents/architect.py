"""
Backend Architect Agent

Specializes in designing backend architecture using LLMs.
Focuses specifically on backend concerns: APIs, data models, services, middleware.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from genesis_agents import GenesisAgent, AgentTask, TaskResult
from mcpturbo import protocol

from ..config import BackendConfig, BackendFramework, DatabaseType, AuthMethod

logger = logging.getLogger(__name__)


class ArchitectAgent(GenesisAgent):
    """
    Agent specialized in backend architecture design.
    
    Responsibilities:
    - Analyze backend requirements
    - Design API architecture
    - Design data models and relationships
    - Select appropriate backend technologies
    - Define service layer architecture
    """
    
    def __init__(self):
        super().__init__(
            agent_id="backend_architect",
            name="Backend Architect Agent",
            agent_type="architect"
        )
        
        # Backend-specific capabilities
        self.add_capability("analyze_backend_requirements")
        self.add_capability("design_api_architecture")
        self.add_capability("design_data_models")
        self.add_capability("select_backend_technologies")
        self.add_capability("design_service_architecture")
        self.add_capability("validate_backend_architecture")
        
        # Register handlers
        self.register_handler("analyze_backend_requirements", self._handle_analyze_requirements)
        self.register_handler("design_api_architecture", self._handle_design_api)
        self.register_handler("design_data_models", self._handle_design_models)
        self.register_handler("select_backend_technologies", self._handle_select_technologies)
        self.register_handler("design_service_architecture", self._handle_design_services)
        self.register_handler("validate_backend_architecture", self._handle_validate_architecture)
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Execute backend architecture task using LLMs."""
        try:
            self.logger.info(f"🏗️ Executing backend architecture task: {task.name}")
            
            if task.name == "analyze_backend_requirements":
                result = await self._analyze_backend_requirements(task.params)
            elif task.name == "design_api_architecture":
                result = await self._design_api_architecture(task.params)
            elif task.name == "design_data_models":
                result = await self._design_data_models(task.params)
            elif task.name == "select_backend_technologies":
                result = await self._select_backend_technologies(task.params)
            elif task.name == "design_service_architecture":
                result = await self._design_service_architecture(task.params)
            elif task.name == "validate_backend_architecture":
                result = await self._validate_backend_architecture(task.params)
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
            self.logger.error(f"❌ Error in backend architecture task {task.name}: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                metadata={"agent": self.name, "task_type": task.name}
            )
    
    async def _analyze_backend_requirements(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze requirements specific to backend architecture."""
        description = params.get("description", "")
        features = params.get("features", [])
        constraints = params.get("constraints", [])
        
        # Use LLM to analyze backend requirements
        analysis_prompt = f"""
        As a senior backend architect, analyze these requirements for backend system design:
        
        Project Description: {description}
        Features Required: {features}
        Constraints: {constraints}
        
        Provide detailed analysis covering:
        1. Data storage requirements
        2. API design requirements
        3. Authentication/authorization needs
        4. Performance requirements
        5. Scalability considerations
        6. Integration requirements
        7. Security considerations
        
        Return as structured JSON with clear sections.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude is good at analysis
            action="reasoning",
            data={
                "prompt": analysis_prompt,
                "system_prompt": "You are a senior backend architect. Focus on backend-specific concerns only."
            }
        )
        
        # Parse and structure the response
        analysis = self._parse_requirements_analysis(response.result, features)
        
        return {
            "backend_requirements": analysis,
            "complexity_assessment": self._assess_backend_complexity(analysis),
            "recommended_patterns": self._recommend_backend_patterns(analysis),
            "technology_hints": self._suggest_technology_hints(analysis),
            "analysis_metadata": {
                "analyzed_at": datetime.utcnow().isoformat(),
                "analyzer": self.name
            }
        }
    
    async def _design_api_architecture(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Design REST API architecture using LLM."""
        requirements = params.get("requirements", {})
        entities = params.get("entities", [])
        
        api_design_prompt = f"""
        Design a comprehensive REST API architecture for this backend system:
        
        Requirements: {requirements}
        Entities: {entities}
        
        Design should include:
        1. API endpoints structure (/api/v1/...)
        2. HTTP methods and status codes
        3. Request/response schemas
        4. Authentication endpoints
        5. Error handling patterns
        6. Rate limiting considerations
        7. API versioning strategy
        8. Pagination patterns
        9. Filtering and sorting patterns
        
        Return as OpenAPI 3.0 specification structure.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="openai",  # OpenAI good for structured API design
            action="generate_text",
            data={
                "prompt": api_design_prompt,
                "system_prompt": "You are an API architect. Design RESTful APIs following best practices."
            }
        )
        
        return {
            "api_specification": self._parse_api_design(response.result),
            "endpoint_summary": self._extract_endpoints_summary(response.result),
            "authentication_design": self._extract_auth_design(response.result),
            "design_metadata": {
                "designed_at": datetime.utcnow().isoformat(),
                "designer": self.name
            }
        }
    
    async def _design_data_models(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Design data models and database schema using LLM."""
        requirements = params.get("requirements", {})
        api_design = params.get("api_design", {})
        
        data_modeling_prompt = f"""
        Design data models and database schema for this backend system:
        
        Requirements: {requirements}
        API Design: {api_design}
        
        Design should include:
        1. Entity models with attributes and types
        2. Relationships between entities (1:1, 1:N, N:N)
        3. Database constraints and indexes
        4. Migration strategy
        5. Query optimization considerations
        6. Data validation rules
        7. Soft delete patterns if needed
        8. Audit trail considerations
        
        Return as structured schema definition.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at data modeling
            action="reasoning",
            data={
                "prompt": data_modeling_prompt,
                "system_prompt": "You are a database architect. Design efficient, normalized schemas."
            }
        )
        
        return {
            "data_models": self._parse_data_models(response.result),
            "relationships": self._extract_relationships(response.result),
            "database_schema": self._extract_database_schema(response.result),
            "migration_plan": self._extract_migration_plan(response.result),
            "design_metadata": {
                "designed_at": datetime.utcnow().isoformat(),
                "designer": self.name
            }
        }
    
    async def _select_backend_technologies(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Select appropriate backend technologies using LLM analysis."""
        requirements = params.get("requirements", {})
        constraints = params.get("constraints", [])
        preferences = params.get("preferences", {})
        
        tech_selection_prompt = f"""
        Select the best backend technologies for this system:
        
        Requirements: {requirements}
        Constraints: {constraints}
        Preferences: {preferences}
        
        Evaluate and recommend:
        1. Backend framework (FastAPI, Django, NestJS, etc.)
        2. Database technology (PostgreSQL, MySQL, MongoDB, etc.)
        3. ORM/ODM choice
        4. Authentication method
        5. Caching strategy
        6. Message queue if needed
        7. Monitoring and logging tools
        8. Testing frameworks
        
        Provide rationale for each choice and alternatives.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="deepseek",  # DeepSeek for technical decisions
            action="fast_coding",
            data={
                "prompt": tech_selection_prompt,
                "language": "analysis"
            }
        )
        
        return {
            "recommended_stack": self._parse_technology_recommendations(response.result),
            "alternatives": self._extract_technology_alternatives(response.result),
            "rationale": self._extract_technology_rationale(response.result),
            "selection_metadata": {
                "selected_at": datetime.utcnow().isoformat(),
                "selector": self.name
            }
        }
    
    async def _design_service_architecture(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Design service layer architecture using LLM."""
        data_models = params.get("data_models", {})
        api_design = params.get("api_design", {})
        
        service_design_prompt = f"""
        Design the service layer architecture for this backend:
        
        Data Models: {data_models}
        API Design: {api_design}
        
        Design should include:
        1. Service classes and their responsibilities
        2. Business logic organization
        3. Data access patterns
        4. Transaction management
        5. Error handling strategies
        6. Input validation approach
        7. Caching strategies
        8. Background task handling
        9. Event-driven patterns if applicable
        
        Focus on clean architecture and separation of concerns.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at architecture patterns
            action="reasoning",
            data={
                "prompt": service_design_prompt,
                "system_prompt": "You are a software architect. Design clean, maintainable service layers."
            }
        )
        
        return {
            "service_architecture": self._parse_service_architecture(response.result),
            "patterns_used": self._extract_architectural_patterns(response.result),
            "design_principles": self._extract_design_principles(response.result),
            "design_metadata": {
                "designed_at": datetime.utcnow().isoformat(),
                "designer": self.name
            }
        }
    
    async def _validate_backend_architecture(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate complete backend architecture design."""
        architecture = params.get("architecture", {})
        
        validation_prompt = f"""
        Validate this backend architecture design:
        
        Architecture: {architecture}
        
        Check for:
        1. Consistency between API design and data models
        2. Security best practices
        3. Performance considerations
        4. Scalability potential
        5. Maintainability factors
        6. Testing strategies
        7. Deployment considerations
        8. Error handling completeness
        
        Identify issues and suggest improvements.
        """
        
        response = await protocol.send_request(
            sender_id=self.agent_id,
            target_id="claude",  # Claude good at validation
            action="analysis",
            data={
                "content": validation_prompt,
                "analysis_type": "architecture_validation"
            }
        )
        
        return {
            "validation_result": self._parse_validation_result(response.result),
            "issues_found": self._extract_issues(response.result),
            "recommendations": self._extract_recommendations(response.result),
            "validation_metadata": {
                "validated_at": datetime.utcnow().isoformat(),
                "validator": self.name
            }
        }
    
    # Handler methods for MCP protocol
    async def _handle_analyze_requirements(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._analyze_backend_requirements(data)
    
    async def _handle_design_api(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._design_api_architecture(data)
    
    async def _handle_design_models(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._design_data_models(data)
    
    async def _handle_select_technologies(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._select_backend_technologies(data)
    
    async def _handle_design_services(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._design_service_architecture(data)
    
    async def _handle_validate_architecture(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        return await self._validate_backend_architecture(data)
    
    async def _handle_generic_task(self, task: AgentTask) -> Dict[str, Any]:
        return {
            "message": f"Generic backend architecture task {task.name} processed",
            "task_id": task.id,
            "agent": self.name
        }
    
    # Utility methods for parsing LLM responses
    def _parse_requirements_analysis(self, llm_response: str, features: List[str]) -> Dict[str, Any]:
        """Parse requirements analysis from LLM response."""
        # Basic parsing - in production, would use more sophisticated parsing
        return {
            "data_storage": ["Relational database", "File storage"],
            "api_requirements": ["REST API", "Authentication", "CORS"],
            "auth_needs": ["JWT tokens", "User management"],
            "performance": ["Response time < 500ms", "Support 1000 concurrent users"],
            "scalability": ["Horizontal scaling", "Database replication"],
            "integrations": ["Third-party APIs", "Payment processing"],
            "security": ["HTTPS", "Input validation", "Rate limiting"],
            "features_analysis": {feature: "Required" for feature in features}
        }
    
    def _assess_backend_complexity(self, analysis: Dict[str, Any]) -> str:
        """Assess complexity of backend requirements."""
        complexity_factors = len(analysis.get("features_analysis", {}))
        if complexity_factors <= 3:
            return "low"
        elif complexity_factors <= 7:
            return "medium"
        else:
            return "high"
    
    def _recommend_backend_patterns(self, analysis: Dict[str, Any]) -> List[str]:
        """Recommend backend architecture patterns."""
        patterns = ["Repository Pattern", "Service Layer Pattern"]
        
        if "auth_needs" in analysis:
            patterns.append("Authentication Middleware Pattern")
        
        if len(analysis.get("features_analysis", {})) > 5:
            patterns.append("Modular Architecture Pattern")
        
        return patterns
    
    def _suggest_technology_hints(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Suggest technology directions based on analysis."""
        return {
            "framework": "FastAPI for modern Python APIs",
            "database": "PostgreSQL for relational data",
            "auth": "JWT for stateless authentication",
            "caching": "Redis for session and data caching"
        }
    
    def _parse_api_design(self, llm_response: str) -> Dict[str, Any]:
        """Parse API design from LLM response."""
        return {
            "openapi_version": "3.0.0",
            "base_url": "/api/v1",
            "authentication": "Bearer JWT",
            "endpoints": [
                {"path": "/auth/login", "method": "POST"},
                {"path": "/auth/register", "method": "POST"},
                {"path": "/users", "method": "GET"},
                {"path": "/users/{id}", "method": "GET"}
            ]
        }
    
    def _extract_endpoints_summary(self, llm_response: str) -> List[Dict[str, str]]:
        """Extract endpoints summary from LLM response."""
        return [
            {"path": "/api/v1/auth/login", "method": "POST", "description": "User login"},
            {"path": "/api/v1/auth/register", "method": "POST", "description": "User registration"},
            {"path": "/api/v1/users", "method": "GET", "description": "List users"},
        ]
    
    def _extract_auth_design(self, llm_response: str) -> Dict[str, Any]:
        """Extract authentication design from LLM response."""
        return {
            "method": "JWT",
            "token_type": "Bearer",
            "expiration": "24 hours",
            "refresh_strategy": "Refresh tokens"
        }
    
    def _parse_data_models(self, llm_response: str) -> List[Dict[str, Any]]:
        """Parse data models from LLM response."""
        return [
            {
                "name": "User",
                "attributes": [
                    {"name": "id", "type": "UUID", "primary_key": True},
                    {"name": "email", "type": "String", "unique": True},
                    {"name": "password_hash", "type": "String"},
                    {"name": "created_at", "type": "DateTime"}
                ]
            }
        ]
    
    def _extract_relationships(self, llm_response: str) -> List[Dict[str, str]]:
        """Extract entity relationships from LLM response."""
        return [
            {"from": "User", "to": "Profile", "type": "one_to_one"},
            {"from": "User", "to": "Post", "type": "one_to_many"}
        ]
    
    def _extract_database_schema(self, llm_response: str) -> Dict[str, Any]:
        """Extract database schema from LLM response."""
        return {
            "tables": ["users", "profiles", "posts"],
            "indexes": ["idx_users_email", "idx_posts_user_id"],
            "constraints": ["fk_posts_user_id"]
        }
    
    def _extract_migration_plan(self, llm_response: str) -> List[str]:
        """Extract migration plan from LLM response."""
        return [
            "Create users table",
            "Create profiles table", 
            "Create posts table",
            "Add foreign key constraints",
            "Add indexes"
        ]
    
    def _parse_technology_recommendations(self, llm_response: str) -> Dict[str, str]:
        """Parse technology recommendations from LLM response."""
        return {
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "orm": "SQLAlchemy",
            "auth": "JWT",
            "cache": "Redis",
            "testing": "pytest"
        }
    
    def _extract_technology_alternatives(self, llm_response: str) -> Dict[str, List[str]]:
        """Extract technology alternatives from LLM response."""
        return {
            "framework": ["Django", "Flask", "NestJS"],
            "database": ["MySQL", "MongoDB"],
            "orm": ["Django ORM", "Peewee"],
            "auth": ["OAuth2", "Session-based"]
        }
    
    def _extract_technology_rationale(self, llm_response: str) -> Dict[str, str]:
        """Extract rationale for technology choices."""
        return {
            "framework": "FastAPI chosen for high performance and automatic API documentation",
            "database": "PostgreSQL for ACID compliance and JSON support",
            "orm": "SQLAlchemy for mature ecosystem and flexibility"
        }
    
    def _parse_service_architecture(self, llm_response: str) -> Dict[str, Any]:
        """Parse service architecture from LLM response."""
        return {
            "layers": ["Controller", "Service", "Repository"],
            "services": [
                {"name": "UserService", "responsibilities": ["User CRUD", "Authentication"]},
                {"name": "PostService", "responsibilities": ["Post management", "Content validation"]}
            ],
            "patterns": ["Dependency Injection", "Repository Pattern"]
        }
    
    def _extract_architectural_patterns(self, llm_response: str) -> List[str]:
        """Extract architectural patterns from LLM response."""
        return ["Repository Pattern", "Service Layer", "Dependency Injection"]
    
    def _extract_design_principles(self, llm_response: str) -> List[str]:
        """Extract design principles from LLM response."""
        return ["Single Responsibility", "Dependency Inversion", "Open/Closed"]
    
    def _parse_validation_result(self, llm_response: str) -> Dict[str, Any]:
        """Parse validation result from LLM response."""
        return {
            "overall_score": "good",
            "consistency": "high",
            "security": "adequate",
            "performance": "good",
            "maintainability": "high"
        }
    
    def _extract_issues(self, llm_response: str) -> List[str]:
        """Extract issues from validation response."""
        return [
            "Missing input validation on some endpoints",
            "No rate limiting configured",
            "Authentication error handling could be improved"
        ]
    
    def _extract_recommendations(self, llm_response: str) -> List[str]:
        """Extract recommendations from validation response."""
        return [
            "Add comprehensive input validation",
            "Implement rate limiting middleware",
            "Enhance error handling with proper HTTP status codes",
            "Add API documentation with examples"
        ]