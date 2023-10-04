from fastapi import FastAPI
from initializers.setup_config import SetupConfig
from api import user, post
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

SetupConfig(app)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
