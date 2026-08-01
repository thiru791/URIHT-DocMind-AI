from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    filepath = Column(String)

    characters = Column(Integer)