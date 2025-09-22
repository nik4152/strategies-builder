from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class Workflow(BaseModel):
    id: UUID | None = None
    name: str
    json: dict


_db: dict[UUID, Workflow] = {}

router = APIRouter()


@router.post("/", response_model=Workflow)
async def create_workflow(workflow: Workflow) -> Workflow:
    workflow.id = uuid4()
    _db[workflow.id] = workflow
    return workflow


@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: UUID) -> Workflow:
    wf = _db.get(workflow_id)
    if wf is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return wf
