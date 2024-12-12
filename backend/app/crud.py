from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas

def get_player_by_name(db: Session, name: str):
    return db.query(models.Player).filter(models.Player.name == name).first()

def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(name=player.name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def create_player_score(db: Session, score: schemas.ScoreCreate):
    # Find player or create if not exists
    db_player = get_player_by_name(db, score.player_name)
    if not db_player:
        db_player = create_player(db, schemas.PlayerCreate(name=score.player_name))
    
    db_score = models.Score(player_id=db_player.id, score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

def get_leaderboard(db: Session, limit: int = 10):
    return (
        db.query(models.Player, models.Score)
        .join(models.Score)
        .order_by(desc(models.Score.score))
        .limit(limit)
        .all()
    )