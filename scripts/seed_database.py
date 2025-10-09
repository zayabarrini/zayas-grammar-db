#!/usr/bin/env python3
"""
Database seeding script for initial grammar data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.seed import main

if __name__ == "__main__":
    main()