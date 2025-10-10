#!/usr/bin/env python3
"""
Integrate Universal Dependencies data from local treebanks
"""

import os
import glob
from collections import defaultdict, Counter
from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample, GrammarConcept, UDTreebankSentence, UDTokenAnalysis

def find_ud_treebanks(base_path):
    """
    Find all UD treebanks in the local directory
    """
    treebanks = {}
    
    # Map our language codes to UD treebank patterns
    language_mapping = {
        'zh': ['UD_Chinese-*', 'UD_Chinese_GSD', 'UD_Chinese-PUD'],
        'de': ['UD_German-*', 'UD_German_GSD', 'UD_German-HDT'],
        'ru': ['UD_Russian-*', 'UD_Russian_GSD', 'UD_Russian-SynTagRus'],
        'fr': ['UD_French-*', 'UD_French_GSD', 'UD_French-Sequoia'],
        'it': ['UD_Italian-*', 'UD_Italian_ISDT', 'UD_Italian-PoSTWITA'],
        'ja': ['UD_Japanese-*', 'UD_Japanese_GSD', 'UD_Japanese-BCCWJ'],
        'ar': ['UD_Arabic-*', 'UD_Arabic_PADT', 'UD_Arabic-NYUAD'],
        'hi': ['UD_Hindi-*', 'UD_Hindi_HDTB', 'UD_Hindi-English-HIENCS']
    }
    
    for lang_code, patterns in language_mapping.items():
        for pattern in patterns:
            search_path = os.path.join(base_path, pattern, "*.conllu")
            files = glob.glob(search_path)
            if files:
                treebanks[lang_code] = files
                print(f"Found treebank for {lang_code}: {files[0]}")
                break
    
    return treebanks

def parse_conllu_file(file_path):
    """
    Parse a CONLL-U file and extract sentences with annotations
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
                    # Parse token line: ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
                    parts = line.split('\t')
                    if len(parts) >= 10 and '-' not in parts[0]:  # Skip multi-word tokens
                        token_info = {
                            'id': parts[0],
                            'form': parts[1],
                            'lemma': parts[2],
                            'upos': parts[3],  # Universal POS tag
                            'xpos': parts[4],  # Language-specific POS tag
                            'feats': parts[5],
                            'head': parts[6],
                            'deprel': parts[7],  # Dependency relation
                            'deps': parts[8],
                            'misc': parts[9]
                        }
                        current_sentence.append(token_info)
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return sentences

def analyze_grammar_patterns(sentences, language_code):
    """
    Analyze sentences to extract common grammar patterns
    """
    patterns = defaultdict(list)
    pos_stats = Counter()
    deprel_stats = Counter()
    
    for sentence in sentences:
        text = sentence['text']
        tokens = sentence['tokens']
        
        # Collect POS and dependency statistics
        for token in tokens:
            pos_stats[token['upos']] += 1
            deprel_stats[token['deprel']] += 1
        
        # Extract specific grammar patterns
        for i, token in enumerate(tokens):
            # Subject-verb patterns
            if token['deprel'] == 'nsubj':
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token and head_token['upos'] == 'VERB':
                    patterns['subject_verb'].append({
                        'subject': token['form'],
                        'verb': head_token['form'],
                        'sentence': text
                    })
            
            # Object patterns
            elif token['deprel'] in ['obj', 'iobj']:
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token and head_token['upos'] == 'VERB':
                    patterns['verb_object'].append({
                        'object': token['form'],
                        'verb': head_token['form'],
                        'sentence': text
                    })
            
            # Modifier patterns
            elif token['deprel'] in ['amod', 'advmod']:
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token:
                    patterns['modifiers'].append({
                        'modifier': token['form'],
                        'modified': head_token['form'],
                        'relation': token['deprel'],
                        'sentence': text
                    })
    
    print(f"  POS distribution: {dict(pos_stats.most_common(5))}")
    print(f"  Top dependencies: {dict(deprel_stats.most_common(5))}")
    
    return patterns, pos_stats, deprel_stats

def create_grammar_rules_from_patterns(patterns, language_code, pos_stats, deprel_stats):
    """
    Create grammar rules from analyzed patterns
    """
    grammar_rules = []
    
    # Rule for most common POS patterns
    most_common_pos = pos_stats.most_common(3)
    if most_common_pos:
        pos_rule = {
            'name': f'Common Parts of Speech',
            'description': f'Most frequent word types: {", ".join([f"{pos} ({count})" for pos, count in most_common_pos])}',
            'examples': [],
            'difficulty': 1
        }
        grammar_rules.append(pos_rule)
    
    # Rule for sentence structure patterns
    if 'subject_verb' in patterns and patterns['subject_verb']:
        sv_rule = {
            'name': 'Subject-Verb Structure',
            'description': 'Basic sentence structure with subjects and verbs',
            'examples': [p['sentence'] for p in patterns['subject_verb'][:3]],
            'difficulty': 2
        }
        grammar_rules.append(sv_rule)
    
    if 'verb_object' in patterns and patterns['verb_object']:
        vo_rule = {
            'name': 'Verb-Object Structure',
            'description': 'Verbs with their objects',
            'examples': [p['sentence'] for p in patterns['verb_object'][:3]],
            'difficulty': 2
        }
        grammar_rules.append(vo_rule)
    
    # Rule for modifiers
    if 'modifiers' in patterns and patterns['modifiers']:
        mod_rule = {
            'name': 'Modifier Usage',
            'description': 'How adjectives and adverbs modify other words',
            'examples': [p['sentence'] for p in patterns['modifiers'][:3]],
            'difficulty': 2
        }
        grammar_rules.append(mod_rule)
    
    return grammar_rules

def integrate_language_treebank(language_code, file_path):
    """
    Integrate a single language's treebank
    """
    print(f"\nProcessing {language_code} from {file_path}")
    
    # Parse the treebank
    sentences = parse_conllu_file(file_path)
    print(f"  Found {len(sentences)} sentences")
    
    if not sentences:
        return 0
    
    # Analyze patterns
    patterns, pos_stats, deprel_stats = analyze_grammar_patterns(sentences, language_code)
    
    # Create grammar rules
    grammar_rules = create_grammar_rules_from_patterns(patterns, language_code, pos_stats, deprel_stats)
    print(f"  Created {len(grammar_rules)} grammar rules")
    
    # Add to database
    db = SessionLocal()
    added_count = 0
    
    for rule_data in grammar_rules:
        try:
            # Find or create a concept
            concept_name = rule_data['name'].lower().replace(' ', '_')
            concept = db.query(GrammarConcept).filter(
                GrammarConcept.concept_name == concept_name
            ).first()
            
            if not concept:
                # Create new concept
                concept = GrammarConcept(
                    concept_name=concept_name,
                    category='universal_dependencies',
                    description=f'Pattern from UD analysis: {rule_data["name"]}'
                )
                db.add(concept)
                db.flush()
            
            # Create grammar rule
            grammar_rule = GrammarRule(
                language_id=language_code,
                concept_id=concept.concept_id,
                rule_name=rule_data['name'],
                rule_description=rule_data['description'],
                difficulty_level=rule_data['difficulty'],
                usage_context='universal_dependencies'
            )
            
            db.add(grammar_rule)
            db.flush()
            
            # Add examples
            for example_text in rule_data['examples']:
                example = RuleExample(
                    rule_id=grammar_rule.rule_id,
                    example_sentence=example_text,
                    notes='From Universal Dependencies treebank'
                )
                db.add(example)
            
            added_count += 1
            
        except Exception as e:
            print(f"Error adding rule: {e}")
            continue
    
    # Store some sentence examples in UD tables
    stored_sentences = 0
    for i, sentence in enumerate(sentences[:10]):  # Store first 10 sentences
        try:
            ud_sentence = UDTreebankSentence(
                language_id=language_code,
                sentence_text=sentence['text'],
                source=os.path.basename(file_path),
                treebank_metadata='{}'
            )
            db.add(ud_sentence)
            db.flush()
            
            # Store token analysis
            for token in sentence['tokens']:
                ud_token = UDTokenAnalysis(
                    sentence_id=ud_sentence.sentence_id,
                    token_id=token['id'],
                    form=token['form'],
                    lemma=token['lemma'],
                    upos=token['upos'],
                    xpos=token['xpos'],
                    feats=token['feats'],
                    head=token['head'],
                    deprel=token['deprel']
                )
                db.add(ud_token)
            
            stored_sentences += 1
            
        except Exception as e:
            print(f"Error storing sentence: {e}")
            continue
    
    db.commit()
    db.close()
    
    print(f"  ✅ Added {added_count} rules and {stored_sentences} example sentences")
    return added_count

def main():
    """
    Main integration function
    """
    ud_base_path = "/home/zaya/Downloads/Workspace/Universal_Dependencies_2.16/ud-treebanks-v2.16"
    
    if not os.path.exists(ud_base_path):
        print(f"UD treebanks path not found: {ud_base_path}")
        return
    
    # Find available treebanks
    treebanks = find_ud_treebanks(ud_base_path)
    
    if not treebanks:
        print("No UD treebanks found for target languages")
        return
    
    print(f"Found treebanks for {len(treebanks)} languages: {list(treebanks.keys())}")
    
    total_rules_added = 0
    
    for lang_code, files in treebanks.items():
        for file_path in files:
            if 'train.conllu' in file_path or 'dev.conllu' in file_path:
                rules_added = integrate_language_treebank(lang_code, file_path)
                total_rules_added += rules_added
                break  # Process only one file per language for now
    
    print(f"\n🎉 Integration complete! Added {total_rules_added} UD-based grammar rules")

if __name__ == '__main__':
    main()