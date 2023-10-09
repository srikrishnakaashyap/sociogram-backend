from fastapi import APIRouter, Depends, HTTPException, status, Form
from models.mongo.post import Post
from models.request.post import CreatePostModel
from models.mongo.user import User
from models.neo.user import User as GraphUser
from models.mongo.file import File
from typing import Annotated
from services.user_service import get_current_user
from services.media_storage import MediaStorage


router = APIRouter()

@router.put("/connect/{email}", response_description="Returns True if Connection Request is Sent")
async def connection_request(user: Annotated[User, Depends(get_current_user)], email):
    try:
        from_user = GraphUser.nodes.get(email=user.email)
        to_user = GraphUser.nodes.get(email=email)
        to_user.connection_requests.connect(from_user)

        return {"status": 200, "message": "Connection Request Sent Successfully"}
    except Exception as e:
        return {"status": 500, "message": f"Failed with error: {e}"}


@router.get("/view-connections")
async def view_connection_requests(user: Annotated[User, Depends(get_current_user)]):
    try:
        current_user = GraphUser.nodes.get(email=user.email)
        connection_request = current_user.connection_requests.get_or_none(email=email)
        connections1 = current_user.connection.get_or_none(email=email)
        connection_requests = GraphUser.nodes.get(email=user.email).connection_requests.all()
        user_objects = [await User.find_one(User.email == i.email) for i in connection_requests]
        response_objects = []
        for user in user_objects:
            response_objects.append({"email": user.email, "name": user.name})
        return {"status": 200, "message": "Fetch Successful", "users": response_objects}
    except Exception as e:
        return {"status": 404, "message": f"Failed with error: {e}"}
    
@router.put("/accept-connection/{email}")
async def accept_connection_request(user: Annotated[User, Depends(get_current_user)], email):
    try:
        current_user = GraphUser.nodes.get(email=user.email)
        connection_request = current_user.connection_requests.get_or_none(email=email)
        if connection_request:
            from_user = GraphUser.nodes.get(email=email)
            to_user = current_user
            to_user.connections.connect(from_user)
            from_user.connections.connect(to_user)
            to_user.connection_requests.disconnect(from_user)

            return {"status": 200, "message": "Connection Request Accepted Successfully"}
        else:
            return {"status": 404, "message": "Connection Request not found"}
    except Exception as e:
        return {"status": 500, "message": f"Failed with error: {e}"}



