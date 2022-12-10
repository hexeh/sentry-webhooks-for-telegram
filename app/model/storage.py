from sqlalchemy import Column, DateTime, Integer, String

from app.adapters import STORAGE


class ChatMapping(STORAGE.base):
    __tablename__ = "chat_map"
    # todo: update model to allow m2m project-chat
    project_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    project_name = Column(String, nullable=True)
    last_webhook = Column(DateTime, nullable=True)
