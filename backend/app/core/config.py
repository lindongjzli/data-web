import os

# MongoDB Configurations
# Example: "mongodb://username:password@host:port/"
# For local development, we can use the default local instance.
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

# JWT Configurations
# This is a secret key for signing JWT tokens.
# In a real application, this should be a much more complex and securely stored key.
# You can generate a good secret key using: openssl rand -hex 32
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-key-that-is-long-and-random")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dataset path
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
