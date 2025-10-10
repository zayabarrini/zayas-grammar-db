#!/usr/bin/env python3
"""
Analyze the UD data we've integrated
"""

from config.database import SessionLocal
from models.language_models import GrammarRule, UDTreebankSentence, UDTokenAnalysis
from sqlalchemy import func

def analyze_ud_integration():
    """
    Analyze what UD data we have integrated
    """
    db = SessionLocal()
    
    # Count UD-based rules by language
    ud_rules = db.query(
        GrammarRule.language_id,
        func.count(GrammarRule.rule_id)
    ).filter(
        GrammarRule.usage_context == 'universal_dependencies'
    ).group_by(
        GrammarRule.language_id
    ).all()
    
    print("UD-Based Grammar Rules by Language:")
    for lang, count in ud_rules:
        print(f"  {lang}: {count} rules")
    
    # Count stored sentences
    sentence_counts = db.query(
        UDTreebankSentence.language_id,
        func.count(UDTreebankSentence.sentence_id)
    ).group_by(
        UDTreebankSentence.language_id
    ).all()
    
    print("\nStored UD Sentences by Language:")
    for lang, count in sentence_counts:
        print(f"  {lang}: {count} sentences")
    
    # Analyze POS distribution from stored tokens
    if sentence_counts:
        pos_distribution = db.query(
            UDTokenAnalysis.upos,
            func.count(UDTokenAnalysis.analysis_id)
        ).group_by(
            UDTokenAnalysis.upos
        ).order_by(
            func.count(UDTokenAnalysis.analysis_id).desc()
        ).limit(10).all()
        
        print("\nUniversal POS Tag Distribution:")
        for pos, count in pos_distribution:
            print(f"  {pos}: {count} tokens")
    
    db.close()

if __name__ == '__main__':
    analyze_ud_integration()