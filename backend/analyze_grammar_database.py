#!/usr/bin/env python3
"""
Comprehensive analysis of the grammar database
"""

from sqlalchemy.orm import joinedload
from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample, Language
from sqlalchemy import func

def analyze_database():
    """
    Comprehensive analysis of the grammar database
    """
    db = SessionLocal()
    
    print("📊 GRAMMAR DATABASE ANALYSIS")
    print("=" * 60)
    
    # Overall statistics
    total_rules = db.query(GrammarRule).count()
    total_languages = db.query(Language).count()
    total_examples = db.query(RuleExample).count()
    
    print(f"\n📈 Overall Statistics:")
    print(f"  Total Grammar Rules: {total_rules}")
    print(f"  Total Languages: {total_languages}")
    print(f"  Total Examples: {total_examples}")
    print(f"  Average Examples per Rule: {total_examples/total_rules:.1f}")
    
    # Rules by language
    print(f"\n🌍 Rules by Language:")
    rules_by_lang = db.query(
        GrammarRule.language_id,
        func.count(GrammarRule.rule_id),
        Language.language_name
    ).join(Language).group_by(
        GrammarRule.language_id, Language.language_name
    ).order_by(func.count(GrammarRule.rule_id).desc()).all()
    
    for lang_id, count, lang_name in rules_by_lang:
        print(f"  {lang_name} ({lang_id}): {count} rules")
    
    # Rules by difficulty
    print(f"\n🎯 Rules by Difficulty Level:")
    rules_by_diff = db.query(
        GrammarRule.difficulty_level,
        func.count(GrammarRule.rule_id)
    ).group_by(GrammarRule.difficulty_level).order_by(GrammarRule.difficulty_level).all()
    
    for level, count in rules_by_diff:
        level_names = {
            1: "Beginner",
            2: "Elementary", 
            3: "Intermediate",
            4: "Advanced",
            5: "Expert"
        }
        level_name = level_names.get(level, f"Level {level}")
        percentage = (count / total_rules) * 100
        print(f"  {level_name}: {count} rules ({percentage:.1f}%)")
    
    # UD vs Manual rules
    print(f"\n🔬 Data Sources:")
    sources = db.query(
        GrammarRule.usage_context,
        func.count(GrammarRule.rule_id)
    ).group_by(GrammarRule.usage_context).all()
    
    for source, count in sources:
        source_name = "Manual" if source is None else source.replace('_', ' ').title()
        percentage = (count / total_rules) * 100
        print(f"  {source_name}: {count} rules ({percentage:.1f}%)")
    
    # Most common concepts
    print(f"\n💡 Most Common Grammar Concepts:")
    from models.language_models import GrammarConcept
    common_concepts = db.query(
        GrammarConcept.concept_name,
        func.count(GrammarRule.rule_id)
    ).join(GrammarRule).group_by(
        GrammarConcept.concept_name
    ).order_by(
        func.count(GrammarRule.rule_id).desc()
    ).limit(10).all()
    
    for concept, count in common_concepts:
        print(f"  {concept}: {count} rules")
    
    # Language-specific insights
    print(f"\n🎨 Language-Specific Features:")
    
    # Chinese rules
    chinese_rules = db.query(GrammarRule).filter(
        GrammarRule.language_id == 'zh'
    ).all()
    print(f"  Chinese: {len(chinese_rules)} rules covering tones, measure words, and aspect particles")
    
    # German rules  
    german_rules = db.query(GrammarRule).filter(
        GrammarRule.language_id == 'de'
    ).all()
    print(f"  German: {len(german_rules)} rules covering cases, verb position, and articles")
    
    # Japanese rules
    japanese_rules = db.query(GrammarRule).filter(
        GrammarRule.language_id == 'ja'
    ).all()
    print(f"  Japanese: {len(japanese_rules)} rules covering particles, politeness, and counters")
    
    # Recent additions
    print(f"\n🆕 Recent UD-Based Additions:")
    recent_ud_rules = db.query(GrammarRule).filter(
        GrammarRule.usage_context.in_(['universal_dependencies', 'enhanced_ud'])
    ).order_by(GrammarRule.rule_id.desc()).limit(5).all()
    
    for rule in recent_ud_rules:
        lang = db.query(Language).filter(Language.language_id == rule.language_id).first()
        print(f"  {lang.language_name}: {rule.rule_name}")
    
    db.close()

if __name__ == '__main__':
    analyze_database()