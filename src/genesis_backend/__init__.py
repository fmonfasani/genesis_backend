"""
Genesis Backend - Backend Code Generation Agents

Specialized agents for generating backend code using LLMs.
Part of the Genesis Engine ecosystem.
"""

__version__ = "1.0.0"
__author__ = "Genesis Engine Team"

# Import main agent classes
from .agents import (
    ArchitectAgent,
    FastAPIAgent,
    DjangoAgent,
    NestJSAgent,
    DatabaseAgent,
    AuthAgent,
)

# Import utilities
from .generators import (
    BackendGenerator,
    APIGenerator,
    ModelGenerator,
    AuthGenerator,
)

# Import configuration classes
from .config import (
    BackendConfig,
    BackendFramework,
    DatabaseType,
    AuthMethod,
)

# Export agents for auto-discovery by genesis-core
def get_agents():
    """
    Return list of agent classes for auto-discovery.
    Used by genesis-core for agent registration.
    """
    return [
        ArchitectAgent,
        FastAPIAgent,
        DjangoAgent,
        NestJSAgent,
        DatabaseAgent,
        AuthAgent,
    ]

# Main exports
__all__ = [
    # Agents
    "ArchitectAgent",
    "FastAPIAgent", 
    "DjangoAgent",
    "NestJSAgent",
    "DatabaseAgent",
    "AuthAgent",
    
    # Generators
    "BackendGenerator",
    "APIGenerator",
    "ModelGenerator",
    "AuthGenerator",
    
    # Configuration
    "BackendConfig",
    "BackendFramework",
    "DatabaseType",
    "AuthMethod",
    
    # Discovery function
    "get_agents",
    
    # Metadata
    "__version__",
    "__author__",
]