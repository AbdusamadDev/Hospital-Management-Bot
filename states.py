from aiogram.dispatcher.filters.state import State, StatesGroup


class UserId(StatesGroup):
    user_id = State()

class GroupId(StatesGroup):
    chat_id = State()

class BlogPost(StatesGroup):
    post = State()

class ClientMassageRequest(StatesGroup):
    cover_letter = State()

class ClientFeedbackRequest(StatesGroup):
    feedback = State()

class DeletePost(StatesGroup):
    delete = State()

class ClearFeedbackModel(StatesGroup):
    clear = State()

class ClearQueueModel(StatesGroup):
    clear = State()
