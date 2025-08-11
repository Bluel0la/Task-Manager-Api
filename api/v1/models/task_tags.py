from sqlalchemy import Column, Integer, ForeignKey
from api.db.database import Base


class TaskTag(Base):
    __tablename__ = "task_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
