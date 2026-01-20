from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import HealthGoalCreate, HealthGoalResponse, HealthGoalUpdate
from app.services.crud import health_goal

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("/", response_model=HealthGoalResponse)
def create_goal(goal: HealthGoalCreate, db: Session = Depends(get_db)):
    return health_goal.create(db=db, obj_in=goal)


@router.get("/{goal_id}", response_model=HealthGoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = health_goal.get(db=db, id=goal_id)
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal


@router.get("/", response_model=list[HealthGoalResponse])
def list_goals(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return health_goal.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{goal_id}", response_model=HealthGoalResponse)
def update_goal(goal_id: int, goal_update: HealthGoalUpdate, db: Session = Depends(get_db)):
    db_goal = health_goal.get(db=db, id=goal_id)
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return health_goal.update(db=db, db_obj=db_goal, obj_in=goal_update)


@router.delete("/{goal_id}", response_model=HealthGoalResponse)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = health_goal.delete(db=db, id=goal_id)
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal
