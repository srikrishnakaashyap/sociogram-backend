from fastapi import APIRouter, Depends
from typing import Annotated
from services.dashboard_service import DashboardService
from services.neo4j_service import Neo4jService
from services.user_service import get_current_user
from models.mongo.user import User

router = APIRouter()


@router.get('/dashboard-posts')
async def dashboard_posts(user: Annotated[User, Depends(get_current_user)]):
    try:
        # connections = await Neo4jService.all_connections(user)
        # serialized_connections= await Neo4jService.serialize(connections)
        posts = await DashboardService.get_posts_by_user(user)
        return {"status": 200, "message": "Fetch Successful", "posts": posts}
    except Exception as e:
        return {"status": 500, "message": f"Failed with error: {e}"}
