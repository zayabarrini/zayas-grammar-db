# Make scripts executable
chmod +x scripts/setup.sh
chmod +x scripts/seed_database.py

# Run the setup
./scripts/setup.sh

# Start development
cd backend
pipenv shell
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# In another terminal
cd frontend
npm run dev


# Database operations
docker-compose up -d              # Start database
docker-compose down              # Stop database
docker-compose logs -f postgres  # View database logs

# Backend
pipenv install <package>         # Add new package
pipenv run pytest               # Run tests
pipenv run black .              # Format code

# Frontend
npm run build                   # Build for production
npm run check                   # Type check
npm run lint                    # Lint code




Terminal 1:
cd ~/Downloads/Zayas/zayas-grammar-db/backend
sudo docker-compose up -d

Terminal 2:
cd ~/Downloads/Zayas/zayas-grammar-db/backend
pipenv shell
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Terminal 3:
cd ~/Downloads/Zayas/zayas-grammar-db/frontend
npm run dev -- --port 5173

Then visit http://localhost:5173/languages - it should work now! 🎉


# Terminal 1 - Database
cd backend && sudo docker-compose up -d

# Terminal 2 - Backend  
cd backend && pipenv shell && uvicorn main:app --reload --port 8000

# Terminal 3 - Frontend
cd frontend && npm run dev -- --port 5173