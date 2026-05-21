from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Planet, NasaMission
from app.models.schemas import PlanetResponse, MissionResponse
from typing import List

router = APIRouter()

@router.get("/planets", response_model=List[PlanetResponse])
def get_planets(db: Session = Depends(get_db)):
    """Return all planets from the database."""
    planets = db.query(Planet).all()
    return planets

@router.get("/planets/{name}", response_model=PlanetResponse)
def get_planet(name: str, db: Session = Depends(get_db)):
    """Return a single planet by name."""
    planet = db.query(Planet).filter(Planet.name.ilike(name)).first()
    if not planet:
        raise HTTPException(status_code=404, detail=f"Planet '{name}' not found.")
    return planet

@router.get("/missions", response_model=List[MissionResponse])
def get_missions(db: Session = Depends(get_db)):
    """Return all NASA missions from the database."""
    missions = db.query(NasaMission).all()
    return missions

@router.get("/missions/{name}", response_model=MissionResponse)
def get_mission(name: str, db: Session = Depends(get_db)):
    """Return a single mission by name."""
    mission = db.query(NasaMission).filter(NasaMission.name.ilike(f"%{name}%")).first()
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission '{name}' not found.")
    return mission