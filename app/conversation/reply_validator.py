"""Ensure generated replies still match the latest message and thread."""
from .messages import ReplyRequest
from .thread_store import ThreadState

def is_current(request: ReplyRequest, thread: ThreadState) -> bool:
    return bool(
        thread.messages
        and request.revision == thread.revision
        and request.generation == thread.generation
        and request.thread_id == thread.messages[-1].thread_id
        and request.reply_to_id == thread.messages[-1].id
        and request.recipient_id == thread.messages[-1].recipient_id
    )
