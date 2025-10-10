#!/usr/bin/env python3
"""
Clean up generic German rules and keep only proper ones
"""

from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample

def cleanup_german_rules():
    """
    Remove generic rules and keep language-specific ones
    """
    db = SessionLocal()
    
    # Rules to keep (language-specific)
    rules_to_keep = [
        'German Case System',
        'Verb Second (V2) Word Order', 
        'Separable Prefix Verbs',
        'Adjective Declension',
        'Subjunctive II (Konjunktiv II)',
        'Accusative Prepositions',
        'Dative Prepositions',
        'Genitive Case',
        'Definite Articles',
        'Verb Second (V2) Rule',
        'Noun Gender',
        'Plural Formation',
        'Perfekt Tense'
    ]
    
    # Find rules to delete
    rules_to_delete = db.query(GrammarRule).filter(
        GrammarRule.language_id == 'de',
        ~GrammarRule.rule_name.in_(rules_to_keep)
    ).all()
    
    print(f"Found {len(rules_to_delete)} German rules to delete")
    
    deleted_count = 0
    for rule in rules_to_delete:
        print(f"Deleting: {rule.rule_name}")
        
        # Delete associated examples first
        db.query(RuleExample).filter(
            RuleExample.rule_id == rule.rule_id
        ).delete()
        
        # Delete the rule
        db.delete(rule)
        deleted_count += 1
    
    db.commit()
    db.close()
    print(f"✅ Deleted {deleted_count} generic German rules")

if __name__ == '__main__':
    cleanup_german_rules()