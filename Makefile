# Genesis Backend - Development Makefile
# Provides convenient commands for development tasks

.PHONY: help install install-dev test test-unit test-integration test-coverage lint format type-check quality clean build publish docs examples

# Default target
help:
	@echo "Genesis Backend - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make install       - Install package dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run all tests"
	@echo "  make test-unit     - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          - Run linting (flake8)"
	@echo "  make format        - Format code (black + isort)"
	@echo "  make type-check    - Run type checking (mypy)"
	@echo "  make quality       - Run all quality checks"
	@echo ""
	@echo "Build & Release:"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make build         - Build package"
	@echo "  make publish       - Publish to PyPI"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs          - Generate documentation"
	@echo "  make examples      - Run example scripts"
	@echo ""
	@echo "Development:"
	@echo "  make dev-setup     - Complete development setup"
	@echo "  make pre-commit    - Run pre-commit checks"

# Installation
install:
	@echo "📦 Installing Genesis Backend..."
	pip install -e .

install-dev:
	@echo "🔧 Installing development dependencies..."
	pip install -e ".[dev,test]"
	pip install pre-commit
	pre-commit install

dev-setup: install-dev
	@echo "🚀 Development environment setup complete!"
	@echo "Run 'make test' to verify installation"

# Testing
test:
	@echo "🧪 Running all tests..."
	pytest tests/ -v

test-unit:
	@echo "🧪 Running unit tests..."
	pytest tests/test_config.py tests/test_agents.py tests/test_generators.py -v -m "not integration"

test-integration:
	@echo "🧪 Running integration tests..."
	pytest tests/test_integration.py -v -m "integration"

test-coverage:
	@echo "📊 Running tests with coverage..."
	pytest tests/ --cov=genesis_backend --cov-report=html --cov-report=term --cov-fail-under=80
	@echo "Coverage report generated in htmlcov/"

test-fast:
	@echo "⚡ Running fast tests only..."
	pytest tests/ -v -m "not slow"

# Code Quality
lint:
	@echo "🔍 Running linting..."
	flake8 src/ tests/ examples/
	@echo "✅ Linting passed"

format:
	@echo "🎨 Formatting code..."
	black src/ tests/ examples/
	isort src/ tests/ examples/
	@echo "✅ Code formatted"

type-check:
	@echo "🔍 Running type checking..."
	mypy src/genesis_backend/
	@echo "✅ Type checking passed"

quality: lint type-check
	@echo "✅ All quality checks passed"

pre-commit:
	@echo "🔍 Running pre-commit checks..."
	pre-commit run --all-files

# Build and Release
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf src/*.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned"

build: clean
	@echo "📦 Building package..."
	python -m build
	@echo "✅ Package built"

publish: build
	@echo "🚀 Publishing to PyPI..."
	python -m twine upload dist/*
	@echo "✅ Published"

publish-test: build
	@echo "🧪 Publishing to Test PyPI..."
	python -m twine upload --repository testpypi dist/*
	@echo "✅ Published to Test PyPI"

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "📖 API documentation available in README.md"
	@echo "📖 Doctrine documentation in ECOSYSTEM_DOCTRINE.md"

docs-serve:
	@echo "🌐 Starting documentation server..."
	python -m http.server 8000 -d docs/

# Examples
examples:
	@echo "🎯 Running basic usage example..."
	cd examples && python basic_usage.py

example-fastapi:
	@echo "⚡ Generating FastAPI example..."
	cd examples && python -c "
import asyncio
from basic_usage import main
asyncio.run(main())
"

example-django:
	@echo "🟢 Generating Django example..."
	@echo "Django example generation (simulated)"

example-nestjs:
	@echo "🟦 Generating NestJS example..."
	@echo "NestJS example generation (simulated)"

# Development Utilities
check-deps:
	@echo "🔍 Checking dependencies..."
	pip check
	pip list --outdated

update-deps:
	@echo "⬆️ Updating dependencies..."
	pip install --upgrade pip setuptools wheel
	pip install --upgrade -e ".[dev,test]"

security-check:
	@echo "🔒 Running security checks..."
	pip install safety bandit
	safety check
	bandit -r src/

benchmark:
	@echo "⚡ Running benchmarks..."
	cd tests && python -m pytest test_integration.py::TestPerformanceIntegration -v

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t genesis-backend:latest .

docker-test:
	@echo "🐳 Running tests in Docker..."
	docker run --rm genesis-backend:latest make test

# Git hooks and versioning
version-patch:
	@echo "📈 Bumping patch version..."
	@echo "Current version: $(shell grep version pyproject.toml | head -1 | cut -d'"' -f2)"
	@echo "Please update version manually in pyproject.toml"

version-minor:
	@echo "📈 Bumping minor version..."
	@echo "Current version: $(shell grep version pyproject.toml | head -1 | cut -d'"' -f2)"
	@echo "Please update version manually in pyproject.toml"

version-major:
	@echo "📈 Bumping major version..."
	@echo "Current version: $(shell grep version pyproject.toml | head -1 | cut -d'"' -f2)"
	@echo "Please update version manually in pyproject.toml"

# Release workflow
release-check: clean quality test
	@echo "✅ Release checks passed"

release-patch: release-check version-patch build
	@echo "🚀 Patch release ready"

release-minor: release-check version-minor build
	@echo "🚀 Minor release ready"

release-major: release-check version-major build
	@echo "🚀 Major release ready"

# Environment info
info:
	@echo "🔍 Environment Information:"
	@echo "Python: $(shell python --version)"
	@echo "Pip: $(shell pip --version)"
	@echo "OS: $(shell uname -s)"
	@echo "PWD: $(shell pwd)"
	@echo ""
	@echo "📦 Genesis Backend:"
	@echo "Version: $(shell grep version pyproject.toml | head -1 | cut -d'"' -f2)"
	@echo ""
	@echo "Dependencies:"
	@pip list | grep -E "(genesis|mcpturbo|pydantic|jinja2)"

# Database for testing
test-db-start:
	@echo "🗄️ Starting test database..."
	docker run -d --name genesis-test-db \
		-e POSTGRES_DB=genesis_test \
		-e POSTGRES_USER=test \
		-e POSTGRES_PASSWORD=test \
		-p 5433:5432 \
		postgres:13

test-db-stop:
	@echo "🗄️ Stopping test database..."
	docker stop genesis-test-db || true
	docker rm genesis-test-db || true

# Development workflow
dev-cycle: format lint type-check test
	@echo "🔄 Development cycle complete!"

ci-check: quality test-coverage
	@echo "✅ CI checks passed"

# Troubleshooting
troubleshoot:
	@echo "🔧 Troubleshooting Genesis Backend..."
	@echo ""
	@echo "1. Check Python version (>=3.9):"
	@python --version
	@echo ""
	@echo "2. Check dependencies:"
	@pip check || echo "❌ Dependency conflicts found"
	@echo ""
	@echo "3. Check imports:"
	@python -c "import genesis_backend; print('✅ Genesis Backend imports OK')" || echo "❌ Import failed"
	@echo ""
	@echo "4. Check MCPturbo:"
	@python -c "import mcpturbo; print('✅ MCPturbo available')" || echo "❌ MCPturbo not found"
	@echo ""
	@echo "5. Check genesis-agents:"
	@python -c "import genesis_agents; print('✅ Genesis Agents available')" || echo "❌ Genesis Agents not found"

# Quick commands for daily development
quick-test: test-unit
	@echo "⚡ Quick test cycle complete"

quick-check: format lint
	@echo "⚡ Quick quality check complete"

# Performance monitoring
perf-test:
	@echo "⚡ Running performance tests..."
	pytest tests/test_integration.py::TestPerformanceIntegration -v --durations=10

memory-test:
	@echo "🧠 Running memory tests..."
	python -m pytest tests/ --memray

# Code analysis
complexity:
	@echo "🔍 Analyzing code complexity..."
	radon cc src/ -s

lines:
	@echo "📏 Counting lines of code..."
	find src/ -name "*.py" | xargs wc -l

# Generate project statistics
stats:
	@echo "📊 Genesis Backend Statistics:"
	@echo ""
	@echo "📁 Project structure:"
	@find src/ -name "*.py" | head -10
	@echo ""
	@echo "📏 Lines of code:"
	@find src/ -name "*.py" | xargs wc -l | tail -1
	@echo ""
	@echo "🧪 Test coverage:"
	@pytest tests/ --cov=genesis_backend --cov-report=term-missing | tail -1 || echo "Run 'make test-coverage' first"
	@echo ""
	@echo "📦 Package size:"
	@du -sh src/ 2>/dev/null || echo "N/A"

# Help for specific topics
help-testing:
	@echo "🧪 Testing Help:"
	@echo ""
	@echo "Available test commands:"
	@echo "  make test          - Run all tests"
	@echo "  make test-unit     - Unit tests only"
	@echo "  make test-integration - Integration tests only"
	@echo "  make test-coverage - Tests with coverage"
	@echo "  make test-fast     - Skip slow tests"
	@echo ""
	@echo "Test markers:"
	@echo "  @pytest.mark.unit - Unit tests"
	@echo "  @pytest.mark.integration - Integration tests"
	@echo "  @pytest.mark.slow - Slow tests"

help-quality:
	@echo "✨ Code Quality Help:"
	@echo ""
	@echo "Quality commands:"
	@echo "  make format        - Format with black + isort"
	@echo "  make lint          - Lint with flake8"
	@echo "  make type-check    - Check types with mypy"
	@echo "  make quality       - Run all quality checks"
	@echo ""
	@echo "Configuration files:"
	@echo "  pyproject.toml     - Black, isort, mypy config"
	@echo "  .flake8           - Flake8 configuration"

help-release:
	@echo "🚀 Release Help:"
	@echo ""
	@echo "Release workflow:"
	@echo "  1. make release-check  - Verify ready for release"
	@echo "  2. Update version in pyproject.toml"
	@echo "  3. make build          - Build package"
	@echo "  4. make publish-test   - Publish to Test PyPI"
	@echo "  5. make publish        - Publish to PyPI"
	@echo ""
	@echo "Version bumping:"
	@echo "  Edit pyproject.toml manually"
	@echo "  Follow semantic versioning"
