#!/usr/bin/env python3
"""
Fix text encoding issues in UD examples
"""

from config.database import SessionLocal
from models.language_models import RuleExample

def fix_text_encoding():
    """
    Remove problematic examples with only underscores
    """
    db = SessionLocal()
    
    # Find examples that are mostly underscores
    problematic_examples = db.query(RuleExample).filter(
        RuleExample.example_sentence.like('%________________________________%')
    ).all()
    
    print(f"Found {len(problematic_examples)} problematic examples")
    
    # Delete them
    for example in problematic_examples:
        db.delete(example)
        print(f"Deleted: {example.example_sentence[:50]}...")
    
    db.commit()
    db.close()
    print(f"✅ Fixed {len(problematic_examples)} problematic examples")

if __name__ == '__main__':
    fix_text_encoding()