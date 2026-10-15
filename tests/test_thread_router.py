"""Focused tests for message isolation, cancellation, and reply matching."""
import unittest
from app.conversation.thread_router import ConversationRouter

class RouterTests(unittest.TestCase):
    def setUp(self): self.router = ConversationRouter()
    def test_separate_threads(self):
        a = self.router.send("family", "tabitha", "bishad", "Hello")
        b = self.router.send("private", "hana", "marama", "Hi")
        self.assertEqual(self.router.request_reply(a).history, (a,))
        self.assertEqual(self.router.request_reply(b).history, (b,))
    def test_interruption_invalidates_reply(self):
        a = self.router.send("family", "tabitha", "bishad", "Hello")
        request = self.router.request_reply(a)
        self.router.interrupt("family")
        self.assertIsNone(self.router.accept_reply(request, "late reply"))
    def test_new_message_invalidates_old_reply(self):
        a = self.router.send("family", "tabitha", "bishad", "Hello")
        request = self.router.request_reply(a)
        self.router.send("family", "tabitha", "bishad", "Actually wait")
        self.assertIsNone(self.router.accept_reply(request, "stale"))
    def test_reply_cannot_repeat(self):
        a = self.router.send("family", "tabitha", "bishad", "Hello")
        request = self.router.request_reply(a)
        reply = self.router.accept_reply(request, "Hi!")
        self.assertEqual(reply.reply_to_id, a.id)
        self.assertIsNone(self.router.accept_reply(request, "again"))
    def test_old_message_cannot_request_reply(self):
        a = self.router.send("family", "tabitha", "bishad", "Hello")
        self.router.send("family", "tabitha", "bishad", "Next")
        with self.assertRaises(ValueError): self.router.request_reply(a)

if __name__ == "__main__": unittest.main()
