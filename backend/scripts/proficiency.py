from ..config.database import SessionLocal
from ..models.language_models import GrammarRule

db = SessionLocal()

# Count Chinese rules by difficulty level
difficulty_counts = db.query(
    GrammarRule.difficulty_level, 
    db.func.count(GrammarRule.rule_id)
).filter(
    GrammarRule.language_id == 'zh'
).group_by(
    GrammarRule.difficulty_level
).all()

print('Current Chinese Rules by Difficulty Level:')
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

total_zh = db.query(GrammarRule).filter(GrammarRule.language_id == 'zh').count()
print(f'\\nTotal Chinese rules: {total_zh}')

db.close()
