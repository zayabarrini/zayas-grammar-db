#!/usr/bin/env python3
"""
Export Chinese rules data from the database to a CSV file
"""

import csv
from sqlalchemy.orm import joinedload
from config.database import SessionLocal
from models.language_models import GrammarRule, RuleExample


def export_chinese_rules_to_csv():
    """
    Export Chinese rules to a CSV file
    """
    db = SessionLocal()

    # Get Chinese rules with examples
    chinese_rules = (
        db.query(GrammarRule)
        .filter(GrammarRule.language_id == "zh")
        .options(joinedload(GrammarRule.examples))
        .all()
    )

    # Define CSV file path
    csv_filename = "chinese_rules_export.csv"

    # Prepare data for CSV
    csv_data = []

    for rule in chinese_rules:
        # Join examples into a single string
        examples_text = ""
        if rule.examples:
            examples_list = []
            for example in rule.examples:
                examples_list.append(example.example_sentence)
            examples_text = " | ".join(examples_list)

        # Create row data - using rule_id instead of id
        row = {
            "rule_id": rule.rule_id or "",
            "language_id": rule.language_id or "",
            "rule_name": rule.rule_name or "",
            "rule_description": rule.rule_description or "",
            "difficulty_level": rule.difficulty_level or "",
            "usage_context": rule.usage_context or "",
            "examples": examples_text,
        }
        csv_data.append(row)

    # Write to CSV
    if csv_data:
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "rule_id",
                "language_id",
                "rule_name",
                "rule_description",
                "difficulty_level",
                "usage_context",
                "examples",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(csv_data)

        print(
            f"✅ Successfully exported {len(csv_data)} Chinese rules to {csv_filename}"
        )

        # Print statistics
        total_rules = len(chinese_rules)
        sources = {}
        difficulties = {}

        for rule in chinese_rules:
            source = rule.usage_context or "manual"
            sources[source] = sources.get(source, 0) + 1
            difficulties[rule.difficulty_level] = (
                difficulties.get(rule.difficulty_level, 0) + 1
            )

        print(f"\n📊 Chinese Rules Statistics:")
        print(f"Total rules: {total_rules}")
        print(f"Sources: {sources}")
        print(f"Difficulty distribution: {difficulties}")
    else:
        print("❌ No Chinese rules found to export")

    db.close()


def analyze_chinese_rules():
    """
    Analyze what Chinese rules we currently have
    """
    db = SessionLocal()

    chinese_rules = (
        db.query(GrammarRule)
        .filter(GrammarRule.language_id == "zh")
        .options(joinedload(GrammarRule.examples))
        .all()
    )

    print("Current Chinese Grammar Rules:")
    print("=" * 60)

    for rule in chinese_rules:
        print(f"\nRule ID: {rule.rule_id}")
        print(f"Rule: {rule.rule_name}")
        print(f"Description: {rule.rule_description}")
        print(f"Difficulty: {rule.difficulty_level}")
        print(f"Source: {rule.usage_context}")

        if rule.examples:
            print("Examples:")
            for example in rule.examples[:2]:
                print(f"  - {example.example_sentence[:80]}...")
        else:
            print("No examples")

        print("-" * 40)

    # Statistics
    total_rules = len(chinese_rules)
    sources = {}
    difficulties = {}

    for rule in chinese_rules:
        source = rule.usage_context or "manual"
        sources[source] = sources.get(source, 0) + 1
        difficulties[rule.difficulty_level] = (
            difficulties.get(rule.difficulty_level, 0) + 1
        )

    print(f"\n📊 Chinese Rules Statistics:")
    print(f"Total rules: {total_rules}")
    print(f"Sources: {sources}")
    print(f"Difficulty distribution: {difficulties}")

    db.close()


if __name__ == "__main__":
    # Run both analysis and export
    analyze_chinese_rules()
    print("\n" + "=" * 60)
    export_chinese_rules_to_csv()
