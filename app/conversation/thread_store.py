"""In-memory thread state; persistence is deliberately separate."""
from dataclasses import dataclass, field
from .messages import Message

@dataclass
class ThreadState:
    messages: list[Message] = field(default_factory=list)
    revision: int = 0
    generation: int = 0

class ThreadStore:
    def __init__(self):
        self._threads: dict[str, ThreadState] = {}

    def get(self, thread_id: str) -> ThreadState:
        if not thread_id:
            raise ValueError("thread_id is required")
        return self._threads.setdefault(thread_id, ThreadState())
