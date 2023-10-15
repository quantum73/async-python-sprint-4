from sqlalchemy import Boolean, Column, String, Integer, DateTime, func

from .base import Base


class ShortURL(Base):
    __tablename__ = "short_url"

    short_id = Column(String(length=64), primary_key=True, unique=True, index=True)
    short_url = Column(String(length=256))
    original_url = Column(String(length=2056))
    click_count = Column(Integer, default=0)
    last_click_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<ShortURL(id={self.short_id}, short_url={self.short_url}, original_url={self.original_url})>"
