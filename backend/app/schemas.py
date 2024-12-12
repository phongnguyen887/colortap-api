from pydantic import BaseModel, Field
from datetime import datetime

class PlayerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class PlayerResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ScoreCreate(BaseModel):
    player_name: str
    score: int = Field(..., gt=0)

class ScoreResponse(BaseModel):
    player_name: str
    score: int
    timestamp: datetime

    class Config:
        orm_mode = True
