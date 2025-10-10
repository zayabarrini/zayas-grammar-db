#!/usr/bin/env python3
"""
Fix UD table field sizes
"""

from config.database import engine, Base
from models.language_models import *

def fix_ud_tables():
    # Drop and recreate the UD tables with correct field sizes
    UDTokenAnalysis.__table__.drop(engine, checkfirst=True)
    UDTreebankSentence.__table__.drop(engine, checkfirst=True)
    
    # Recreate tables
    Base.metadata.create_all(bind=engine)
    print("✅ UD tables recreated with correct field sizes")

if __name__ == '__main__':
    fix_ud_tables()