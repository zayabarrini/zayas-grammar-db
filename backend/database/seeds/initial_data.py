from sqlalchemy.orm import Session
from models.language_models import Language, GrammarConcept

def seed_initial_data(db: Session):
    """Seed initial languages and grammar concepts"""
    
    # Add languages
    languages = [
        Language(language_id='de', language_name='German', language_family='Indo-European', script='Latin'),
        Language(language_id='ja', language_name='Japanese', language_family='Japonic', script='Mixed'),
        Language(language_id='ar', language_name='Arabic', language_family='Afro-Asiatic', script='Arabic'),
        Language(language_id='hi', language_name='Hindi', language_family='Indo-European', script='Devanagari'),
        Language(language_id='ko', language_name='Korean', language_family='Koreanic', script='Hangul'),
        Language(language_id='fr', language_name='French', language_family='Indo-European', script='Latin'),
        Language(language_id='it', language_name='Italian', language_family='Indo-European', script='Latin'),
        Language(language_id='ru', language_name='Russian', language_family='Indo-European', script='Cyrillic'),
        Language(language_id='zh', language_name='Chinese', language_family='Sino-Tibetan', script='Hanzi'),
    ]
    
    for language in languages:  
        db.merge(language)  # Use merge to avoid duplicates
    
    # Add grammar concepts
    concepts = [
        GrammarConcept(concept_name='nominative_case', category='case', description='Subject of a verb'),
        GrammarConcept(concept_name='accusative_case', category='case', description='Direct object of a verb'),
        GrammarConcept(concept_name='dative_case', category='case', description='Indirect object of a verb'),
        GrammarConcept(concept_name='topic_marker', category='particle', description='Marks the topic of a sentence'),
        GrammarConcept(concept_name='subject_marker', category='particle', description='Marks the subject of a sentence'),
        GrammarConcept(concept_name='perfective_aspect', category='aspect', description='Completed action'),
        GrammarConcept(concept_name='imperfective_aspect', category='aspect', description='Ongoing or habitual action'),
    ]
    
    for concept in concepts:
        db.merge(concept)
    
    db.commit()
    print("✅ Initial data seeded successfully!")

if __name__ == "__main__":
    from config.database import SessionLocal
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()