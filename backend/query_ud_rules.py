#!/usr/bin/env python3
"""
Query and display UD-based grammar rules
"""

from sqlalchemy.orm import joinedload
from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample
from sqlalchemy import func

def display_ud_rules():
    """
    Display all UD-based grammar rules
    """
    db = SessionLocal()
    
    # Get UD-based rules with examples
    ud_rules = db.query(GrammarRule).filter(
        GrammarRule.usage_context.in_(['universal_dependencies', 'enhanced_ud'])
    ).options(
        joinedload(GrammarRule.examples),
        joinedload(GrammarRule.language)
    ).all()
    
    print("UD-Based Grammar Rules:\n")
    print("=" * 80)
    
    for rule in ud_rules:
        print(f"\nLanguage: {rule.language.language_name} ({rule.language_id})")
        print(f"Rule: {rule.rule_name}")
        print(f"Description: {rule.rule_description}")
        print(f"Difficulty: {rule.difficulty_level}/5")
        print(f"Source: {rule.usage_context}")
        
        if rule.examples:
            print("Examples:")
            for example in rule.examples[:3]:  # Show first 3 examples
                print(f"  - {example.example_sentence}")
        
        print("-" * 40)
    
    # Statistics
    stats = db.query(
        GrammarRule.usage_context,
        GrammarRule.language_id,
        func.count(GrammarRule.rule_id)
    ).filter(
        GrammarRule.usage_context.in_(['universal_dependencies', 'enhanced_ud'])
    ).group_by(
        GrammarRule.usage_context,
        GrammarRule.language_id
    ).all()
    
    print(f"\n📊 UD Rules Statistics:")
    for source, lang, count in stats:
        print(f"  {lang} ({source}): {count} rules")
    
    total_ud_rules = db.query(GrammarRule).filter(
        GrammarRule.usage_context.in_(['universal_dependencies', 'enhanced_ud'])
    ).count()
    
    total_rules = db.query(GrammarRule).count()
    
    print(f"\nTotal UD-based rules: {total_ud_rules}")
    print(f"Total all grammar rules: {total_rules}")
    print(f"UD rules percentage: {(total_ud_rules/total_rules)*100:.1f}%")
    
    db.close()

if __name__ == '__main__':
    display_ud_rules()