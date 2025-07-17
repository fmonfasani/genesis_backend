from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional
import logging


@dataclass
class AgentTask:
    id: str
    name: str
    params: Dict[str, Any]


@dataclass
class TaskResult:
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class GenesisAgent:
    def __init__(self, agent_id: str, name: str, agent_type: str) -> None:
        self.agent_id = agent_id
        self.name = name
        self.agent_type = agent_type
        self.capabilities: list[str] = []
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_capability(self, capability: str) -> None:
        self.capabilities.append(capability)

    def register_handler(self, action: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._handlers[action] = handler

    async def execute_task(self, task: AgentTask) -> TaskResult:
        handler = self._handlers.get(task.name)
        if handler:
            try:
                result = await handler(task.params)
                return TaskResult(task_id=task.id, success=True, result=result, metadata={"agent": self.name, "task_type": task.name})
            except Exception as exc:
                return TaskResult(task_id=task.id, success=False, error=str(exc), metadata={"agent": self.name, "task_type": task.name})
        return TaskResult(task_id=task.id, success=True, result={"message": f"Generic {self.agent_type} task {task.name} processed"}, metadata={"agent": self.name, "task_type": task.name})
