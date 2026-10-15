"""Route new messages and accept only correctly correlated replies."""
from uuid import uuid4
from .messages import Message, ReplyRequest
from .thread_store import ThreadStore
from .reply_validator import is_current

class ConversationRouter:
    def __init__(self, store=None):
        self.store = store or ThreadStore()

    def send(self, thread_id: str, sender_id: str, recipient_id: str, text: str) -> Message:
        if not all((thread_id, sender_id, recipient_id, text.strip())):
            raise ValueError("thread, sender, recipient and nonempty text required")
        thread = self.store.get(thread_id)
        message = Message(str(uuid4()), thread_id, sender_id, recipient_id, text)
        thread.messages.append(message)
        thread.revision += 1
        thread.generation += 1
        return message

    def request_reply(self, message: Message) -> ReplyRequest:
        thread = self.store.get(message.thread_id)
        if not thread.messages or thread.messages[-1].id != message.id:
            raise ValueError("Only the latest message can request a reply")
        return ReplyRequest(str(uuid4()), message.thread_id, message.recipient_id, message.id,
                            thread.revision, thread.generation, tuple(thread.messages))

    def accept_reply(self, request: ReplyRequest, text: str) -> Message | None:
        thread = self.store.get(request.thread_id)
        if not text.strip() or not is_current(request, thread):
            return None
        original = thread.messages[-1]
        reply = Message(str(uuid4()), request.thread_id, request.recipient_id,
                        original.sender_id, text, reply_to_id=request.reply_to_id)
        thread.messages.append(reply)
        thread.revision += 1
        thread.generation += 1
        return reply

    def interrupt(self, thread_id: str):
        self.store.get(thread_id).generation += 1
