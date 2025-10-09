-- Initial schema setup
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Your tables from the previous design go here
-- (languages, grammar_concepts, grammar_rules, rule_examples, etc.)


-- 1. Languages table
CREATE TABLE languages (
    language_id CHAR(2) PRIMARY KEY,  -- ISO 639-1 codes
    language_name VARCHAR(50) NOT NULL,
    language_family VARCHAR(50),
    script VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Grammar concepts (universal taxonomy)
CREATE TABLE grammar_concepts (
    concept_id SERIAL PRIMARY KEY,
    concept_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,  -- 'case', 'tense', 'particle', etc.
    description TEXT,
    universal_linguistic_id VARCHAR(50)  -- Links to linguistic standards
);

-- 3. Grammar rules main table
CREATE TABLE grammar_rules (
    rule_id SERIAL PRIMARY KEY,
    language_id CHAR(2) NOT NULL REFERENCES languages(language_id),
    concept_id INTEGER REFERENCES grammar_concepts(concept_id),
    rule_name VARCHAR(200) NOT NULL,
    rule_description TEXT NOT NULL,
    usage_context VARCHAR(100),  -- 'formal', 'informal', 'written', 'spoken'
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Examples for rules
CREATE TABLE rule_examples (
    example_id SERIAL PRIMARY KEY,
    rule_id INTEGER NOT NULL REFERENCES grammar_rules(rule_id) ON DELETE CASCADE,
    example_sentence TEXT NOT NULL,
    example_translation TEXT,
    example_romanization TEXT,  -- For non-Latin scripts
    example_gloss TEXT,  -- Linguistic interlinear gloss
    notes TEXT
);

-- 5. Cross-language rule relationships
CREATE TABLE rule_relationships (
    relationship_id SERIAL PRIMARY KEY,
    source_rule_id INTEGER REFERENCES grammar_rules(rule_id),
    target_rule_id INTEGER REFERENCES grammar_rules(rule_id),
    relationship_type VARCHAR(50) NOT NULL,  -- 'equivalent', 'contrasts_with', 'similar_to'
    confidence_level INTEGER CHECK (confidence_level BETWEEN 1 AND 5),
    notes TEXT,
    UNIQUE(source_rule_id, target_rule_id, relationship_type)
);

-- 6. Language-specific exceptions and notes
CREATE TABLE rule_exceptions (
    exception_id SERIAL PRIMARY KEY,
    rule_id INTEGER NOT NULL REFERENCES grammar_rules(rule_id) ON DELETE CASCADE,
    exception_pattern TEXT NOT NULL,
    exception_description TEXT NOT NULL,
    frequency VARCHAR(20)  -- 'common', 'rare', 'archaic'
);