from api.v1.schemas.projectSchema import ProjectCreate, ProjectResponse
from fastapi import APIRouter, HTTPException, Depends, status
from api.utils.firebase import create_project, get_project_by_id, get_project_by_name, get_all_projects
from api.utils.authentication import get_current_user

projects = APIRouter(prefix="/project", tags=["project"])

@projects.post("/create", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_new_project(project: ProjectCreate, current_user: dict = Depends(get_current_user)):
    """
    Create a new project.
    """
    existing_project = get_project_by_name(project.name)
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A Project with this name already exists."
        )
    
    new_project = create_project(project, owner_username=current_user["username"])
    if not new_project:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project."
        )
    
    return new_project

@projects.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
        
    return project

@projects.get("/all", response_model=list[ProjectResponse])
def fetch_all_projects(current_user: dict = Depends(get_current_user)):
    projects = get_all_projects()
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No projects found."
        )
        
    return projects
    
    