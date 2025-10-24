#!/bin/zsh

# start.sh - Launch using tmux sessions

PROJECT_ROOT="$(pwd)"

echo "Starting Zayas Grammar DB in tmux..."
echo "Project root: $PROJECT_ROOT"

# Check directories
[[ ! -d "$PROJECT_ROOT/backend" ]] && { echo "Error: backend directory not found"; exit 1 }
[[ ! -d "$PROJECT_ROOT/frontend" ]] && { echo "Error: frontend directory not found"; exit 1 }

# Create new tmux session
tmux new-session -d -s zayas-grammar -n "Database" "cd $PROJECT_ROOT/backend && sudo docker-compose up -d; zsh"

# Wait for database
sleep 5

# Create new windows in the same session
tmux new-window -t zayas-grammar:1 -n "Backend" "cd $PROJECT_ROOT/backend && pipenv shell && uvicorn main:app --reload --port 8000"
tmux new-window -t zayas-grammar:2 -n "Frontend" "cd $PROJECT_ROOT/frontend && npm run dev -- --port 5173"

# Attach to the session
echo "✅ All services started in tmux session 'zayas-grammar'"
echo "📊 To attach: tmux attach -t zayas-grammar"
echo "📊 To detach: Ctrl+b, then d"
echo "📊 Services:"
echo "   - Database:  http://localhost:5432"
echo "   - Backend:   http://localhost:8000"
echo "   - Frontend:  http://localhost:5173"