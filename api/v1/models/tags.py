from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db.database import Base

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    tasks = relationship("TaskTag", backref="tag", cascade="all, delete")