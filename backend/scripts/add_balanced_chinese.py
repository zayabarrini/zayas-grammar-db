#!/usr/bin/env python3
"""
Add balanced Chinese grammar rules to fill gaps
"""

from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample
from sqlalchemy import func

def add_balanced_chinese():
    db = SessionLocal()
    
    # More beginner-friendly rules (Level 1-2)
    balanced_rules = [
        # Beginner Level (1)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=13,  # Basic structure
                rule_name='Basic Questions with 什么', 
                rule_description='Using 什么 (what) to form basic questions about objects.',
                difficulty_level=1
            ),
            'examples': [
                '这是什么？ (Zhè shì shénme?) - What is this?',
                '你喜欢什么颜色？ (Nǐ xǐhuan shénme yánsè?) - What color do you like?',
                '你想吃什么？ (Nǐ xiǎng chī shénme?) - What do you want to eat?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=12,  # Questions
                rule_name='Basic Questions with 谁', 
                rule_description='Using 谁 (who) to ask about people.',
                difficulty_level=1
            ),
            'examples': [
                '你是谁？ (Nǐ shì shéi?) - Who are you?',
                '他是谁？ (Tā shì shéi?) - Who is he?',
                '谁是你的老师？ (Shéi shì nǐ de lǎoshī?) - Who is your teacher?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=12,  # Questions
                rule_name='Basic Questions with 哪里', 
                rule_description='Using 哪里 (where) to ask about locations.',
                difficulty_level=1
            ),
            'examples': [
                '你在哪里？ (Nǐ zài nǎlǐ?) - Where are you?',
                '书店在哪里？ (Shūdiàn zài nǎlǐ?) - Where is the bookstore?',
                '你去哪里？ (Nǐ qù nǎlǐ?) - Where are you going?'
            ]
        },
        
        # Elementary Level (2)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,  # Measure words
                rule_name='Common Measure Words', 
                rule_description='Essential measure words for everyday objects.',
                difficulty_level=2
            ),
            'examples': [
                '一杯水 (yī bēi shuǐ) - one glass of water',
                '一碗饭 (yī wǎn fàn) - one bowl of rice',
                '一瓶啤酒 (yī píng píjiǔ) - one bottle of beer',
                '一块蛋糕 (yī kuài dàngāo) - one piece of cake'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,  # Adverbs
                rule_name='Basic Adverbs of Time', 
                rule_description='Common time adverbs and their placement.',
                difficulty_level=2
            ),
            'examples': [
                '我现在很忙。 (Wǒ xiànzài hěn máng.) - I am very busy now.',
                '他刚才来了。 (Tā gāngcái lái le.) - He came just now.',
                '我们马上出发。 (Wǒmen mǎshàng chūfā.) - We will leave immediately.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=65,  # Time expressions
                rule_name='Days of the Week', 
                rule_description='Using days of the week in sentences.',
                difficulty_level=2
            ),
            'examples': [
                '今天星期一。 (Jīntiān xīngqīyī.) - Today is Monday.',
                '我们星期五考试。 (Wǒmen xīngqīwǔ kǎoshì.) - We have an exam on Friday.',
                '他星期天休息。 (Tā xīngqītiān xiūxi.) - He rests on Sunday.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=65,  # Time expressions
                rule_name='Months and Seasons', 
                rule_description='Talking about months and seasons.',
                difficulty_level=2
            ),
            'examples': [
                '一月很冷。 (Yī yuè hěn lěng.) - January is very cold.',
                '春天很漂亮。 (Chūntiān hěn piàoliang.) - Spring is very beautiful.',
                '我喜欢秋天。 (Wǒ xǐhuan qiūtiān.) - I like autumn.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=66,  # Location
                rule_name='Basic Location Words', 
                rule_description='Common location words and their usage.',
                difficulty_level=2
            ),
            'examples': [
                '书在桌子上。 (Shū zài zhuōzi shàng.) - The book is on the table.',
                '猫在椅子下面。 (Māo zài yǐzi xiàmiàn.) - The cat is under the chair.',
                '银行在学校旁边。 (Yínháng zài xuéxiào pángbiān.) - The bank is next to the school.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='和 for Connecting Nouns', 
                rule_description='Using 和 to connect multiple nouns.',
                difficulty_level=2
            ),
            'examples': [
                '我和他都是学生。 (Wǒ hé tā dōu shì xuéshēng.) - Both he and I are students.',
                '我喜欢苹果和香蕉。 (Wǒ xǐhuan píngguǒ hé xiāngjiāo.) - I like apples and bananas.',
                '这本书和那本书都很好。 (Zhè běn shū hé nà běn shū dōu hěn hǎo.) - This book and that book are both good.'
            ]
        },
        
        # More Intermediate Level (3)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='或者 for Alternatives', 
                rule_description='Using 或者 to express alternatives or choices.',
                difficulty_level=3
            ),
            'examples': [
                '你可以喝茶或者咖啡。 (Nǐ kěyǐ hē chá huòzhě kāfēi.) - You can drink tea or coffee.',
                '我们明天或者后天见面。 (Wǒmen míngtiān huòzhě hòutiān jiànmiàn.) - We can meet tomorrow or the day after.',
                '你要中文书或者英文书？ (Nǐ yào Zhōngwén shū huòzhě Yīngwén shū?) - Do you want Chinese books or English books?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='还是 for Questions', 
                rule_description='Using 还是 in questions to offer choices.',
                difficulty_level=3
            ),
            'examples': [
                '你想喝茶还是咖啡？ (Nǐ xiǎng hē chá háishì kāfēi?) - Do you want to drink tea or coffee?',
                '我们坐公交还是地铁？ (Wǒmen zuò gōngjiāo háishì dìtiě?) - Should we take the bus or subway?',
                '你今天去还是明天去？ (Nǐ jīntiān qù háishì míngtiān qù?) - Are you going today or tomorrow?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=39,  # Aspect
                rule_name='了 with Time Phrases', 
                rule_description='Using 了 with specific time phrases.',
                difficulty_level=3
            ),
            'examples': [
                '我昨天看了一场电影。 (Wǒ zuótiān kàn le yī chǎng diànyǐng.) - I watched a movie yesterday.',
                '他上个月去了上海。 (Tā shàng gè yuè qù le Shànghǎi.) - He went to Shanghai last month.',
                '我们去年开始学中文。 (Wǒmen qùnián kāishǐ xué Zhōngwén.) - We started learning Chinese last year.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=55,  # Aspect particles
                rule_name='着 for State Description', 
                rule_description='Using 着 to describe the state something is in.',
                difficulty_level=3
            ),
            'examples': [
                '门开着。 (Mén kāi zhe.) - The door is open.',
                '灯亮着。 (Dēng liàng zhe.) - The light is on.',
                '他穿着红衣服。 (Tā chuān zhe hóng yīfu.) - He is wearing red clothes.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=52,  # Result complement
                rule_name='Result Complements with 到', 
                rule_description='Using 到 as a result complement meaning "to reach" or "to achieve".',
                difficulty_level=3
            ),
            'examples': [
                '我找到我的手机了。 (Wǒ zhǎo dào wǒ de shǒujī le.) - I found my phone.',
                '他买到票了。 (Tā mǎi dào piào le.) - He bought the ticket (successfully).',
                '我看到他了。 (Wǒ kàn dào tā le.) - I saw him.'
            ]
        }
    ]

    print('Adding balanced Chinese grammar rules...')
    added_count = 0

    for rule_data in balanced_rules:
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
    print(f'✅ Successfully added {added_count} balanced Chinese grammar rules!')

    # Final statistics
    total_zh = db.query(GrammarRule).filter(GrammarRule.language_id == 'zh').count()
    print(f'Total Chinese grammar rules: {total_zh}')

    difficulty_counts = db.query(
        GrammarRule.difficulty_level, 
        func.count(GrammarRule.rule_id)
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

    # Calculate percentages
    total = sum(count for _, count in difficulty_counts)
    print(f'\nTotal rules: {total}')
    for level, count in sorted(difficulty_counts):
        percentage = (count / total) * 100
        print(f'Level {level}: {count} rules ({percentage:.1f}%)')

    db.close()

if __name__ == '__main__':
    add_balanced_chinese()