from dotenv import load_dotenv, dotenv_values

class GC:

    config = dotenv_values(".env")
    DATABASE_URI = config.get('DB_URL')
    DATABASE_NAME = config.get('DB_NAME')



