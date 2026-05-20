
from sqlalchemy.orm import Mapped, mapped_column
from database.entity.BaseModel import BaseModel
from typing import Optional
from sqlalchemy import TIMESTAMP,BIGINT,VARCHAR,TEXT,INTEGER,UUID
import uuid,datetime



class PlatformTokenLogModel(BaseModel):
    __tablename__ = 'platform_token_log'
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    action: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    amount: Mapped[Optional[int]] = mapped_column(INTEGER)
    meta_data: Mapped[Optional[str]] = mapped_column(TEXT)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID)
