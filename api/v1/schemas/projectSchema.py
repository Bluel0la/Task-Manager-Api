from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    # No owner_id — we inject owner_username in the endpoint from the current user
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: str  # Firestore doc IDs are strings
    owner_username: str
    created_at: datetime
