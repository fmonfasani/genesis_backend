from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class BackendFramework(str, Enum):
    """Supported backend frameworks."""

    FASTAPI = "fastapi"
    DJANGO = "django"
    NESTJS = "nestjs"
    EXPRESS = "express"


class DatabaseType(str, Enum):
    """Supported database engines."""

    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"


class ORMType(str, Enum):
    """Supported ORMs."""

    SQLALCHEMY = "sqlalchemy"
    DJANGO_ORM = "django_orm"
    TYPEORM = "typeorm"
    PRISMA = "prisma"
    MONGOOSE = "mongoose"


class AuthMethod(str, Enum):
    """Authentication methods."""

    JWT = "jwt"
    OAUTH2 = "oauth2"
    SESSION = "session"
    SOCIAL = "social"


@dataclass
class DatabaseConfig:
    """Database connection configuration."""

    type: DatabaseType
    host: Optional[str] = None
    port: Optional[int] = None
    name: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    orm: Optional[ORMType] = None

    @property
    def connection_url(self) -> str:
        """Return connection URL based on settings."""

        if self.type == DatabaseType.SQLITE:
            return f"sqlite:///{self.name}" if self.name else "sqlite:///"

        cred = ""
        if self.user:
            cred = self.user
            if self.password:
                cred += f":{self.password}"
            cred += "@"

        host = self.host or "localhost"
        port = f":{self.port}" if self.port else ""
        name = f"/{self.name}" if self.name else ""
        return f"{self.type.value}://{cred}{host}{port}{name}"

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "type": self.type.value,
            "host": self.host,
            "port": self.port,
            "name": self.name,
            "user": self.user,
            "password": self.password,
            "orm": self.orm.value if self.orm else None,
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatabaseConfig":
        if not data:
            raise ValueError("DatabaseConfig data required")

        db_type = data.get("type")
        if isinstance(db_type, str):
            data["type"] = DatabaseType(db_type)
        orm = data.get("orm")
        if isinstance(orm, str):
            data["orm"] = ORMType(orm)
        return cls(**data)


@dataclass
class AuthConfig:
    """Authentication configuration."""

    method: AuthMethod
    secret_key: Optional[str] = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    oauth_providers: List[str] = field(default_factory=list)
    session_timeout: Optional[int] = None
    cookie_secure: bool = False
    cookie_httponly: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": self.method.value,
            "secret_key": self.secret_key,
            "algorithm": self.algorithm,
            "access_token_expire_minutes": self.access_token_expire_minutes,
            "refresh_token_expire_days": self.refresh_token_expire_days,
            "oauth_providers": self.oauth_providers or None,
            "session_timeout": self.session_timeout,
            "cookie_secure": self.cookie_secure,
            "cookie_httponly": self.cookie_httponly,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuthConfig":
        if not data:
            raise ValueError("AuthConfig data required")
        method = data.get("method")
        if isinstance(method, str):
            data["method"] = AuthMethod(method)
        return cls(**data)


@dataclass
class BackendConfig:
    """Main backend configuration container."""

    project_name: str
    description: str = ""
    framework: BackendFramework = BackendFramework.FASTAPI
    version: str = "0.1.0"
    debug: bool = False
    features: List[str] = field(default_factory=list)
    api_version: str = "v1"
    cors_origins: List[str] = field(default_factory=list)
    database: Optional[DatabaseConfig] = None
    auth: Optional[AuthConfig] = None

    def __post_init__(self) -> None:
        if not self.project_name:
            raise ValueError("project_name is required")

        if isinstance(self.framework, str):
            self.framework = BackendFramework(self.framework)

        if self.database is not None and not isinstance(self.database, DatabaseConfig):
            self.database = DatabaseConfig.from_dict(self.database)  # type: ignore[arg-type]

        if self.auth is not None and not isinstance(self.auth, AuthConfig):
            self.auth = AuthConfig.from_dict(self.auth)  # type: ignore[arg-type]

    @property
    def language(self) -> str:
        mapping = {
            BackendFramework.FASTAPI: "python",
            BackendFramework.DJANGO: "python",
            BackendFramework.NESTJS: "typescript",
            BackendFramework.EXPRESS: "javascript",
        }
        return mapping.get(self.framework, "python")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "description": self.description,
            "framework": self.framework.value,
            "version": self.version,
            "debug": self.debug,
            "features": list(self.features),
            "api_version": self.api_version,
            "cors_origins": list(self.cors_origins),
            "database": self.database.to_dict() if self.database else None,
            "auth": self.auth.to_dict() if self.auth else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BackendConfig":
        if not data:
            raise ValueError("BackendConfig data required")

        data = dict(data)
        if "framework" in data and isinstance(data["framework"], str):
            data["framework"] = BackendFramework(data["framework"])
        if "database" in data and data["database"] is not None:
            if isinstance(data["database"], DatabaseConfig):
                pass
            else:
                data["database"] = DatabaseConfig.from_dict(data["database"])
        if "auth" in data and data["auth"] is not None:
            if isinstance(data["auth"], AuthConfig):
                pass
            else:
                data["auth"] = AuthConfig.from_dict(data["auth"])
        return cls(**data)
