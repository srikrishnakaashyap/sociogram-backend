from dotenv import load_dotenv, dotenv_values
from fastapi.security import OAuth2PasswordBearer

class GC:

    config = dotenv_values(".env")
    DATABASE_URI = config.get('DB_URL')
    DATABASE_NAME = config.get('DB_NAME')
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")
    



