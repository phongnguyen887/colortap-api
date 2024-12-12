from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

# Import all necessary modules
from .database import engine, get_db
from . import crud, models, schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(
    title="Game Leaderboard API",
    description="API for managing game player scores and leaderboard",
    version="1.0.0"
)

# Root route for basic health check
@app.get("/")
def read_root():
    return {"message": "Welcome to Game Leaderboard API", "status": "healthy"}

# Check player name availability
@app.get("/players/check", response_model=bool)
def check_player_name(
    name: str = Query(
        ..., 
        min_length=1, 
        max_length=50, 
        description="Player name to check"
        )
    , db: Session = Depends(get_db)
):
    """
    Check if player name is available
    
    - Requires a non-empty name
    - Name must be between 1 and 50 characters
    - Trims whitespace
    """
    # Trim whitespace and validate
    cleaned_name = name.strip()
    
    if not cleaned_name:
        raise HTTPException(
            status_code=400, 
            detail="Player name cannot be empty or just whitespace"
        ) 
        return False

    player = crud.get_player_by_name(db, name)
    return player is None

# Register new player
@app.post("/players/register", response_model=schemas.PlayerResponse)
def register_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """Register a new player"""
    existing_player = crud.get_player_by_name(db, player.name)
    if existing_player:
        raise HTTPException(status_code=400, detail="Player name already exists")
    return crud.create_player(db, player)

# Submit player score
@app.post("/scores/submit", response_model=schemas.ScoreResponse)
def submit_score(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    """Submit a player's score"""
    return crud.create_player_score(db, score)

# Get leaderboard
@app.get("/leaderboard", response_model=List[schemas.ScoreResponse])
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

# Optional: Add Swagger UI documentation routes
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return app