#!/usr/bin/env python3
"""
Script to add 50 Chinese grammar rules with examples
"""

from ..config.database import SessionLocal
from ..models.language_models import GrammarRule, RuleExample

def add_chinese_rules():
    db = SessionLocal()
    
    chinese_rules = [
        # Basic Sentence Structure (10 rules)
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=13,
                rule_name='Basic SVO Structure', 
                rule_description='Chinese follows Subject-Verb-Object word order in basic sentences.',
                difficulty_level=1
            ),
            'examples': [
                '我吃苹果。 (Wǒ chī píngguǒ.) - I eat apples.',
                '他看书。 (Tā kàn shū.) - He reads books.',
                '我们学习中文。 (Wǒmen xuéxí zhōngwén.) - We study Chinese.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=41,
                rule_name='Topic-Comment Sentences', 
                rule_description='Topic comes first, followed by comment. More flexible than strict SVO.',
                difficulty_level=2
            ),
            'examples': [
                '这本书，我很喜欢。 (Zhè běn shū, wǒ hěn xǐhuan.) - This book, I like it very much.',
                '中文，他说得很好。 (Zhōngwén, tā shuō de hěn hǎo.) - Chinese, he speaks it very well.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,
                rule_name='Measure Words (量词)', 
                rule_description='Required when counting nouns. Different measure words for different types of objects.',
                difficulty_level=2
            ),
            'examples': [
                '一个人 (yī gè rén) - one person',
                '两只猫 (liǎng zhī māo) - two cats',
                '三本书 (sān běn shū) - three books'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=38,
                rule_name='Four Tones System', 
                rule_description='Mandarin has four main tones that change word meaning. Essential for pronunciation.',
                difficulty_level=1
            ),
            'examples': [
                '妈 (mā) - mother (1st tone)',
                '麻 (má) - hemp (2nd tone)',
                '马 (mǎ) - horse (3rd tone)',
                '骂 (mà) - scold (4th tone)'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=39,
                rule_name='Aspect Particle 了', 
                rule_description='了 indicates completed action or change of state. Not exactly past tense.',
                difficulty_level=2
            ),
            'examples': [
                '我吃了饭。 (Wǒ chī le fàn.) - I have eaten.',
                '他去了北京。 (Tā qù le Běijīng.) - He went to Beijing.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=54,
                rule_name='Question Particle 吗', 
                rule_description='Add 吗 at the end of a statement to make a yes/no question.',
                difficulty_level=1
            ),
            'examples': [
                '你是学生吗？ (Nǐ shì xuéshēng ma?) - Are you a student?',
                '他喜欢中文吗？ (Tā xǐhuan zhōngwén ma?) - Does he like Chinese?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=12,
                rule_name='Question Words', 
                rule_description='Use question words in the same position as the answer would be.',
                difficulty_level=1
            ),
            'examples': [
                '你是谁？ (Nǐ shì shéi?) - Who are you?',
                '这是什么？ (Zhè shì shénme?) - What is this?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=55,
                rule_name='Aspect Particle 着', 
                rule_description='着 indicates ongoing action or continuous state.',
                difficulty_level=2
            ),
            'examples': [
                '他坐着。 (Tā zuò zhe.) - He is sitting.',
                '门开着。 (Mén kāi zhe.) - The door is open.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=55,
                rule_name='Aspect Particle 过', 
                rule_description='过 indicates past experience.',
                difficulty_level=2
            ),
            'examples': [
                '我去过中国。 (Wǒ qù guo Zhōngguó.) - I have been to China.',
                '他吃过北京烤鸭。 (Tā chī guo Běijīng kǎoyā.) - He has eaten Beijing duck.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,
                rule_name='把 Structure', 
                rule_description='把 moves the object before the verb. Used for disposal or manipulation of objects.',
                difficulty_level=3
            ),
            'examples': [
                '我把书放在桌子上。 (Wǒ bǎ shū fàng zài zhuōzi shàng.) - I put the book on the table.',
                '请把门关上。 (Qǐng bǎ mén guān shàng.) - Please close the door.'
            ]
        },

        # More rules to reach 50...
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=58,
                rule_name='被 Structure', 
                rule_description='被 forms passive sentences. The receiver of action becomes the subject.',
                difficulty_level=3
            ),
            'examples': [
                '书被他拿走了。 (Shū bèi tā ná zǒu le.) - The book was taken by him.',
                '我的自行车被偷了。 (Wǒ de zìxíngchē bèi tōu le.) - My bicycle was stolen.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=59,
                rule_name='是...的 Structure', 
                rule_description='是...的 emphasizes time, place, manner, or purpose of past actions.',
                difficulty_level=3
            ),
            'examples': [
                '我是昨天来的。 (Wǒ shì zuótiān lái de.) - It was yesterday that I came.',
                '他是坐飞机去的。 (Tā shì zuò fēijī qù de.) - It was by plane that he went.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=52,
                rule_name='Result Complement', 
                rule_description='Shows the result of an action. Comes directly after the verb.',
                difficulty_level=2
            ),
            'examples': [
                '我看完书了。 (Wǒ kàn wán shū le.) - I finished reading the book.',
                '他听见了声音。 (Tā tīng jiàn le shēngyīn.) - He heard the sound.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=53,
                rule_name='Direction Complement', 
                rule_description='Shows direction of movement. 来 (toward speaker) or 去 (away from speaker).',
                difficulty_level=2
            ),
            'examples': [
                '他走上来了。 (Tā zǒu shàng lái le.) - He walked up (toward me).',
                '请拿进去。 (Qǐng ná jìn qù.) - Please take it inside (away from me).'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=60,
                rule_name='Comparative 比', 
                rule_description='比 used for comparisons: A 比 B + adjective.',
                difficulty_level=2
            ),
            'examples': [
                '我比他高。 (Wǒ bǐ tā gāo.) - I am taller than him.',
                '中文比英文难。 (Zhōngwén bǐ Yīngwén nán.) - Chinese is more difficult than English.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=61,
                rule_name='Superlative 最', 
                rule_description='最 used for superlatives: 最 + adjective.',
                difficulty_level=2
            ),
            'examples': [
                '他最高。 (Tā zuì gāo.) - He is the tallest.',
                '这是最好的书。 (Zhè shì zuì hǎo de shū.) - This is the best book.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=62,
                rule_name='Verb Reduplication', 
                rule_description='Reduplicating verbs makes the action brief or casual.',
                difficulty_level=2
            ),
            'examples': [
                '你看看这本书。 (Nǐ kàn kan zhè běn shū.) - Take a look at this book.',
                '我试试这件衣服。 (Wǒ shì shi zhè jiàn yīfu.) - Let me try on this clothing.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,
                rule_name='Potential Complement', 
                rule_description='Shows ability or possibility. Insert 得 (can) or 不 (cannot) in complements.',
                difficulty_level=3
            ),
            'examples': [
                '我看得懂中文。 (Wǒ kàn de dǒng zhōngwén.) - I can understand written Chinese.',
                '我听不清楚。 (Wǒ tīng bù qīngchu.) - I cannot hear clearly.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=65,
                rule_name='Time Expression Order', 
                rule_description='Time words generally come before the verb, after the subject.',
                difficulty_level=2
            ),
            'examples': [
                '我明天去北京。 (Wǒ míngtiān qù Běijīng.) - I go to Beijing tomorrow.',
                '他每天学习中文。 (Tā měitiān xuéxí zhōngwén.) - He studies Chinese every day.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=66,
                rule_name='Location Expressions', 
                rule_description='在 + location comes before the verb.',
                difficulty_level=2
            ),
            'examples': [
                '我在图书馆看书。 (Wǒ zài túshūguǎn kàn shū.) - I read books in the library.',
                '他在公司工作。 (Tā zài gōngsī gōngzuò.) - He works at the company.'
            ]
        },
        # Continue adding more rules...
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,
                rule_name='Adverb Placement', 
                rule_description='Adverbs usually come before the verb they modify.',
                difficulty_level=2
            ),
            'examples': [
                '他很高兴。 (Tā hěn gāoxìng.) - He is very happy.',
                '我也去。 (Wǒ yě qù.) - I also go.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,
                rule_name='Conjunction 和', 
                rule_description='和 connects nouns, not clauses or sentences.',
                difficulty_level=2
            ),
            'examples': [
                '我和他 (wǒ hé tā) - me and him',
                '书和笔 (shū hé bǐ) - books and pens'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,
                rule_name='但是 for Contrast', 
                rule_description='但是 (but) connects contrasting clauses.',
                difficulty_level=2
            ),
            'examples': [
                '我很累，但是还要工作。 (Wǒ hěn lèi, dànshì hái yào gōngzuò.) - I am tired, but still have to work.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,
                rule_name='个 - General Measure Word', 
                rule_description='个 is the most common measure word, used for people and general objects.',
                difficulty_level=1
            ),
            'examples': [
                '一个人 (yī gè rén) - one person',
                '三个苹果 (sān gè píngguǒ) - three apples'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,
                rule_name='本 for Books', 
                rule_description='本 used for books, magazines, and notebooks.',
                difficulty_level=1
            ),
            'examples': [
                '一本书 (yī běn shū) - one book',
                '两本杂志 (liǎng běn zázhì) - two magazines'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,
                rule_name='张 for Flat Objects', 
                rule_description='张 used for flat objects like paper, tables, tickets.',
                difficulty_level=2
            ),
            'examples': [
                '一张纸 (yī zhāng zhǐ) - one piece of paper',
                '三张桌子 (sān zhāng zhuōzi) - three tables'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=54,
                rule_name='Question Particle 呢', 
                rule_description='呢 used for follow-up questions or how about questions.',
                difficulty_level=2
            ),
            'examples': [
                '我很好，你呢？ (Wǒ hěn hǎo, nǐ ne?) - I am fine, and you?',
                '我的书在这儿，你的呢？ (Wǒ de shū zài zhèr, nǐ de ne?) - My book is here, where is yours?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=12,
                rule_name='Affirmative-Negative Questions', 
                rule_description='Repeat the verb in affirmative and negative form to form questions.',
                difficulty_level=2
            ),
            'examples': [
                '你是不是学生？ (Nǐ shì bù shì xuéshēng?) - Are you a student or not?',
                '你去不去学校？ (Nǐ qù bù qù xuéxiào?) - Are you going to school or not?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=55,
                rule_name='Degree Complement 得', 
                rule_description='得 introduces complements describing degree or manner.',
                difficulty_level=3
            ),
            'examples': [
                '他说得很好。 (Tā shuō de hěn hǎo.) - He speaks very well.',
                '我跑得快。 (Wǒ pǎo de kuài.) - I run fast.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,
                rule_name='因为...所以', 
                rule_description='因为 (because)...所以 (so) for cause and effect.',
                difficulty_level=2
            ),
            'examples': [
                '因为下雨，所以我们不去公园。 (Yīnwèi xià yǔ, suǒyǐ wǒmen bù qù gōngyuán.) - Because it is raining, so we are not going to the park.'
            ]
        },
        # Add 20 more rules to reach 50...
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=39,
                rule_name='了 Placement Rules', 
                rule_description='了 can go after the verb for completion or at sentence end for change of state.',
                difficulty_level=3
            ),
            'examples': [
                '我买了三本书。 (Wǒ mǎi le sān běn shū.) - I bought three books.',
                '我吃饭了。 (Wǒ chī fàn le.) - I have eaten.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=60,
                rule_name='Negative Comparison', 
                rule_description='没有 for negative comparisons: A 没有 B + adjective.',
                difficulty_level=2
            ),
            'examples': [
                '我没有他高。 (Wǒ méiyǒu tā gāo.) - I am not as tall as him.',
                '这本书没有那本书有意思。 (Zhè běn shū méiyǒu nà běn shū yǒuyìsi.) - This book is not as interesting as that book.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,
                rule_name='Negative Adverbs', 
                rule_description='不 and 没 come before verbs. 不 for present/future, 没 for past.',
                difficulty_level=2
            ),
            'examples': [
                '我不去。 (Wǒ bù qù.) - I am not going.',
                '他没来。 (Tā méi lái.) - He did not come.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,
                rule_name='Frequency Adverbs', 
                rule_description='常常, 经常, 总是 come before the verb.',
                difficulty_level=2
            ),
            'examples': [
                '我常常去图书馆。 (Wǒ chángcháng qù túshūguǎn.) - I often go to the library.',
                '他总是迟到。 (Tā zǒngshì chídào.) - He is always late.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,
                rule_name='虽然...但是', 
                rule_description='虽然 (although)...但是 (but) for concession.',
                difficulty_level=3
            ),
            'examples': [
                '虽然很贵，但是质量很好。 (Suīrán hěn guì, dànshì zhìliàng hěn hǎo.) - Although it is expensive, the quality is very good.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=56,
                rule_name='如果...就', 
                rule_description='如果 (if)...就 (then) for conditional sentences.',
                difficulty_level=3
            ),
            'examples': [
                '如果你来，我就很高兴。 (Rúguǒ nǐ lái, wǒ jiù hěn gāoxìng.) - If you come, then I will be very happy.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,
                rule_name='只 for Animals', 
                rule_description='只 used for animals, birds, and one of a pair.',
                difficulty_level=2
            ),
            'examples': [
                '一只猫 (yī zhī māo) - one cat',
                '两只鸟 (liǎng zhī niǎo) - two birds'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,
                rule_name='辆 for Vehicles', 
                rule_description='辆 used for vehicles with wheels.',
                difficulty_level=2
            ),
            'examples': [
                '一辆汽车 (yī liàng qìchē) - one car',
                '两辆自行车 (liǎng liàng zìxíngchē) - two bicycles'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=62,
                rule_name='Adjective Reduplication', 
                rule_description='Reduplicating adjectives makes them more vivid or informal.',
                difficulty_level=2
            ),
            'examples': [
                '高高 (gāogāo) - very tall',
                '慢慢 (mànmàn) - very slow'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=63,
                rule_name='Coverbs (Preposition-like Verbs)', 
                rule_description='Verbs that function like prepositions, indicating location, direction, etc.',
                difficulty_level=2
            ),
            'examples': [
                '我在家学习。 (Wǒ zài jiā xuéxí.) - I study at home.',
                '他给我一本书。 (Tā gěi wǒ yī běn shū.) - He gives me a book.'
            ]
        },
        # Add 10 more rules...
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=54,
                rule_name='Question Particle 吧', 
                rule_description='吧 used for suggestions or seeking agreement.',
                difficulty_level=2
            ),
            'examples': [
                '我们走吧。 (Wǒmen zǒu ba.) - Let us go.',
                '这是你的书吧？ (Zhè shì nǐ de shū ba?) - This is your book, right?'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=65,
                rule_name='Time Words Order', 
                rule_description='General to specific: Year > Month > Date > Day of week > Time.',
                difficulty_level=2
            ),
            'examples': [
                '我二零二三年十月十五号星期一去。 (Wǒ èr líng èr sān nián shí yuè shíwǔ hào xīngqīyī qù.) - I go on Monday, October 15th, 2023.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=66,
                rule_name='Location with 在', 
                rule_description='在 can indicate location of existence or action location.',
                difficulty_level=2
            ),
            'examples': [
                '书在桌子上。 (Shū zài zhuōzi shàng.) - The book is on the table.',
                '我在家吃饭。 (Wǒ zài jiā chī fàn.) - I eat at home.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=57,
                rule_name='Degree Adverbs', 
                rule_description='很 (very), 太 (too), 最 (most), 更 (more) come before adjectives.',
                difficulty_level=2
            ),
            'examples': [
                '很好吃 (hěn hǎochī) - very delicious',
                '太贵了 (tài guì le) - too expensive'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=55,
                rule_name='Double 了 Structure', 
                rule_description='了 after verb and at sentence end indicates both completion and current relevance.',
                difficulty_level=3
            ),
            'examples': [
                '我买了三本书了。 (Wǒ mǎi le sān běn shū le.) - I have bought three books (so far).',
                '他学了两年中文了。 (Tā xué le liǎng nián zhōngwén le.) - He has studied Chinese for two years.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=54,
                rule_name='Duration with 了', 
                rule_description='When using 了 with duration, object comes before time.',
                difficulty_level=3
            ),
            'examples': [
                '我学中文学了三年。 (Wǒ xué zhōngwén xué le sān nián.) - I studied Chinese for three years.',
                '他看书看了两个小时。 (Tā kàn shū kàn le liǎng gè xiǎoshí.) - He read books for two hours.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=64,
                rule_name='Numeral Classifiers', 
                rule_description='Numbers combined with measure words for counting specific objects.',
                difficulty_level=2
            ),
            'examples': [
                '第一 (dì yī) - first',
                '第二个 (dì èr gè) - second one',
                '第三本书 (dì sān běn shū) - third book'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=40,
                rule_name='Serial Verb Construction', 
                rule_description='Multiple verbs can appear in sequence to describe connected actions.',
                difficulty_level=2
            ),
            'examples': [
                '我去商店买东西。 (Wǒ qù shāngdiàn mǎi dōngxi.) - I go to the store to buy things.',
                '他回家吃饭。 (Tā huí jiā chī fàn.) - He goes home to eat.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=54,
                rule_name='Complement of Duration', 
                rule_description='Shows how long an action lasts. Time expression comes after the verb.',
                difficulty_level=2
            ),
            'examples': [
                '我学了三年中文。 (Wǒ xué le sān nián zhōngwén.) - I studied Chinese for three years.',
                '他等了两个小时。 (Tā děng le liǎng gè xiǎoshí.) - He waited for two hours.'
            ]
        },
        {
            'rule': GrammarRule(
                language_id='zh', 
                concept_id=51,
                rule_name='Measure Word 条', 
                rule_description='条 used for long, flexible objects like rivers, roads, fish.',
                difficulty_level=2
            ),
            'examples': [
                '一条河 (yī tiáo hé) - one river',
                '两条鱼 (liǎng tiáo yú) - two fish',
                '三条路 (sān tiáo lù) - three roads'
            ]
        },
    ]

    print('Adding Chinese grammar rules...')
    added_count = 0

    for rule_data in chinese_rules:
        try:
            db.add(rule_data['rule'])
            db.flush()  # This assigns the rule_id
            
            # Add examples for this rule
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
            db.rollback()
            continue

    db.commit()
    print(f'✅ Successfully added {added_count} Chinese grammar rules with examples!')

    # Count total Chinese rules now
    total_zh_rules = db.query(GrammarRule).filter(GrammarRule.language_id == 'zh').count()
    print(f'Total Chinese grammar rules in database: {total_zh_rules}')

    # Count examples
    zh_rule_ids = [r.rule_id for r in db.query(GrammarRule.rule_id).filter(GrammarRule.language_id == 'zh').all()]
    total_examples = db.query(RuleExample).filter(RuleExample.rule_id.in_(zh_rule_ids)).count()
    print(f'Total examples for Chinese rules: {total_examples}')

    db.close()

if __name__ == '__main__':
    add_chinese_rules()