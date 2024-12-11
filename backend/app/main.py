from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Game Leaderboard API")

@app.post("/players/check", response_model=bool)
def check_player_name(name: str, db: Session = Depends(get_db)):
    """Check if player name is available"""
    player = crud.get_player_by_name(db, name)
    return player is None

@app.post("/players/register", response_model=schemas.PlayerResponse)
def register_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """Register a new player"""
    existing_player = crud.get_player_by_name(db, player.name)
    if existing_player:
        raise HTTPException(status_code=400, detail="Player name already exists")
    return crud.create_player(db, player)

@app.post("/scores/submit", response_model=schemas.ScoreResponse)
def submit_score(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    """Submit a player's score"""
    return crud.create_player_score(db, score)

@app.get("/leaderboard", response_model=list[schemas.ScoreResponse])
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Get top scores"""
    leaderboard = crud.get_leaderboard(db, limit)
    return [
        schemas.ScoreResponse(
            player_name=player.name, 
            score=score.score, 
            timestamp=score.timestamp
        ) 
        for player, score in leaderboard
    ]
