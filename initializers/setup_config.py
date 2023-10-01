from .db.db import connect_and_init_db, close_db_connect

class SetupConfig:
    def __init__(self, app):
        app.add_event_handler("startup", connect_and_init_db)
        app.add_event_handler("shutdown", close_db_connect)

        