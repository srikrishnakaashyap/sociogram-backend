from fastapi import FastAPI
from initializers.setup_config import SetupConfig
from api import user

app = FastAPI()
SetupConfig(app)

app.include_router(user.router)
