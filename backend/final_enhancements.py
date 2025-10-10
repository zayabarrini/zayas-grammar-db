#!/usr/bin/env python3
"""
Add final enhancements to balance the database
"""

from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample

def add_balanced_rules():
    """
    Add rules to languages with fewer examples
    """
    db = SessionLocal()
    
    additional_rules = [
        # German - more advanced topics
        {
            'language': 'de',
            'name': 'Subjunctive II (Konjunktiv II)',
            'description': 'Used for hypothetical situations, wishes, and polite requests. Formed with würden + infinitive or with umlaut changes.',
            'difficulty': 4,
            'examples': [
                'Wenn ich reich wäre, würde ich um die Welt reisen.',
                'Ich wünschte, ich hätte mehr Zeit.',
                'Könntest du mir bitte helfen?'
            ]
        },
        
        # French - more verb tenses
        {
            'language': 'fr', 
            'name': 'Imparfait vs Passé Composé',
            'description': 'Imparfait for ongoing past actions, Passé Composé for completed actions. Key distinction in French narrative.',
            'difficulty': 3,
            'examples': [
                'Quand j\'étais jeune, je jouais au football.',
                'Hier, j\'ai fini mon travail à 18 heures.',
                'Il pleuvait quand je suis sorti.'
            ]
        },
        
        # Japanese - more particles
        {
            'language': 'ja',
            'name': 'Particles は vs が',
            'description': 'は marks the topic, が marks the subject. は for known information, が for new information.',
            'difficulty': 3,
            'examples': [
                '私は学生です。 (I am a student - topic)',
                '私が行きます。 (I will go - emphasis)',
                '猫は机の上にいます。 (The cat is on the desk - topic)'
            ]
        },
        
        # Arabic - more verb forms
        {
            'language': 'ar',
            'name': 'Verb Forms (أوزان)',
            'description': 'Arabic has 10 common verb forms that change meaning. Form I is basic, other forms add meanings like causation, reflexivity, etc.',
            'difficulty': 4,
            'examples': [
                'كَتَبَ (he wrote - Form I)',
                'كَتَّبَ (he made someone write - Form II)',
                'تَكَاتَبَ (they corresponded with each other - Form VI)'
            ]
        }
    ]
    
    added_count = 0
    for rule_data in additional_rules:
        try:
            grammar_rule = GrammarRule(
                language_id=rule_data['language'],
                rule_name=rule_data['name'],
                rule_description=rule_data['description'],
                difficulty_level=rule_data['difficulty']
            )
            
            db.add(grammar_rule)
            db.flush()
            
            for example_text in rule_data['examples']:
                example = RuleExample(
                    rule_id=grammar_rule.rule_id,
                    example_sentence=example_text
                )
                db.add(example)
            
            added_count += 1
            print(f"Added: {rule_data['language']} - {rule_data['name']}")
            
        except Exception as e:
            print(f"Error adding rule: {e}")
    
    db.commit()
    db.close()
    print(f"✅ Added {added_count} final enhancement rules")

if __name__ == '__main__':
    add_balanced_rules()