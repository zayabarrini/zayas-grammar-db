#!/usr/bin/env python3
"""
Add intermediate-level Chinese grammar rules
"""

from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample
from sqlalchemy import func  # Add this import

def add_intermediate_chinese():
    db = SessionLocal()
    
    intermediate_rules = [
        # Intermediate Structures (Difficulty 3)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,  # Ba construction
                rule_name='把 with Direction Complements', 
                rule_description='把 structure combined with direction complements for complex movements.',
                difficulty_level=3
            ),
            'examples': [
                '他把书拿出来了。 (Tā bǎ shū ná chūlái le.) - He took the book out.',
                '请把椅子搬过去。 (Qǐng bǎ yǐzi bān guòqù.) - Please move the chair over there.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=58,  # Bei construction
                rule_name='被 with Agents', 
                rule_description='被 structure specifying who performed the action.',
                difficulty_level=3
            ),
            'examples': [
                '我的钱包被小偷偷走了。 (Wǒ de qiánbāo bèi xiǎotōu tōu zǒu le.) - My wallet was stolen by a thief.',
                '这个问题被他解决了。 (Zhège wèntí bèi tā jiějué le.) - This problem was solved by him.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=59,  # Shi de construction
                rule_name='是...的 for Emphasis', 
                rule_description='Using 是...的 to emphasize different aspects of past events.',
                difficulty_level=3
            ),
            'examples': [
                '我是在北京学的汉语。 (Wǒ shì zài Běijīng xué de Hànyǔ.) - It was in Beijing that I studied Chinese.',
                '他是坐火车来的。 (Tā shì zuò huǒchē lái de.) - It was by train that he came.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Potential complement
                rule_name='Complex Potential Complements', 
                rule_description='Potential complements with more complex verb phrases.',
                difficulty_level=3
            ),
            'examples': [
                '这个问题我回答不上来。 (Zhège wèntí wǒ huídá bù shànglái.) - I cannot answer this question.',
                '他一个人做得完这么多工作吗？ (Tā yī gè rén zuò dé wán zhème duō gōngzuò ma?) - Can he finish this much work alone?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=52,  # Result complement
                rule_name='Multiple Result Complements', 
                rule_description='Using multiple result complements in sequence.',
                difficulty_level=3
            ),
            'examples': [
                '我听懂了老师讲的内容。 (Wǒ tīng dǒng le lǎoshī jiǎng de nèiróng.) - I understood the content the teacher explained.',
                '他看完了那本小说。 (Tā kàn wán le nà běn xiǎoshuō.) - He finished reading that novel.'
            ]
        },
        
        # Connectors and Complex Sentences (Difficulty 3)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='不但...而且 (Not only...but also)', 
                rule_description='Expressing addition and emphasis in complex sentences.',
                difficulty_level=3
            ),
            'examples': [
                '他不但会说中文，而且说得非常流利。 (Tā bùdàn huì shuō Zhōngwén, érqiě shuō dé fēicháng liúlì.) - He not only can speak Chinese, but also speaks very fluently.',
                '这个地方不但漂亮，而且安静。 (Zhège dìfāng bùdàn piàoliang, érqiě ānjìng.) - This place is not only beautiful, but also quiet.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='虽然...但是 (Although...but)', 
                rule_description='Expressing concession and contrast.',
                difficulty_level=3
            ),
            'examples': [
                '虽然下雨了，但是我们还是去公园了。 (Suīrán xià yǔ le, dànshì wǒmen háishì qù gōngyuán le.) - Although it rained, we still went to the park.',
                '他虽然年轻，但是很有经验。 (Tā suīrán niánqīng, dànshì hěn yǒu jīngyàn.) - Although he is young, he is very experienced.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='因为...所以 (Because...therefore)', 
                rule_description='Expressing cause and effect relationships.',
                difficulty_level=3
            ),
            'examples': [
                '因为天气不好，所以比赛取消了。 (Yīnwèi tiānqì bù hǎo, suǒyǐ bǐsài qǔxiāo le.) - Because the weather is bad, the game was cancelled.',
                '因为他努力学习，所以进步很快。 (Yīnwèi tā nǔlì xuéxí, suǒyǐ jìnbù hěn kuài.) - Because he studies hard, he improves quickly.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='如果...就 (If...then)', 
                rule_description='Conditional sentences expressing hypothetical situations.',
                difficulty_level=3
            ),
            'examples': [
                '如果明天下雨，我们就不去爬山。 (Rúguǒ míngtiān xià yǔ, wǒmen jiù bù qù páshān.) - If it rains tomorrow, we will not go hiking.',
                '如果你有时间，就来参加我的生日聚会。 (Rúguǒ nǐ yǒu shíjiān, jiù lái cānjiā wǒ de shēngrì jùhuì.) - If you have time, come to my birthday party.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,  # Conjunctions
                rule_name='只要...就 (As long as...then)', 
                rule_description='Expressing sufficient conditions.',
                difficulty_level=3
            ),
            'examples': [
                '只要你努力，就一定能成功。 (Zhǐyào nǐ nǔlì, jiù yīdìng néng chénggōng.) - As long as you work hard, you will definitely succeed.',
                '只要不下雨，我们就去野餐。 (Zhǐyào bù xià yǔ, wǒmen jiù qù yěcān.) - As long as it doesn\'t rain, we will go for a picnic.'
            ]
        },
        
        # Advanced Usage of Particles (Difficulty 3)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=39,  # Aspect particles
                rule_name='了 for Change of State', 
                rule_description='Using 了 to indicate a change of state or new situation.',
                difficulty_level=3
            ),
            'examples': [
                '他现在是大学生了。 (Tā xiànzài shì dàxuéshēng le.) - He is a college student now (he wasn\'t before).',
                '天气冷了，多穿点衣服。 (Tiānqì lěng le, duō chuān diǎn yīfu.) - The weather has gotten cold, wear more clothes.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=55,  # Aspect particles
                rule_name='着 for Simultaneous Actions', 
                rule_description='Using 着 to describe two actions happening simultaneously.',
                difficulty_level=3
            ),
            'examples': [
                '他笑着对我说。 (Tā xiào zhe duì wǒ shuō.) - He said to me while smiling.',
                '妈妈听着音乐做饭。 (Māmā tīng zhe yīnyuè zuò fàn.) - Mom cooks while listening to music.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=55,  # Aspect particles
                rule_name='过 for Life Experiences', 
                rule_description='Using 过 to talk about life experiences and past events.',
                difficulty_level=3
            ),
            'examples': [
                '我从来没有见过这么漂亮的风景。 (Wǒ cónglái méiyǒu jiàn guò zhème piàoliang de fēngjǐng.) - I have never seen such beautiful scenery.',
                '你吃过四川菜吗？ (Nǐ chī guò Sìchuān cài ma?) - Have you ever eaten Sichuan food?'
            ]
        },
        
        # Complex Question Patterns (Difficulty 3)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=12,  # Question patterns
                rule_name='Rhetorical Questions', 
                rule_description='Questions that don\'t expect answers, used for emphasis.',
                difficulty_level=3
            ),
            'examples': [
                '这不是很明显吗？ (Zhè bù shì hěn míngxiǎn ma?) - Isn\'t this very obvious?',
                '谁不知道这件事呢？ (Shéi bù zhīdào zhè jiàn shì ne?) - Who doesn\'t know about this matter?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=54,  # Question particles
                rule_name='吧 for Suggestions and Assumptions', 
                rule_description='Using 吧 to make suggestions or express assumptions.',
                difficulty_level=3
            ),
            'examples': [
                '我们走吧。 (Wǒmen zǒu ba.) - Let\'s go.',
                '他大概是美国人吧。 (Tā dàgài shì Měiguó rén ba.) - He is probably American, I assume.'
            ]
        },
        
        # Additional Intermediate Structures
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=40,  # Serial verbs
                rule_name='Purpose with 来 and 去', 
                rule_description='Using 来 and 去 in serial verb constructions to express purpose.',
                difficulty_level=3
            ),
            'examples': [
                '我来中国学习中文。 (Wǒ lái Zhōngguó xuéxí Zhōngwén.) - I came to China to study Chinese.',
                '他去图书馆看书。 (Tā qù túshūguǎn kàn shū.) - He goes to the library to read books.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=65,  # Time expressions
                rule_name='Time Duration Placement', 
                rule_description='Correct placement of time duration expressions in sentences.',
                difficulty_level=3
            ),
            'examples': [
                '我学中文学了三年。 (Wǒ xué Zhōngwén xué le sān nián.) - I studied Chinese for three years.',
                '他等了你半个小时。 (Tā děng le nǐ bàn gè xiǎoshí.) - He waited for you for half an hour.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=66,  # Location expressions
                rule_name='Complex Location Phrases', 
                rule_description='Using complex location phrases with 在 and position words.',
                difficulty_level=3
            ),
            'examples': [
                '书在桌子上的盒子里面。 (Shū zài zhuōzi shàng de hézi lǐmiàn.) - The book is inside the box on the table.',
                '他在学校后面的咖啡馆工作。 (Tā zài xuéxiào hòumiàn de kāfēi guǎn gōngzuò.) - He works at the café behind the school.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,  # Measure words
                rule_name='Advanced Measure Words', 
                rule_description='Less common but important measure words for specific contexts.',
                difficulty_level=3
            ),
            'examples': [
                '一项研究 (yī xiàng yánjiū) - one research project',
                '一道菜 (yī dào cài) - one dish (of food)',
                '一场电影 (yī chǎng diànyǐng) - one movie screening',
                '一件衣服 (yī jiàn yīfu) - one piece of clothing'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,  # Adverbs
                rule_name='Adverbs of Frequency and Degree', 
                rule_description='Using various adverbs to express frequency and degree precisely.',
                difficulty_level=3
            ),
            'examples': [
                '他偶尔会来看我。 (Tā ǒu\'ěr huì lái kàn wǒ.) - He occasionally comes to see me.',
                '这个问题相当复杂。 (Zhège wèntí xiāngdāng fùzá.) - This problem is quite complex.',
                '我几乎每天都锻炼。 (Wǒ jīhū měitiān dōu duànliàn.) - I exercise almost every day.'
            ]
        }
    ]

    print('Adding intermediate Chinese grammar rules...')
    added_count = 0

    for rule_data in intermediate_rules:
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
    print(f'✅ Successfully added {added_count} intermediate Chinese grammar rules!')

    # Count total Chinese rules now
    total_zh = db.query(GrammarRule).filter(GrammarRule.language_id == 'zh').count()
    print(f'Total Chinese grammar rules: {total_zh}')

    # Count by difficulty
    difficulty_counts = db.query(
        GrammarRule.difficulty_level, 
        db.func.count(GrammarRule.rule_id)
    ).filter(
        GrammarRule.language_id == 'zh'
    ).group_by(
        GrammarRule.difficulty_level
    ).all()

    print('\nChinese Rules by Difficulty Level After Update:')
    for level, count in difficulty_counts:
        descriptions = {
            1: 'Beginner',
            2: 'Elementary', 
            3: 'Intermediate',
            4: 'Advanced',
            5: 'Expert'
        }
        desc = descriptions.get(level, 'Unknown')
        print(f'Level {level} ({desc}): {count} rules')

    db.close()

if __name__ == '__main__':
    add_intermediate_chinese()