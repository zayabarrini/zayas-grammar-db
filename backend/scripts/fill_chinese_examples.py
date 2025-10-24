#!/usr/bin/env python3
"""
Add missing examples to Chinese rules and include advanced word order patterns
"""

from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample


def add_missing_chinese_examples():
    db = SessionLocal()

    # Rules that need examples (based on your CSV data)
    rules_needing_examples = [
        {
            "rule_id": 95,
            "examples": [
                "我们学习中文。 (Wǒmen xuéxí zhōngwén.) - We study Chinese.",
                "他看书。 (Tā kàn shū.) - He reads books.",
                "我吃苹果。 (Wǒ chī píngguǒ.) - I eat apples.",
            ],
        },
        {
            "rule_id": 114,
            "examples": [
                "这本书，很有意思。 (Zhè běn shū, hěn yǒuyìsi.) - This book, very interesting.",
                "北京，我去过三次。 (Běijīng, wǒ qùguò sān cì.) - Beijing, I have been three times.",
                "中文，他学了五年。 (Zhōngwén, tā xué le wǔ nián.) - Chinese, he studied for five years.",
            ],
        },
        {
            "rule_id": 117,
            "examples": [
                "我吃了饭。 (Wǒ chī le fàn.) - I ate/have eaten.",
                "他去了北京。 (Tā qù le Běijīng.) - He went to Beijing.",
                "天气冷了。 (Tiānqì lěng le.) - The weather has gotten cold.",
            ],
        },
        {
            "rule_id": 118,
            "examples": [
                "你好吗？ (Nǐ hǎo ma?) - How are you?",
                "他是老师吗？ (Tā shì lǎoshī ma?) - Is he a teacher?",
                "你喜欢中文吗？ (Nǐ xǐhuān zhōngwén ma?) - Do you like Chinese?",
            ],
        },
        {
            "rule_id": 119,
            "examples": [
                "你是谁？ (Nǐ shì shéi?) - Who are you?",
                "这是什么？ (Zhè shì shénme?) - What is this?",
                "你去哪里？ (Nǐ qù nǎlǐ?) - Where are you going?",
            ],
        },
        {
            "rule_id": 120,
            "examples": [
                "他坐着看书。 (Tā zuò zhe kàn shū.) - He is sitting and reading.",
                "门开着。 (Mén kāi zhe.) - The door is open.",
                "她笑着说话。 (Tā xiào zhe shuōhuà.) - She speaks while smiling.",
            ],
        },
        {
            "rule_id": 121,
            "examples": [
                "我去过中国。 (Wǒ qùguò Zhōngguó.) - I have been to China.",
                "他吃过北京烤鸭。 (Tā chīguò Běijīng kǎoyā.) - He has eaten Peking duck.",
                "我们见过面。 (Wǒmen jiànguò miàn.) - We have met before.",
            ],
        },
        {
            "rule_id": 122,
            "examples": [
                "我把书放在桌子上。 (Wǒ bǎ shū fàng zài zhuōzi shàng.) - I put the book on the table.",
                "他把作业做完了。 (Tā bǎ zuòyè zuò wán le.) - He finished his homework.",
                "请把门关上。 (Qǐng bǎ mén guān shàng.) - Please close the door.",
            ],
        },
        {
            "rule_id": 123,
            "examples": [
                "他被老师批评了。 (Tā bèi lǎoshī pīpíng le.) - He was criticized by the teacher.",
                "书被他拿走了。 (Shū bèi tā ná zǒu le.) - The book was taken away by him.",
                "问题被解决了。 (Wèntí bèi jiějué le.) - The problem was solved.",
            ],
        },
        {
            "rule_id": 124,
            "examples": [
                "我是昨天来的。 (Wǒ shì zuótiān lái de.) - It was yesterday that I came.",
                "他是在北京学的汉语。 (Tā shì zài Běijīng xué de Hànyǔ.) - It was in Beijing that he studied Chinese.",
                "我们是坐飞机去的。 (Wǒmen shì zuò fēijī qù de.) - It was by plane that we went.",
            ],
        },
    ]

    print("Adding missing examples to Chinese rules...")
    added_examples_count = 0

    for rule_data in rules_needing_examples:
        try:
            # Check if rule exists and get current examples
            rule = (
                db.query(GrammarRule)
                .filter(GrammarRule.rule_id == rule_data["rule_id"])
                .first()
            )
            if not rule:
                print(f"Rule ID {rule_data['rule_id']} not found, skipping...")
                continue

            current_examples = (
                db.query(RuleExample)
                .filter(RuleExample.rule_id == rule_data["rule_id"])
                .all()
            )

            if not current_examples:  # Only add if no examples exist
                for example_text in rule_data["examples"]:
                    example = RuleExample(
                        rule_id=rule_data["rule_id"], example_sentence=example_text
                    )
                    db.add(example)
                    added_examples_count += 1

                print(f"Added examples to rule: {rule.rule_name}")
            else:
                print(f"Rule {rule.rule_name} already has examples, skipping...")

        except Exception as e:
            print(f'Error adding examples to rule ID {rule_data["rule_id"]}: {e}')
            continue

    db.commit()
    print(f"✅ Successfully added {added_examples_count} examples to Chinese rules!")


def add_advanced_word_order_rules():
    db = SessionLocal()

    advanced_word_order_rules = [
        # Advanced Word Order Patterns (Difficulty 4-5)
        {
            "rule": GrammarRule(
                language_id="zh",
                concept_id=59,  # Advanced word order
                rule_name="Complex Topic-Comment with Multiple Topics",
                rule_description="Multiple topics stacked before the comment, common in academic and formal writing.",
                difficulty_level=5,
                usage_context="academic",
            ),
            "examples": [
                "拉康的偏执、享乐和身体真实的交集，这个问题我们需要深入探讨。 (Lākāng de piānzhí, xiǎnglè hé shēntǐ zhēnshí de jiāojí, zhège wèntí wǒmen xūyào shēnrù tàntǎo.) - The intersection of Lacan's paranoia, jouissance, and bodily truth, this issue requires our in-depth exploration.",
                "现代社会的快速变化、技术发展和文化转型，这些现象都值得我们研究。 (Xiàndài shèhuì de kuàisù biànhuà, jìshù fāzhǎn hé wénhuà zhuǎnxíng, zhèxiē xiànxiàng dōu zhídé wǒmen yánjiū.) - The rapid changes, technological development, and cultural transformation of modern society, these phenomena are all worth our research.",
            ],
        },
        {
            "rule": GrammarRule(
                language_id="zh",
                concept_id=60,  # Preposed objects
                rule_name="Object Preposing for Emphasis",
                rule_description="Moving objects to the beginning of sentences for emphasis, different from English word order.",
                difficulty_level=4,
                usage_context="literary",
            ),
            "examples": [
                "这本书，我已经读了三遍。 (Zhè běn shū, wǒ yǐjīng dú le sān biàn.) - This book, I have already read three times.",
                "那个问题，我们必须尽快解决。 (Nàgè wèntí, wǒmen bìxū jǐnkuài jiějué.) - That problem, we must solve as soon as possible.",
            ],
        },
        {
            "rule": GrammarRule(
                language_id="zh",
                concept_id=61,  # Time expressions
                rule_name="Complex Time Expression Order",
                rule_description="Multiple time expressions in specific order: duration > frequency > general time > specific time.",
                difficulty_level=4,
                usage_context="formal",
            ),
            "examples": [
                "他每天上午八点到十点都在图书馆学习三个小时。 (Tā měitiān shàngwǔ bā diǎn dào shí diǎn dōu zài túshūguǎn xuéxí sān gè xiǎoshí.) - Every day from 8 to 10 AM, he studies in the library for three hours.",
                "我们去年在中国旅行了整整一个月。 (Wǒmen qùnián zài Zhōngguó lǚxíng le zhěngzhěng yī gè yuè.) - Last year we traveled in China for a whole month.",
            ],
        },
        {
            "rule": GrammarRule(
                language_id="zh",
                concept_id=62,  # Multiple modifiers
                rule_name="Multiple Modifier Order",
                rule_description="Complex ordering of multiple adjectives and adverbs before nouns.",
                difficulty_level=4,
                usage_context="academic",
            ),
            "examples": [
                "这是一本非常重要的古代中国哲学经典著作。 (Zhè shì yī běn fēicháng zhòngyào de gǔdài Zhōngguó zhéxué jīngdiǎn zhùzuò.) - This is a very important ancient Chinese philosophical classic work.",
                "那位穿着红色裙子的年轻女演员表演得很出色。 (Nà wèi chuān zhe hóngsè qúnzi de niánqīng nǚ yǎnyuán biǎoyǎn de hěn chūsè.) - That young actress wearing a red dress performed excellently.",
            ],
        },
        {
            "rule": GrammarRule(
                language_id="zh",
                concept_id=63,  # Complex serial verbs
                rule_name="Complex Serial Verb Constructions",
                rule_description="Multiple verbs in sequence describing complex actions and purposes.",
                difficulty_level=4,
                usage_context="narrative",
            ),
            "examples": [
                "他站起来走过去开门让客人进来坐下喝茶。 (Tā zhàn qǐlai zǒu guòqù kāi mén ràng kèrén jìnlái zuò xià hē chá.) - He stood up, walked over, opened the door, let the guest come in, sit down, and drink tea.",
                "我打算明天去书店买几本关于中国历史的书来看。 (Wǒ dǎsuàn míngtiān qù shūdiàn mǎi jǐ běn guānyú Zhōngguó lìshǐ de shū lái kàn.) - I plan to go to the bookstore tomorrow to buy some books about Chinese history to read.",
            ],
        },
        {
            "rule": GrammarRule(
                language_id="zh",
                concept_id=64,  # Complex location
                rule_name="Complex Location Phrases",
                rule_description="Multiple location indicators in specific hierarchical order.",
                difficulty_level=4,
                usage_context="descriptive",
            ),
            "examples": [
                "书放在桌子左边的抽屉里。 (Shū fàng zài zhuōzi zuǒbiān de chōuti lǐ.) - The book is placed in the drawer on the left side of the table.",
                "他住在北京市海淀区中关村大街的一个小区里。 (Tā zhù zài Běijīng shì Hǎidiàn qū Zhōngguāncūn dàjiē de yī gè xiǎoqū lǐ.) - He lives in a residential area on Zhongguancun Street in Haidian District, Beijing.",
            ],
        },
    ]

    print("\nAdding advanced Chinese word order rules...")
    added_rules_count = 0
    added_examples_count = 0

    for rule_data in advanced_word_order_rules:
        try:
            db.add(rule_data["rule"])
            db.flush()

            for example_text in rule_data["examples"]:
                example = RuleExample(
                    rule_id=rule_data["rule"].rule_id, example_sentence=example_text
                )
                db.add(example)
                added_examples_count += 1

            added_rules_count += 1
            print(f'Added rule: {rule_data["rule"].rule_name}')

        except Exception as e:
            print(f'Error adding rule {rule_data["rule"].rule_name}: {e}')
            continue

    db.commit()
    print(
        f"✅ Successfully added {added_rules_count} advanced word order rules with {added_examples_count} examples!"
    )


def main():
    print("Starting Chinese grammar enhancement...")

    # Add missing examples to existing rules
    add_missing_chinese_examples()

    # Add advanced word order rules
    add_advanced_word_order_rules()

    # Print final statistics
    db = SessionLocal()
    total_rules = db.query(GrammarRule).filter(GrammarRule.language_id == "zh").count()

    rules_with_examples = (
        db.query(GrammarRule)
        .join(RuleExample)
        .filter(GrammarRule.language_id == "zh")
        .distinct()
        .count()
    )

    print(f"\n📊 Final Chinese Rules Statistics:")
    print(f"Total Chinese rules: {total_rules}")
    print(f"Rules with examples: {rules_with_examples}")
    print(f"Rules without examples: {total_rules - rules_with_examples}")
    print(f"Coverage: {(rules_with_examples/total_rules)*100:.1f}%")

    db.close()
    print("\n🎉 Chinese grammar enhancement completed!")


if __name__ == "__main__":
    main()
