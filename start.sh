#!/bin/zsh

# start.sh - Zsh version with better job control

PROJECT_ROOT="$(pwd)"

echo "Starting Zayas Grammar DB..."
echo "Project root: $PROJECT_ROOT"

# Check directories
[[ ! -d "$PROJECT_ROOT/backend" ]] && { echo "Error: backend directory not found"; exit 1 }
[[ ! -d "$PROJECT_ROOT/frontend" ]] && { echo "Error: frontend directory not found"; exit 1 }

# Cleanup function
cleanup() {
    echo "\n🛑 Stopping all services..."
    cd "$PROJECT_ROOT/backend" && sudo docker-compose down
    kill %1 %2 %3 2>/dev/null
    exit 0
}

trap cleanup SIGINT

# Start services
echo "🐘 Starting Database..."
cd "$PROJECT_ROOT/backend" && sudo docker-compose up -d

sleep 5

echo "🚀 Starting Backend..."
cd "$PROJECT_ROOT/backend" && pipenv run uvicorn main:app --reload --port 8000 &!

sleep 3

echo "💻 Starting Frontend..."
cd "$PROJECT_ROOT/frontend" && npm run dev -- --port 5173 &!

echo "✅ All services started!"
echo "📊 Services:"
echo "   - Database:  http://localhost:5432"
echo "   - Backend:   http://localhost:8000"
echo "   - Frontend:  http://localhost:5173"
echo ""
echo "🔍 Check jobs: jobs"
echo "🛑 Stop all:  Ctrl+C"

# Keep script running
wait