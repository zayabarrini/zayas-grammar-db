from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.language_models import Language

router = APIRouter(prefix="/languages", tags=["languages"])

@router.get("/")
async def get_languages(db: Session = Depends(get_db)):
    languages = db.query(Language).all()
    return languages

@router.get("/{language_id}")
async def get_language(language_id: str, db: Session = Depends(get_db)):
    language = db.query(Language).filter(Language.language_id == language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language