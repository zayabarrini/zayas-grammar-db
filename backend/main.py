from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
from models.language_models import Language, GrammarConcept, GrammarRule
from api.routes import languages  # Add this import

# Import all models to ensure they are registered with Base
from models.language_models import *

# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

create_tables()

app = FastAPI(title="Zayas Grammar API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(languages.router)  # Add this line

@app.get("/")
async def root():
    return {"message": "Zayas Grammar API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)