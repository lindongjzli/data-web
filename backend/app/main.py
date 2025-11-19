from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth_api, dataset_api
from app.db.mongodb_utils import connect_to_mongo, close_mongo_connection

# Create FastAPI app instance
app = FastAPI(title="Dataset Sharing Platform API")

# Add CORS middleware to allow cross-origin requests from the frontend
# This is important for development when frontend and backend run on different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add event handlers for database connection
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Include API routers
app.include_router(auth_api.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dataset_api.router, prefix="/api/dataset", tags=["Dataset"])


@app.get("/")
async def read_root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the Data-Web API. Visit /docs for documentation."}
