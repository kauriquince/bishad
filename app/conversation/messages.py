"""Typed message contracts, with thread-specific identity."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Message:
    id: str
    thread_id: str
    sender_id: str
    recipient_id: str
    text: str
    reply_to_id: str | None = None

@dataclass(frozen=True)
class ReplyRequest:
    request_id: str
    thread_id: str
    recipient_id: str
    reply_to_id: str
    revision: int
    generation: int
    history: tuple[Message, ...]
