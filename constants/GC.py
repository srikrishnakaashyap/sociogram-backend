from dotenv import load_dotenv, dotenv_values
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

class GC:

    config = dotenv_values(".env")
    DATABASE_URI = config.get('DB_URL')
    DATABASE_NAME = config.get('DB_NAME')
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")
    SECRET_KEY = config.get('SECRET_KEY')
    JWT_HASH_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    S3_ACCESS_KEY = config.get("S3_ACCESS_KEY")
    S3_SECRET_KEY = config.get("S3_SECRET_KEY")
    S3_BUCKET_NAME = config.get("S3_SECRET_KEY")
    S3_UPLOAD_FOLDER_NAME = config.get("S3_SECRET_KEY")
    WEB3 = config.get("WEB3")

    



