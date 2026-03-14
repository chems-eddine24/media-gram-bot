from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from sqlalchemy import DateTime as datetime

Base = declarative_base()


class Download:
    __tablename__ = "downloads"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    telegram_id = Column(String, unique=True, nullable=False)
    platfrom = Column(String, nullable=False)
    media_type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    download_at = Column(datetime(timezone=True), nullable=False)
