from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, DateTime
from api.v1.models.model_enums import TaskPriority, TaskStatus
from sqlalchemy.orm import relationship
from api.db.database import Base
from datetime import datetime


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", backref="tasks")
    assignments = relationship("TaskAssignment", backref="task", cascade="all, delete")
    tags = relationship("TaskTag", backref="task", cascade="all, delete")
