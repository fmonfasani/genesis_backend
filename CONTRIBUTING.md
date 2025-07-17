# Contributing to Genesis Backend

Welcome to Genesis Backend! We're excited to have you contribute to our backend code generation system. This guide will help you get started with contributing to the project.

## 🎯 Overview

Genesis Backend is a specialized module of the Genesis Engine ecosystem that focuses on backend code generation using AI agents. Your contributions help make backend development faster, more consistent, and more intelligent.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of backend frameworks (FastAPI, Django, NestJS)
- Familiarity with LLMs and AI agents (helpful but not required)

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/your-username/genesis-backend.git
   cd genesis-backend
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install in development mode
   make dev-setup
   ```

3. **Verify Installation**
   ```bash
   make test
   ```

## 🏗️ Project Structure

Understanding the project structure helps you navigate and contribute effectively:

```
genesis-backend/
├── src/genesis_backend/          # Main package
│   ├── __init__.py              # Package exports
│   ├── config.py                # Configuration classes
│   ├── agents/                  # AI agents for code generation
│   │   ├── architect.py         # Architecture design agent
│   │   ├── fastapi_agent.py     # FastAPI generation agent
│   │   ├── django_agent.py      # Django generation agent
│   │   ├── nestjs_agent.py      # NestJS generation agent
│   │   ├── database_agent.py    # Database design agent
│   │   └── auth_agent.py        # Authentication agent
│   └── generators/              # Code generators
│       ├── backend_generator.py # Main backend generator
│       ├── api_generator.py     # API generation utilities
│       ├── model_generator.py   # Model generation utilities
│       └── auth_generator.py    # Authentication generation
├── tests/                       # Test suite
├── examples/                    # Usage examples
└── docs/                        # Documentation
```

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **🐛 Bug Fixes** - Fix issues in existing code
2. **✨ New Features** - Add new backend frameworks, agents, or generators
3. **📚 Documentation** - Improve docs, examples, or docstrings
4. **🧪 Tests** - Add or improve test coverage
5. **🎨 Code Quality** - Refactoring, performance improvements
6. **🤖 Agent Improvements** - Enhance AI agent capabilities

### Contribution Workflow

1. **Check Existing Issues**
   - Look for existing issues or feature requests
   - Create a new issue if needed
   - Discuss your approach in the issue

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the coding standards (see below)
   - Write tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   make quality  # Run linting and type checking
   make test     # Run all tests
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Create a pull request on GitHub
   - Fill out the pull request template
   - Wait for review and address feedback

## 📋 Coding Standards

### Python Code Style

We follow strict coding standards to maintain code quality:

- **Formatting**: Use Black for code formatting
- **Import Sorting**: Use isort for import organization
- **Linting**: Use flake8 for linting
- **Type Hints**: Use mypy for static type checking

```bash
# Format code
make format

# Check code quality
make quality
```

### Code Quality Guidelines

1. **Type Hints**
   ```python
   def generate_backend(config: BackendConfig) -> Dict[str, Any]:
       """Generate backend with proper type hints."""
       pass
   ```

2. **Docstrings**
   ```python
   def create_agent(agent_type: str) -> GenesisAgent:
       """
       Create a specialized agent for backend generation.
       
       Args:
           agent_type: Type of agent to create (e.g., 'fastapi', 'django')
           
       Returns:
           Configured agent instance
           
       Raises:
           ValueError: If agent_type is not supported
       """
       pass
   ```

3. **Error Handling**
   ```python
   try:
       result = await agent.execute_task(task)
   except Exception as e:
       logger.error(f"Task execution failed: {e}")
       return TaskResult(success=False, error=str(e))
   ```

4. **Async/Await**
   ```python
   async def generate_code(prompt: str) -> str:
       """Use async/await for LLM interactions."""
       response = await protocol.send_request(...)
       return response.result
   ```

### Architecture Guidelines

Follow the Genesis Backend architecture principles:

1. **Agent Responsibilities**
   - Each agent has a specific, focused responsibility
   - Agents use LLMs for intelligent code generation
   - No direct user interaction in agents

2. **Generator Patterns**
   - Generators coordinate multiple agents
   - Framework-specific generation logic
   - Template engine integration

3. **Configuration Management**
   - Use dataclasses for configuration
   - Provide validation and defaults
   - Support serialization/deserialization

## 🧪 Testing Guidelines

We maintain high test coverage and quality:

### Test Types

1. **Unit Tests** - Test individual components
2. **Integration Tests** - Test component interactions
3. **Agent Tests** - Test agent functionality with mocked LLMs
4. **Generator Tests** - Test code generation workflows

### Writing Tests

```python
import pytest
from unittest.mock import AsyncMock, patch

class TestFastAPIAgent:
    @pytest.fixture
    def fastapi_agent(self):
        return FastAPIAgent()
    
    @pytest.mark.asyncio
    async def test_generate_app(self, fastapi_agent):
        with patch('mcpturbo.protocol.send_request') as mock_protocol:
            mock_protocol.return_value = AsyncMock()
            mock_protocol.return_value.result = "Generated FastAPI code"
            
            task = AgentTask(name="generate_fastapi_app", params={})
            result = await fastapi_agent.execute_task(task)
            
            assert result.success
            assert "main_application" in result.result
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration

# Run with coverage
make test-coverage

# Run fast tests only
make test-fast
```

## 🤖 Working with AI Agents

### Agent Development Guidelines

1. **Use MCPturbo Protocol**
   ```python
   response = await protocol.send_request(
       sender_id=self.agent_id,
       target_id="claude",
       action="code_generation",
       data={"prompt": prompt, "language": "python"}
   )
   ```

2. **Prompt Engineering**
   - Be specific about requirements
   - Provide context and examples
   - Request structured output
   - Include error handling instructions

3. **Response Parsing**
   ```python
   def _parse_llm_response(self, response: str) -> Dict[str, Any]:
       """Parse and structure LLM response."""
       # Implement robust parsing logic
       pass
   ```

### Adding New Agents

1. **Inherit from GenesisAgent**
   ```python
   from genesis_agents import GenesisAgent, AgentTask, TaskResult
   
   class CustomAgent(GenesisAgent):
       def __init__(self):
           super().__init__(
               agent_id="custom_agent",
               name="Custom Agent",
               agent_type="custom"
           )
   ```

2. **Implement Required Methods**
   ```python
   async def execute_task(self, task: AgentTask) -> TaskResult:
       # Implement task execution logic
       pass
   ```

3. **Register Capabilities**
   ```python
   self.add_capability("custom_generation")
   self.register_handler("custom_generation", self._handle_custom)
   ```

## 🔧 Adding New Framework Support

To add support for a new backend framework:

1. **Update Configuration**
   ```python
   # In config.py
   class BackendFramework(Enum):
       NEW_FRAMEWORK = "new_framework"
   ```

2. **Create Framework Agent**
   ```python
   # In agents/new_framework_agent.py
   class NewFrameworkAgent(GenesisAgent):
       # Implement framework-specific generation
       pass
   ```

3. **Update Generators**
   ```python
   # In generators/
   # Add framework-specific generation logic
   ```

4. **Add Tests**
   ```python
   # In tests/
   # Add comprehensive tests for new framework
   ```

5. **Update Documentation**
   - Update README.md
   - Add examples
   - Update ECOSYSTEM_DOCTRINE.md

## 📚 Documentation

### Documentation Types

1. **Code Documentation**
   - Comprehensive docstrings
   - Type hints
   - Inline comments for complex logic

2. **API Documentation**
   - Method signatures
   - Parameter descriptions
   - Return value descriptions
   - Usage examples

3. **User Documentation**
   - README updates
   - Example scripts
   - Tutorial content

### Writing Good Documentation

```python
def generate_backend(
    config: BackendConfig,
    architecture: Dict[str, Any],
    output_path: Path
) -> Dict[str, Any]:
    """
    Generate a complete backend application.
    
    This method orchestrates the generation of a backend application
    using specialized agents for different components.
    
    Args:
        config: Backend configuration specifying framework, database,
               authentication method, and other settings
        architecture: Architecture design including entities, relationships,
                     and API design from the architect agent
        output_path: Directory where generated files will be written
        
    Returns:
        Dictionary containing:
        - files: Dict mapping file paths to generated content
        - framework: Framework used for generation
        - metadata: Generation metadata including timestamp
        
    Raises:
        ValueError: If framework is not supported
        FileNotFoundError: If output path cannot be created
        
    Example:
        >>> config = BackendConfig(
        ...     project_name="my-api",
        ...     framework=BackendFramework.FASTAPI
        ... )
        >>> architecture = {"entities": [...]}
        >>> result = await generator.generate_backend(
        ...     config, architecture, Path("./output")
        ... )
        >>> print(f"Generated {len(result['files'])} files")
    """
```

## 🐛 Bug Reports

When reporting bugs:

1. **Use the Bug Report Template**
2. **Provide Detailed Information**
   - Genesis Backend version
   - Python version
   - Operating system
   - Full error traceback
   - Steps to reproduce

3. **Include Minimal Reproduction Case**
   ```python
   # Minimal code that reproduces the bug
   from genesis_backend import BackendConfig
   
   config = BackendConfig(project_name="test")
   # Bug occurs here...
   ```

## 💡 Feature Requests

When requesting features:

1. **Check Existing Issues** - Avoid duplicates
2. **Describe the Use Case** - Why is this needed?
3. **Propose Solution** - How should it work?
4. **Consider Alternatives** - Are there other approaches?

## 🏆 Recognition

Contributors are recognized in several ways:

- **Contributors file** - Listed in CONTRIBUTORS.md
- **Commit attribution** - Proper git attribution
- **Release notes** - Mentioned in significant releases
- **Community recognition** - Highlighted in community channels

## 🔒 Security

If you discover security vulnerabilities:

1. **Don't create public issues**
2. **Email security@genesis-engine.dev**
3. **Provide detailed information**
4. **Allow time for investigation**

## 📞 Getting Help

If you need help while contributing:

1. **Check Documentation** - README, docstrings, examples
2. **Search Issues** - Existing discussions
3. **Join Discussions** - GitHub Discussions
4. **Ask Questions** - Create issue with "question" label

## 🎉 Thank You!

Thank you for contributing to Genesis Backend! Your efforts help make backend development more efficient and enjoyable for developers worldwide.

## 📄 License

By contributing to Genesis Backend, you agree that your contributions will be licensed under the MIT License.

---

Happy coding! 🚀
