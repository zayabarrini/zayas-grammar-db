#!/usr/bin/env python3
"""
Analyze current German rules in the database
"""

from sqlalchemy.orm import joinedload
from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample

def analyze_german_rules():
    """
    Analyze what German rules we currently have
    """
    db = SessionLocal()
    
    german_rules = db.query(GrammarRule).filter(
        GrammarRule.language_id == 'de'
    ).options(
        joinedload(GrammarRule.examples)
    ).all()
    
    print("Current German Grammar Rules:")
    print("=" * 60)
    
    for rule in german_rules:
        print(f"\nRule: {rule.rule_name}")
        print(f"Description: {rule.rule_description}")
        print(f"Difficulty: {rule.difficulty_level}")
        print(f"Source: {rule.usage_context}")
        
        if rule.examples:
            print("Examples:")
            for example in rule.examples[:2]:
                print(f"  - {example.example_sentence[:80]}...")
        else:
            print("No examples")
        
        print("-" * 40)
    
    # Statistics
    total_rules = len(german_rules)
    sources = {}
    difficulties = {}
    
    for rule in german_rules:
        source = rule.usage_context or 'manual'
        sources[source] = sources.get(source, 0) + 1
        difficulties[rule.difficulty_level] = difficulties.get(rule.difficulty_level, 0) + 1
    
    print(f"\n📊 German Rules Statistics:")
    print(f"Total rules: {total_rules}")
    print(f"Sources: {sources}")
    print(f"Difficulty distribution: {difficulties}")
    
    db.close()

if __name__ == '__main__':
    analyze_german_rules()