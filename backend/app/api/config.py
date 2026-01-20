from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import AppConfigCreate, AppConfigResponse, AppConfigUpdate
from app.services.crud import app_config

router = APIRouter(prefix="/config", tags=["config"])


@router.post("/", response_model=AppConfigResponse)
def create_config(cfg: AppConfigCreate, db: Session = Depends(get_db)):
    return app_config.create(db=db, obj_in=cfg)


@router.get("/{config_id}", response_model=AppConfigResponse)
def get_config(config_id: int, db: Session = Depends(get_db)):
    db_cfg = app_config.get(db=db, id=config_id)
    if not db_cfg:
        raise HTTPException(status_code=404, detail="Config not found")
    return db_cfg


@router.get("/key/{key}", response_model=AppConfigResponse)
def get_config_by_key(key: str, db: Session = Depends(get_db)):
    from app.models import AppConfig

    db_cfg = db.query(AppConfig).filter(AppConfig.key == key).first()
    if not db_cfg:
        raise HTTPException(status_code=404, detail="Config not found")
    return db_cfg


@router.get("/", response_model=list[AppConfigResponse])
def list_configs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return app_config.get_multi(db=db, skip=skip, limit=limit)


@router.patch("/{config_id}", response_model=AppConfigResponse)
def update_config(config_id: int, cfg_update: AppConfigUpdate, db: Session = Depends(get_db)):
    db_cfg = app_config.get(db=db, id=config_id)
    if not db_cfg:
        raise HTTPException(status_code=404, detail="Config not found")
    return app_config.update(db=db, db_obj=db_cfg, obj_in=cfg_update)


@router.delete("/{config_id}", response_model=AppConfigResponse)
def delete_config(config_id: int, db: Session = Depends(get_db)):
    db_cfg = app_config.delete(db=db, id=config_id)
    if not db_cfg:
        raise HTTPException(status_code=404, detail="Config not found")
    return db_cfg
