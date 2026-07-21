import asyncio
import unittest
from types import SimpleNamespace

from app.bot.handlers import plan


class DummyMessage:
    def __init__(self):
        self.edited = None

    async def edit_text(self, text, reply_markup=None):
        self.edited = (text, reply_markup)


class DummyCallback:
    def __init__(self):
        self.message = DummyMessage()
        self.from_user = SimpleNamespace(id=42)
        self.answered = False

    async def answer(self):
        self.answered = True


class DummyService:
    def __init__(self):
        self.users = []

    async def ensure_user(self, user_id):
        self.users.append(user_id)


class PlanHandlerTests(unittest.TestCase):
    def test_handle_start_shows_plan_keyboard(self):
        callback = DummyCallback()
        service = DummyService()

        async def run_test():
            await plan.handle_start(callback, None, service)

        asyncio.run(run_test())

        self.assertEqual(service.users, [42])
        self.assertEqual(callback.message.edited[0], "Выбери план тренировок:")
        self.assertIsNotNone(callback.message.edited[1])


if __name__ == "__main__":
    unittest.main()
