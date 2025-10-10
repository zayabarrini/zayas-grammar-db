#!/usr/bin/env python3
"""
Extract proper German grammar rules from UD data
"""

import os
from collections import defaultdict, Counter
from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample, GrammarConcept

def analyze_german_ud_patterns(file_path):
    """
    Analyze German UD patterns based on actual dependency relations
    """
    sentences = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            current_sentence = []
            sentence_text = ""
            
            for line in f:
                line = line.strip()
                
                if line.startswith('# text = '):
                    sentence_text = line[9:]
                
                elif line.startswith('#'):
                    continue
                
                elif not line:  # Empty line indicates sentence end
                    if current_sentence and sentence_text:
                        sentences.append({
                            'text': sentence_text,
                            'tokens': current_sentence
                        })
                    current_sentence = []
                    sentence_text = ""
                
                else:
                    # Parse token line
                    parts = line.split('\t')
                    if len(parts) >= 10 and '-' not in parts[0]:
                        token_info = {
                            'id': parts[0],
                            'form': parts[1],
                            'lemma': parts[2],
                            'upos': parts[3],
                            'xpos': parts[4],
                            'feats': parts[5],
                            'head': parts[6],
                            'deprel': parts[7],
                            'deps': parts[8],
                            'misc': parts[9]
                        }
                        current_sentence.append(token_info)
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return sentences

def extract_german_specific_rules(sentences):
    """
    Extract German-specific grammar rules based on UD patterns
    """
    patterns = defaultdict(list)
    
    for sentence in sentences:
        text = sentence['text']
        tokens = sentence['tokens']
        
        # Skip very short sentences
        if len(tokens) < 4:
            continue
            
        # German-specific patterns
        for token in tokens:
            # Case usage patterns
            if 'Case=' in token.get('feats', ''):
                case_info = token['feats'].split('Case=')[1].split('|')[0]
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token:
                    patterns['case_usage'].append({
                        'word': token['form'],
                        'case': case_info,
                        'head': head_token['form'],
                        'relation': token['deprel'],
                        'sentence': text
                    })
            
            # Verb second (V2) pattern detection
            if token['upos'] == 'VERB' and token['deprel'] == 'root':
                # Check if verb is in second position
                verb_position = int(token['id'])
                if verb_position == 2:  # V2 pattern
                    patterns['verb_second'].append({
                        'verb': token['form'],
                        'sentence': text
                    })
            
            # Separable prefix verbs
            if token['deprel'] == 'compound:prt':
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token and head_token['upos'] == 'VERB':
                    patterns['separable_verbs'].append({
                        'prefix': token['form'],
                        'verb': head_token['form'],
                        'sentence': text
                    })
            
            # Adjective declension patterns
            if token['upos'] == 'ADJ' and token['deprel'] == 'amod':
                if 'Case=' in token.get('feats', '') and 'Degree=' in token.get('feats', ''):
                    patterns['adjective_declension'].append({
                        'adjective': token['form'],
                        'features': token['feats'],
                        'sentence': text
                    })
    
    return patterns

def create_proper_german_rules(patterns):
    """
    Create proper German grammar rules based on UD analysis
    """
    grammar_rules = []
    
    # Case system rules
    if 'case_usage' in patterns:
        case_examples = patterns['case_usage'][:5]
        case_rule = {
            'name': 'German Case System',
            'description': 'Usage of grammatical cases (Nominative, Accusative, Dative, Genitive) in German sentences',
            'examples': [ex['sentence'] for ex in case_examples],
            'difficulty': 3,
            'concept': 'case_system'
        }
        grammar_rules.append(case_rule)
    
    # Verb second rule
    if 'verb_second' in patterns:
        v2_examples = patterns['verb_second'][:5]
        v2_rule = {
            'name': 'Verb Second (V2) Word Order',
            'description': 'In main clauses, the finite verb appears in the second position',
            'examples': [ex['sentence'] for ex in v2_examples],
            'difficulty': 2,
            'concept': 'word_order'
        }
        grammar_rules.append(v2_rule)
    
    # Separable verbs
    if 'separable_verbs' in patterns:
        sep_examples = patterns['separable_verbs'][:5]
        sep_rule = {
            'name': 'Separable Prefix Verbs',
            'description': 'Verbs with separable prefixes that move to the end of the clause',
            'examples': [ex['sentence'] for ex in sep_examples],
            'difficulty': 3,
            'concept': 'verb_prefixes'
        }
        grammar_rules.append(sep_rule)
    
    # Adjective declension
    if 'adjective_declension' in patterns:
        adj_examples = patterns['adjective_declension'][:5]
        adj_rule = {
            'name': 'Adjective Declension',
            'description': 'Adjective endings change based on case, gender, number, and definiteness',
            'examples': [ex['sentence'] for ex in adj_examples],
            'difficulty': 4,
            'concept': 'adjective_declension'
        }
        grammar_rules.append(adj_rule)
    
    return grammar_rules

def integrate_proper_german_rules():
    """
    Integrate proper German grammar rules from UD data
    """
    ud_path = "/home/zaya/Downloads/Workspace/Universal_Dependencies_2.16/ud-treebanks-v2.16/UD_German-HDT/de_hdt-ud-train.conllu"
    
    if not os.path.exists(ud_path):
        print(f"German UD file not found: {ud_path}")
        return
    
    print("Analyzing German UD patterns...")
    sentences = analyze_german_ud_patterns(ud_path)
    print(f"Found {len(sentences)} German sentences")
    
    if not sentences:
        return
    
    patterns = extract_german_specific_rules(sentences)
    print(f"Extracted {sum(len(v) for v in patterns.values())} German-specific patterns")
    
    grammar_rules = create_proper_german_rules(patterns)
    print(f"Created {len(grammar_rules)} proper German grammar rules")
    
    # Add to database
    db = SessionLocal()
    added_count = 0
    
    for rule_data in grammar_rules:
        try:
            # Find or create concept
            concept = db.query(GrammarConcept).filter(
                GrammarConcept.concept_name == rule_data['concept']
            ).first()
            
            if not concept:
                concept = GrammarConcept(
                    concept_name=rule_data['concept'],
                    category='german_specific',
                    description=f'German-specific grammar concept from UD analysis'
                )
                db.add(concept)
                db.flush()
            
            # Check if rule already exists
            existing_rule = db.query(GrammarRule).filter(
                GrammarRule.language_id == 'de',
                GrammarRule.rule_name == rule_data['name']
            ).first()
            
            if not existing_rule:
                grammar_rule = GrammarRule(
                    language_id='de',
                    concept_id=concept.concept_id,
                    rule_name=rule_data['name'],
                    rule_description=rule_data['description'],
                    difficulty_level=rule_data['difficulty'],
                    usage_context='german_ud_specific'
                )
                
                db.add(grammar_rule)
                db.flush()
                
                # Add examples
                for example_text in rule_data['examples']:
                    example = RuleExample(
                        rule_id=grammar_rule.rule_id,
                        example_sentence=example_text
                    )
                    db.add(example)
                
                added_count += 1
                print(f"Added: {rule_data['name']}")
            else:
                print(f"Skipped (already exists): {rule_data['name']}")
                
        except Exception as e:
            print(f"Error adding rule: {e}")
    
    db.commit()
    db.close()
    print(f"✅ Added {added_count} proper German grammar rules")

if __name__ == '__main__':
    integrate_proper_german_rules()