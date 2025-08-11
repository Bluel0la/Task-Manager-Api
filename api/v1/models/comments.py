from sqlalchemy import Column, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from api.db.database import Base
from datetime import datetime


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task = relationship("Task", backref="comments")
    user = relationship("User", backref="comments")
