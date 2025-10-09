#!/bin/bash

echo "Setting up Zayas Grammar Database..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    echo "Run: sudo apt install docker.io docker-compose"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker service."
    echo "Run: sudo systemctl start docker && sudo usermod -aG docker $USER"
    echo "You may need to log out and log back in for group changes to take effect."
    exit 1
fi

# Start database
echo "Starting PostgreSQL database..."
cd backend
docker-compose up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Setup backend
echo "Setting up backend..."
pipenv install

# Setup frontend
echo "Setting up frontend..."
cd ../frontend

# Ensure we're using Node.js 20
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 20.13.1

# Clean install
echo "Installing frontend dependencies..."
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps

cd ..

echo "✅ Setup complete!"
echo ""
echo "🚀 Development servers:"
echo "   Database: localhost:5432"
echo "   PgAdmin:  http://localhost:8080 (admin@zayasgrammar.com / admin)"
echo "   Backend:  cd backend && pipenv shell && uvicorn main:app --reload --port 8000"
echo "   Frontend: cd frontend && npm run dev -- --port 5173"
echo ""
echo "📊 To check services:"
echo "   docker-compose ps (in backend directory)"
echo "   npm run check (in frontend directory)"