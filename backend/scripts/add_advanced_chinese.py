#!/usr/bin/env python3
"""
Add advanced Chinese grammar rules
"""

from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample
from sqlalchemy import func  # Add this import

def add_advanced_chinese():
    db = SessionLocal()
    
    advanced_rules = [
        # Advanced Structures (Difficulty 4)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,  # Ba construction
                rule_name='把 with Negative Commands', 
                rule_description='Using 把 structure in negative imperative sentences.',
                difficulty_level=4
            ),
            'examples': [
                '别把这件事告诉他。 (Bié bǎ zhè jiàn shì gàosu tā.) - Don\'t tell him about this matter.',
                '不要把垃圾扔在这里。 (Bù yào bǎ lèsè rēng zài zhèlǐ.) - Don\'t throw trash here.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=58,  # Bei construction
                rule_name='被 without Agent', 
                rule_description='Using 被 without specifying who performed the action.',
                difficulty_level=4
            ),
            'examples': [
                '窗户被打破了。 (Chuānghù bèi dǎpò le.) - The window was broken.',
                '计划被改变了。 (Jìhuà bèi gǎibiàn le.) - The plan was changed.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='即使...也 (Even if...still)', 
                rule_description='Expressing concession in hypothetical situations.',
                difficulty_level=4
            ),
            'examples': [
                '即使下雨，我们也要去。 (Jíshǐ xià yǔ, wǒmen yě yào qù.) - Even if it rains, we still want to go.',
                '即使他很忙，也会帮助你。 (Jíshǐ tā hěn máng, yě huì bāngzhù nǐ.) - Even if he is busy, he will still help you.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='无论...都 (No matter...all)', 
                rule_description='Expressing universal conditions.',
                difficulty_level=4
            ),
            'examples': [
                '无论你去哪里，我都跟着你。 (Wúlùn nǐ qù nǎlǐ, wǒ dōu gēn zhe nǐ.) - No matter where you go, I will follow you.',
                '无论多么困难，我们都要完成这个任务。 (Wúlùn duōme kùnnán, wǒmen dōu yào wánchéng zhège rènwù.) - No matter how difficult it is, we must complete this task.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=39,  # Aspect particles
                rule_name='了 in Complex Sentences', 
                rule_description='Advanced usage of 了 in compound and complex sentences.',
                difficulty_level=4
            ),
            'examples': [
                '我吃了饭就去图书馆。 (Wǒ chī le fàn jiù qù túshūguǎn.) - I will go to the library after I eat.',
                '他看了三个小时书才休息。 (Tā kàn le sān gè xiǎoshí shū cái xiūxi.) - He didn\'t rest until he had read for three hours.'
            ]
        }
    ]

    print('Adding advanced Chinese grammar rules...')
    added_count = 0

    for rule_data in advanced_rules:
        try:
            db.add(rule_data['rule'])
            db.flush()
            
            for example_text in rule_data['examples']:
                example = RuleExample(
                    rule_id=rule_data['rule'].rule_id,
                    example_sentence=example_text
                )
                db.add(example)
            
            added_count += 1
            print(f'Added rule: {rule_data["rule"].rule_name}')
            
        except Exception as e:
            print(f'Error adding rule {rule_data["rule"].rule_name}: {e}')
            continue

    db.commit()
    print(f'✅ Successfully added {added_count} advanced Chinese grammar rules!')

    # Final count and distribution
    total_zh = db.query(GrammarRule).filter(GrammarRule.language_id == 'zh').count()
    print(f'Total Chinese grammar rules: {total_zh}')

    difficulty_counts = db.query(
        GrammarRule.difficulty_level, 
        db.func.count(GrammarRule.rule_id)
    ).filter(
        GrammarRule.language_id == 'zh'
    ).group_by(
        GrammarRule.difficulty_level
    ).all()

    print('\nFinal Chinese Rules Distribution:')
    print('Level | Count | Description')
    print('------|-------|-------------')
    for level, count in difficulty_counts:
        descriptions = {
            1: 'Beginner',
            2: 'Elementary', 
            3: 'Intermediate',
            4: 'Advanced',
            5: 'Expert'
        }
        desc = descriptions.get(level, 'Unknown')
        print(f'{level:5} | {count:5} | {desc}')

    db.close()

if __name__ == '__main__':
    add_advanced_chinese()