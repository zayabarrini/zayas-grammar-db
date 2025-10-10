#!/usr/bin/env python3
"""
Enhanced UD integration with better grammar rule extraction
"""

import os
import glob
from collections import defaultdict, Counter
from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample, GrammarConcept, UDTreebankSentence, UDTokenAnalysis

def extract_meaningful_patterns(sentences, language_code):
    """
    Extract more meaningful grammar patterns from UD data
    """
    patterns = defaultdict(list)
    language_specific_insights = []
    
    for sentence in sentences:
        text = sentence['text']
        tokens = sentence['tokens']
        
        # Skip very short or very long sentences
        if len(tokens) < 3 or len(tokens) > 50:
            continue
            
        # Extract word order patterns
        pos_sequence = [token['upos'] for token in tokens]
        pos_bigram = ' '.join(pos_sequence[:min(5, len(pos_sequence))])
        
        # Language-specific pattern analysis
        if language_code == 'zh':  # Chinese
            # Look for measure words and their nouns
            for i, token in enumerate(tokens):
                if token['upos'] == 'NUM' and i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if next_token['upos'] == 'NOUN' and 'measure' in next_token.get('feats', '').lower():
                        patterns['measure_words'].append({
                            'num': token['form'],
                            'measure': next_token['form'],
                            'sentence': text
                        })
        
        elif language_code == 'de':  # German
            # Look for verb-second patterns
            verbs = [t for t in tokens if t['upos'] == 'VERB']
            if len(verbs) >= 2:
                patterns['verb_second'].append({
                    'verbs': [v['form'] for v in verbs],
                    'sentence': text
                })
        
        elif language_code == 'ja':  # Japanese
            # Look for topic markers
            for token in tokens:
                if token['form'] in ['は', 'が', 'を']:
                    patterns['particles'].append({
                        'particle': token['form'],
                        'sentence': text
                    })
        
        elif language_code == 'ru':  # Russian
            # Look for case markers
            for token in tokens:
                if 'Case=' in token.get('feats', ''):
                    case = token['feats'].split('Case=')[1].split('|')[0]
                    patterns['cases'].append({
                        'word': token['form'],
                        'case': case,
                        'sentence': text
                    })
        
        # Universal patterns
        subjects = [t for t in tokens if t['deprel'] == 'nsubj']
        objects = [t for t in tokens if t['deprel'] in ['obj', 'iobj']]
        verbs = [t for t in tokens if t['upos'] == 'VERB']
        
        if subjects and verbs:
            patterns['subject_verb'].append({
                'subject': subjects[0]['form'],
                'verb': verbs[0]['form'],
                'sentence': text
            })
        
        if objects and verbs:
            patterns['verb_object'].append({
                'object': objects[0]['form'],
                'verb': verbs[0]['form'],
                'sentence': text
            })
        
        # Adjective-noun patterns
        for token in tokens:
            if token['deprel'] == 'amod':
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token and head_token['upos'] == 'NOUN':
                    patterns['adjective_noun'].append({
                        'adjective': token['form'],
                        'noun': head_token['form'],
                        'sentence': text
                    })
    
    return patterns

def create_enhanced_grammar_rules(patterns, language_code, pos_stats, deprel_stats):
    """
    Create more sophisticated grammar rules from patterns
    """
    grammar_rules = []
    
    # Create rules based on most frequent patterns
    if 'subject_verb' in patterns and patterns['subject_verb']:
        # Analyze subject-verb agreement patterns
        sv_rule = {
            'name': 'Basic Sentence Structure',
            'description': f'Subject-verb construction with {len(patterns["subject_verb"])} examples found',
            'examples': [p['sentence'] for p in patterns['subject_verb'][:5]],
            'difficulty': 2,
            'concept': 'sentence_structure'
        }
        grammar_rules.append(sv_rule)
    
    if 'verb_object' in patterns and patterns['verb_object']:
        vo_rule = {
            'name': 'Verb-Object Relationships',
            'description': f'Transitive verb usage with direct objects',
            'examples': [p['sentence'] for p in patterns['verb_object'][:5]],
            'difficulty': 2,
            'concept': 'verb_objects'
        }
        grammar_rules.append(vo_rule)
    
    if 'adjective_noun' in patterns and patterns['adjective_noun']:
        adj_rule = {
            'name': 'Adjective-Noun Modification',
            'description': f'Adjective placement and noun modification patterns',
            'examples': [p['sentence'] for p in patterns['adjective_noun'][:5]],
            'difficulty': 2,
            'concept': 'adjective_usage'
        }
        grammar_rules.append(adj_rule)
    
    # Language-specific rules
    if language_code == 'zh' and 'measure_words' in patterns:
        measure_rule = {
            'name': 'Chinese Measure Words',
            'description': f'Usage of measure words with numerals',
            'examples': [p['sentence'] for p in patterns['measure_words'][:5]],
            'difficulty': 3,
            'concept': 'measure_words'
        }
        grammar_rules.append(measure_rule)
    
    if language_code == 'de' and 'verb_second' in patterns:
        v2_rule = {
            'name': 'German V2 Word Order',
            'description': f'Verb-second position in main clauses',
            'examples': [p['sentence'] for p in patterns['verb_second'][:5]],
            'difficulty': 3,
            'concept': 'word_order'
        }
        grammar_rules.append(v2_rule)
    
    if language_code == 'ja' and 'particles' in patterns:
        particle_rule = {
            'name': 'Japanese Particles',
            'description': f'Usage of case and topic particles',
            'examples': [p['sentence'] for p in patterns['particles'][:5]],
            'difficulty': 2,
            'concept': 'particles'
        }
        grammar_rules.append(particle_rule)
    
    if language_code == 'ru' and 'cases' in patterns:
        case_rule = {
            'name': 'Russian Case System',
            'description': f'Grammatical case usage in nouns',
            'examples': [p['sentence'] for p in patterns['cases'][:5]],
            'difficulty': 3,
            'concept': 'case_system'
        }
        grammar_rules.append(case_rule)
    
    return grammar_rules

def integrate_enhanced_ud():
    """
    Enhanced UD integration with better pattern extraction
    """
    ud_base_path = "/home/zaya/Downloads/Workspace/Universal_Dependencies_2.16/ud-treebanks-v2.16"
    
    if not os.path.exists(ud_base_path):
        print(f"UD treebanks path not found: {ud_base_path}")
        return
    
    # Use the same treebank finding logic
    from integrate_local_ud import find_ud_treebanks, parse_conllu_file
    
    treebanks = find_ud_treebanks(ud_base_path)
    
    if not treebanks:
        print("No UD treebanks found for target languages")
        return
    
    print(f"Found treebanks for {len(treebanks)} languages")
    
    db = SessionLocal()
    total_rules_added = 0
    
    for lang_code, files in treebanks.items():
        for file_path in files:
            if 'train.conllu' in file_path or 'dev.conllu' in file_path:
                print(f"\nProcessing {lang_code} from {file_path}")
                
                # Parse the treebank
                sentences = parse_conllu_file(file_path)
                print(f"  Found {len(sentences)} sentences")
                
                if not sentences:
                    continue
                
                # Extract meaningful patterns
                patterns = extract_meaningful_patterns(sentences, lang_code)
                print(f"  Extracted {sum(len(v) for v in patterns.values())} patterns")
                
                # Get basic stats for context
                pos_stats = Counter(t['upos'] for s in sentences for t in s['tokens'])
                deprel_stats = Counter(t['deprel'] for s in sentences for t in s['tokens'])
                
                # Create enhanced grammar rules
                grammar_rules = create_enhanced_grammar_rules(patterns, lang_code, pos_stats, deprel_stats)
                print(f"  Created {len(grammar_rules)} enhanced grammar rules")
                
                # Add to database
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
                                category='universal_dependencies',
                                description=f'Enhanced pattern from UD analysis'
                            )
                            db.add(concept)
                            db.flush()
                        
                        # Create grammar rule
                        grammar_rule = GrammarRule(
                            language_id=lang_code,
                            concept_id=concept.concept_id,
                            rule_name=rule_data['name'],
                            rule_description=rule_data['description'],
                            difficulty_level=rule_data['difficulty'],
                            usage_context='enhanced_ud'
                        )
                        
                        db.add(grammar_rule)
                        db.flush()
                        
                        # Add examples
                        for example_text in rule_data['examples']:
                            example = RuleExample(
                                rule_id=grammar_rule.rule_id,
                                example_sentence=example_text,
                                notes='From enhanced UD analysis'
                            )
                            db.add(example)
                        
                        added_count += 1
                        print(f"    Added: {rule_data['name']}")
                        
                    except Exception as e:
                        print(f"    Error adding rule {rule_data['name']}: {e}")
                        continue
                
                total_rules_added += added_count
                print(f"  ✅ Added {added_count} enhanced rules for {lang_code}")
                break  # Process only one file per language
    
    db.commit()
    db.close()
    print(f"\n🎉 Enhanced integration complete! Added {total_rules_added} rules")

if __name__ == '__main__':
    integrate_enhanced_ud()