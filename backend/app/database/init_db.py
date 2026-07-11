from app.database.database import engine
from app.database.base import Base

# Import models
from app.models.user import User
from app.models.document import Document
from app.models.chat import Chat


def init_db():
    Base.metadata.create_all(bind=engine)