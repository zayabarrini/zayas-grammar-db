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


from sqlalchemy import func
from models.language_models import Language, GrammarRule


@router.get("/with-rules/count")
async def get_languages_with_rule_counts(db: Session = Depends(get_db)):
    # Query to get languages with their rule counts
    languages_with_counts = (
        db.query(
            Language.language_id,
            Language.language_name,
            Language.language_family,
            Language.script,
            func.count(GrammarRule.rule_id).label("rule_count"),
        )
        .outerjoin(GrammarRule, Language.language_id == GrammarRule.language_id)
        .group_by(
            Language.language_id,
            Language.language_name,
            Language.language_family,
            Language.script,
        )
        .all()
    )

    # Convert to list of dictionaries
    result = []
    for lang in languages_with_counts:
        result.append(
            {
                "language_id": lang.language_id,
                "language_name": lang.language_name,
                "language_family": lang.language_family,
                "script": lang.script,
                "rule_count": lang.rule_count,
            }
        )

    return result
