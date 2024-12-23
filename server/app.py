from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.caption import router as caption_router
from routes.song import router as song_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(caption_router, prefix="/api/caption", tags=["caption"])
app.include_router(song_router, prefix="/api/song", tags=["song"])

@app.get("/")
async def root():
    return {"message": "Welcome to Instagram Caption Generator API"}