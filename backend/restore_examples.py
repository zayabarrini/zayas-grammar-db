#!/usr/bin/env python3
"""
Restore essential examples for key grammar rules
"""

from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample

def restore_essential_examples():
    """
    Add back essential examples for important rules
    """
    db = SessionLocal()
    
    # Key examples to restore
    essential_examples = [
        # Chinese basic examples
        {
            'rule_name': 'Basic SVO Structure',
            'language': 'zh',
            'examples': [
                '我吃苹果。 (Wǒ chī píngguǒ.) - I eat apples.',
                '他看书。 (Tā kàn shū.) - He reads books.',
                '我们学习中文。 (Wǒmen xuéxí zhōngwén.) - We study Chinese.'
            ]
        },
        {
            'rule_name': 'Measure Words (量词)',
            'language': 'zh', 
            'examples': [
                '一个人 (yī gè rén) - one person',
                '两只猫 (liǎng zhī māo) - two cats',
                '三本书 (sān běn shū) - three books'
            ]
        },
        
        # German examples
        {
            'rule_name': 'Subjunctive II (Konjunktiv II)',
            'language': 'de',
            'examples': [
                'Wenn ich reich wäre, würde ich um die Welt reisen.',
                'Ich wünschte, ich hätte mehr Zeit.',
                'Könntest du mir bitte helfen?'
            ]
        },
        
        # Japanese examples
        {
            'rule_name': 'Particles は vs が',
            'language': 'ja',
            'examples': [
                '私は学生です。 (I am a student - topic)',
                '私が行きます。 (I will go - emphasis)', 
                '猫は机の上にいます。 (The cat is on the desk - topic)'
            ]
        },
        
        # French examples
        {
            'rule_name': 'Imparfait vs Passé Composé',
            'language': 'fr',
            'examples': [
                'Quand j\'étais jeune, je jouais au football.',
                'Hier, j\'ai fini mon travail à 18 heures.',
                'Il pleuvait quand je suis sorti.'
            ]
        },
        
        # Arabic examples
        {
            'rule_name': 'Verb Forms (أوزان)',
            'language': 'ar',
            'examples': [
                'كَتَبَ (he wrote - Form I)',
                'كَتَّبَ (he made someone write - Form II)',
                'تَكَاتَبَ (they corresponded with each other - Form VI)'
            ]
        }
    ]
    
    restored_count = 0
    for example_data in essential_examples:
        try:
            # Find the rule
            rule = db.query(GrammarRule).filter(
                GrammarRule.rule_name == example_data['rule_name'],
                GrammarRule.language_id == example_data['language']
            ).first()
            
            if rule:
                # Add examples
                for example_text in example_data['examples']:
                    example = RuleExample(
                        rule_id=rule.rule_id,
                        example_sentence=example_text
                    )
                    db.add(example)
                    restored_count += 1
                
                print(f"Restored examples for: {example_data['language']} - {example_data['rule_name']}")
            else:
                print(f"Rule not found: {example_data['language']} - {example_data['rule_name']}")
                
        except Exception as e:
            print(f"Error restoring examples: {e}")
    
    db.commit()
    db.close()
    print(f"✅ Restored {restored_count} essential examples")

if __name__ == '__main__':
    restore_essential_examples()