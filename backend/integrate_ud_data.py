#!/usr/bin/env python3
"""
Integrate Universal Dependencies data into our grammar database
"""

import requests
import re
from collections import defaultdict, Counter
from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample, GrammarConcept
from sqlalchemy import func

def download_ud_treebank(language_code, treebank_name):
    """
    Download UD treebank data
    """
    base_url = "https://raw.githubusercontent.com/UniversalDependencies/"
    
    # Map our language codes to UD treebanks
    ud_mapping = {
        'zh': 'UD_Chinese-GSD',
        'de': 'UD_German-GSD', 
        'ru': 'UD_Russian-GSD',
        'fr': 'UD_French-GSD',
        'it': 'UD_Italian-ISDT',
        'ja': 'UD_Japanese-GSD',
        'ar': 'UD_Arabic-PADT',
        'hi': 'UD_Hindi-HDTB'
    }
    
    if language_code not in ud_mapping:
        print(f"No UD treebank available for {language_code}")
        return None
    
    treebank = ud_mapping[language_code]
    url = f"{base_url}{treebank}/master/{treebank.lower()}-ud-train.conllu"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {treebank}: {e}")
        return None

def parse_conllu(data):
    """
    Parse CONLL-U format data
    """
    sentences = []
    current_sentence = []
    
    for line in data.split('\n'):
        line = line.strip()
        
        if line.startswith('#'):
            if line.startswith('# text = '):
                sentence_text = line[9:]
            continue
            
        if not line:  # Empty line indicates sentence end
            if current_sentence:
                sentences.append({
                    'text': sentence_text,
                    'tokens': current_sentence
                })
                current_sentence = []
            continue
            
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
    
    return sentences

def extract_grammar_patterns(sentences, language_code):
    """
    Extract common grammar patterns from UD data
    """
    patterns = defaultdict(list)
    
    for sentence in sentences:
        text = sentence['text']
        tokens = sentence['tokens']
        
        # Extract dependency patterns
        dep_relations = [(t['form'], t['deprel']) for t in tokens]
        
        # Common patterns to look for
        for i, token in enumerate(tokens):
            # Subject-verb relationships
            if token['deprel'] == 'nsubj':
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token and head_token['upos'] == 'VERB':
                    patterns['nsubj'].append({
                        'subject': token['form'],
                        'verb': head_token['form'],
                        'sentence': text
                    })
            
            # Object-verb relationships
            elif token['deprel'] in ['obj', 'iobj']:
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token and head_token['upos'] == 'VERB':
                    patterns['obj'].append({
                        'object': token['form'],
                        'verb': head_token['form'],
                        'sentence': text
                    })
            
            # Adjective-noun relationships
            elif token['deprel'] == 'amod':
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token and head_token['upos'] == 'NOUN':
                    patterns['amod'].append({
                        'adjective': token['form'],
                        'noun': head_token['form'],
                        'sentence': text
                    })
            
            # Adverb-verb relationships
            elif token['deprel'] == 'advmod':
                head_token = next((t for t in tokens if t['id'] == token['head']), None)
                if head_token and head_token['upos'] == 'VERB':
                    patterns['advmod'].append({
                        'adverb': token['form'],
                        'verb': head_token['form'],
                        'sentence': text
                    })
    
    return patterns

def map_ud_to_grammar_concepts(patterns, language_code):
    """
    Map UD patterns to our grammar concepts
    """
    concept_mapping = {
        'nsubj': 'nominative_case',  # Subjects
        'obj': 'accusative_case',    # Objects
        'iobj': 'dative_case',       # Indirect objects
        'amod': 'adjective_usage',   # Adjective modification
        'advmod': 'adverb_placement', # Adverb usage
    }
    
    grammar_rules = []
    
    for pattern_type, examples in patterns.items():
        if pattern_type in concept_mapping:
            concept_name = concept_mapping[pattern_type]
            
            # Get the most frequent patterns
            if examples:
                # Create a rule based on this pattern
                rule_description = f"Pattern extracted from UD data: {pattern_type.upper()} relationship"
                
                # Use first few examples
                sample_examples = examples[:3]
                
                grammar_rules.append({
                    'concept': concept_name,
                    'description': rule_description,
                    'examples': [ex['sentence'] for ex in sample_examples],
                    'pattern_type': pattern_type
                })
    
    return grammar_rules

def integrate_ud_for_language(language_code):
    """
    Main function to integrate UD data for a specific language
    """
    print(f"Integrating UD data for {language_code}...")
    
    # Download UD data
    ud_data = download_ud_treebank(language_code, None)
    if not ud_data:
        print(f"No UD data available for {language_code}")
        return 0
    
    # Parse the data
    sentences = parse_conllu(ud_data)
    print(f"Parsed {len(sentences)} sentences for {language_code}")
    
    if not sentences:
        print(f"No sentences parsed for {language_code}")
        return 0
    
    # Extract patterns
    patterns = extract_grammar_patterns(sentences, language_code)
    print(f"Extracted {sum(len(v) for v in patterns.values())} grammar patterns")
    
    # Map to grammar concepts
    grammar_rules = map_ud_to_grammar_concepts(patterns, language_code)
    print(f"Mapped to {len(grammar_rules)} grammar rules")
    
    # Add to database
    db = SessionLocal()
    added_count = 0
    
    for rule_data in grammar_rules:
        try:
            # Find the concept
            concept = db.query(GrammarConcept).filter(
                GrammarConcept.concept_name == rule_data['concept']
            ).first()
            
            if not concept:
                print(f"Concept not found: {rule_data['concept']}")
                continue
            
            # Create grammar rule
            grammar_rule = GrammarRule(
                language_id=language_code,
                concept_id=concept.concept_id,
                rule_name=f"UD Pattern: {rule_data['pattern_type']}",
                rule_description=rule_data['description'],
                difficulty_level=2,  # Medium difficulty
                usage_context='universal_dependencies'
            )
            
            db.add(grammar_rule)
            db.flush()
            
            # Add examples
            for example_text in rule_data['examples']:
                example = RuleExample(
                    rule_id=grammar_rule.rule_id,
                    example_sentence=example_text,
                    notes=f"From UD treebank - {rule_data['pattern_type']}"
                )
                db.add(example)
            
            added_count += 1
            
        except Exception as e:
            print(f"Error adding rule: {e}")
            continue
    
    db.commit()
    db.close()
    
    print(f"✅ Added {added_count} UD-based rules for {language_code}")
    return added_count

def create_ud_concepts():
    """
    Create UD-specific grammar concepts if they don't exist
    """
    db = SessionLocal()
    
    ud_concepts = [
        GrammarConcept(concept_name='universal_pos_tags', category='universal', description='Universal Part-of-Speech tags from UD'),
        GrammarConcept(concept_name='dependency_relations', category='syntax', description='Universal Dependency relations'),
        GrammarConcept(concept_name='syntactic_trees', category='syntax', description='Sentence structure analysis'),
        GrammarConcept(concept_name='morphological_features', category='morphology', description='Word form features'),
        GrammarConcept(concept_name='cross_linguistic_patterns', category='comparative', description='Patterns across multiple languages'),
    ]
    
    added = 0
    for concept in ud_concepts:
        try:
            db.merge(concept)
            added += 1
        except Exception as e:
            print(f"Error adding concept {concept.concept_name}: {e}")
    
    db.commit()
    db.close()
    print(f"✅ Added {added} UD-specific concepts")

if __name__ == '__main__':
    # First, create UD-specific concepts
    create_ud_concepts()
    
    # Then integrate data for each language
    languages = ['zh', 'de', 'ru', 'fr', 'it', 'ja', 'ar', 'hi']
    total_added = 0
    
    for lang in languages:
        added = integrate_ud_for_language(lang)
        total_added += added
    
    print(f"\n🎉 Total UD rules added: {total_added}")