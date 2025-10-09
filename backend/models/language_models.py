from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class Language(Base):
    __tablename__ = "languages"
    
    language_id = Column(String(2), primary_key=True)
    language_name = Column(String(50), nullable=False)
    language_family = Column(String(50))
    script = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())

class GrammarConcept(Base):
    __tablename__ = "grammar_concepts"
    
    concept_id = Column(Integer, primary_key=True, autoincrement=True)
    concept_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    universal_linguistic_id = Column(String(50))

class GrammarRule(Base):
    __tablename__ = "grammar_rules"
    
    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    language_id = Column(String(2), ForeignKey('languages.language_id'), nullable=False)
    concept_id = Column(Integer, ForeignKey('grammar_concepts.concept_id'))
    rule_name = Column(String(200), nullable=False)
    rule_description = Column(Text, nullable=False)
    usage_context = Column(String(100))
    difficulty_level = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    language = relationship("Language")
    concept = relationship("GrammarConcept")
    examples = relationship("RuleExample", back_populates="rule", cascade="all, delete-orphan")

class RuleExample(Base):
    __tablename__ = "rule_examples"
    
    example_id = Column(Integer, primary_key=True, autoincrement=True)
    rule_id = Column(Integer, ForeignKey('grammar_rules.rule_id'), nullable=False)
    example_sentence = Column(Text, nullable=False)
    example_translation = Column(Text)
    example_romanization = Column(Text)
    example_gloss = Column(Text)
    notes = Column(Text)
    
    # Relationships
    rule = relationship("GrammarRule", back_populates="examples")