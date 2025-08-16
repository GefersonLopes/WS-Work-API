import os;

class Config:
    NODE_ENV = os.getenv("NODE_ENV", "development")
    PORT = int(os.getenv("PORT", "3000"))
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+pg8000://{os.getenv('DB_USER','postgres')}:{os.getenv('DB_PASS','postgres')}"
        f"@{os.getenv('DB_HOST','localhost')}:{os.getenv('DB_PORT','5432')}/{os.getenv('DB_NAME','wswork_cars')}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS","").split(",") if o.strip()]
    RUN_SEED = os.getenv("RUN_SEED","false").lower() == "true"
