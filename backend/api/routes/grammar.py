from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.language_models import GrammarRule, GrammarConcept, Language
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/grammar", tags=["grammar"])

@router.get("/rules")
async def get_grammar_rules(language_id: str = None, db: Session = Depends(get_db)):
    query = db.query(GrammarRule).options(
        joinedload(GrammarRule.language),
        joinedload(GrammarRule.examples)
    )
    if language_id:
        query = query.filter(GrammarRule.language_id == language_id)
    rules = query.all()
    return rules

@router.get("/rules/{language_id}")
async def get_rules_by_language(language_id: str, db: Session = Depends(get_db)):
    rules = db.query(GrammarRule).options(
        joinedload(GrammarRule.language),
        joinedload(GrammarRule.examples)
    ).filter(GrammarRule.language_id == language_id).all()
    if not rules:
        raise HTTPException(status_code=404, detail="No rules found for this language")
    return rules

@router.get("/concepts")
async def get_grammar_concepts(db: Session = Depends(get_db)):
    return db.query(GrammarConcept).all()

@router.get("/languages-with-rules")
async def get_languages_with_rules(db: Session = Depends(get_db)):
    # Get languages that have grammar rules
    languages_with_rules = db.query(Language).join(GrammarRule).distinct().all()
    return languages_with_rules