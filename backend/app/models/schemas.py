from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    question: str
    
class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
    question: str

class PlanetBase(BaseModel):
    name: str
    type: Optional[str] = None
    mass: Optional[float] = None
    radius: Optional[float] = None
    distance_from_sun: Optional[float] = None
    orbital_period: Optional[float] = None
    moons: Optional[int] = None
    description: Optional[str] = None

class PlanetResponse(PlanetBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class MissionBase(BaseModel):
    name: str
    launch_date: Optional[str] = None
    status: Optional[str] = None
    target: Optional[str] = None
    description: Optional[str] = None
    agency: Optional[str] = None

class MissionResponse(MissionBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    query: str
    n_results: Optional[int] = 5

class SearchResponse(BaseModel):
    results: List[dict]
    query: str