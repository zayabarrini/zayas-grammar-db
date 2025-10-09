#!/bin/bash

echo "Resetting Zayas Grammar Database..."

cd backend

# Stop and remove containers
docker-compose down

# Remove volumes (WARNING: This will delete all data)
docker volume rm backend_postgres_data

# Start fresh
docker-compose up -d

# Wait for database
sleep 10

# Create tables
pipenv run python -c "
from config.database import engine, Base
from models.language_models import *
Base.metadata.create_all(bind=engine)
print('✅ Tables created!')
"

# Seed data
pipenv run python database/seeds/initial_data.py

echo "✅ Reset complete!"